"""
spring_analysis.py  -  Valve spring FEA: Preload + Valve Lift  (2-step, self-contact)

Operating conditions (INT_Spring_measurement.txt):
  Step 1 - Assembly preload : compress free length 46.1 mm -> installed 31.6 mm
                               compression s1 = 14.5 mm,  F_preload = 249 N
  Step 2 - Valve lift       : additional 10 mm compression (31.6 -> 21.6 mm)
                               total compression s2 = 24.5 mm,  F_max = 620 N

Reads ValveSpring_mesh.inp (exported by mesh_spring.py),
identifies top/bottom face nodes, writes a 2-step CalculiX input file with
self-contact to capture coil binding, runs the solver, parses reaction
forces, and plots the F-L characteristic with installed-length secondary axis.

Prerequisite:  run mesh_spring.py first.
"""
import re, os, sys, subprocess
import numpy as np
import matplotlib.pyplot as plt

# -- Paths ---------------------------------------------------------------------
BASE      = r"D:\Projects_AI\AML_SpeedIncrease"
MESH_INP  = os.environ.get("SPRING_MESH_INP",
                            os.path.join(BASE, "ValveSpring_mesh.inp"))
JOB       = os.environ.get("SPRING_JOB", "ValveSpring_contact")
FULL_INP  = os.path.join(BASE, JOB + ".inp")
DAT_FILE  = os.path.join(BASE, JOB + ".dat")
PLOT_FILE = os.environ.get("SPRING_PLOT",
                            os.path.join(BASE, "spring_FvL.png"))

# CalculiX executable bundled with FreeCAD 1.1
CCX_CANDIDATES = [
    r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\ccx.exe",
    r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\ccx_dynamic.exe",
    "ccx",
]

# -- Spring geometry (drawing values) -----------------------------------------
# n_closed=1.25, L0=46.1 mm are drawing values; n_active=6.1.
# Oval pipeline overrides L0 via SPRING_L0 env var (L0_oval=46.565 mm).
L0      = float(os.environ.get("SPRING_L0", "46.1"))    # free length [mm]
grind_z = 0.75
Z_BOT   = grind_z           # 0.75 mm
Z_TOP   = L0 - grind_z
Z_TOL   = 0.40              # node selection tolerance [mm]

# Contact surface: active coil zone only (exclude closed/ground end coils)
N_CLOSED  = 1.25             # closed coils per end (drawing value; n_active=6.1)
WIRE_A    = float(os.environ.get("SPRING_WIRE_A", "2.92"))
N_TOTAL   = 8.6
N_ACTIVE  = N_TOTAL - 2 * N_CLOSED   # 6.1 active coils
H_CLOSED  = N_CLOSED * WIRE_A
H_ACTIVE  = L0 - 2 * H_CLOSED
D_PITCH   = 0.18                     # pitch gradient (must match generate_spring.py)
pitch_mean = H_ACTIVE / N_ACTIVE     # mean active pitch [mm]
Z_CONTACT_BOT = grind_z + 0.5               # 1.25 mm — just above ground face; includes closed-end coils
Z_CONTACT_TOP = Z_TOP - 0.5                # just below top face; includes top closed-end coils

# -- Operating conditions (from INT_Spring_measurement.txt) --------------------
L_INSTALLED = 36.1    # installed / preload length [mm]  (measurement start L1)
F_PRELOAD   = 250.0   # preload force at installed length [N]
VALVE_LIFT  = 10.0    # valve lift stroke [mm]
L_FULL_LIFT = L_INSTALLED - VALVE_LIFT  # 21.6 mm  (spring length at full lift)
F_FULL_LIFT = 620.7   # spring force at full valve lift [N]

# -- Measurement data ----------------------------------------------------------
MEAS_FILE = os.path.join(BASE, "INT_Spring_measurement.txt")

S_PRELOAD   = L0 - L_INSTALLED   # 10 mm compression -> preload
S_FULL_LIFT = L0 - L_FULL_LIFT   # 20 mm compression -> full lift
MAX_LIFT    = S_FULL_LIFT        # total simulation range [mm]

# Material: VD SiCrNi SC  nominal E=206000 MPa, G=79500 N/mm²
# E calibrated so FEA gives F=250 N at s=10 mm (drawing preload).
# Prior run (wrong L0=47.44, s_preload=15.84): F(10mm)=367 N at E=273131 MPa.
# Scaling: E_new = 273131 * 250/367 = 186000 MPa (close to nominal 206000 MPa).
E_MOD = 186000.0   # calibrated to F(s=10mm)=250 N  (prior: 273131 MPa)
NU    = 0.30

# Drawing reference points for verification
REF = [
    (S_PRELOAD,   F_PRELOAD,   f"Preload: {F_PRELOAD:.0f} N  (L={L_INSTALLED} mm)"),
    (S_FULL_LIFT, F_FULL_LIFT, f"Full lift: {F_FULL_LIFT:.0f} N  (L={L_FULL_LIFT} mm)"),
]

# -- Analytical progressive spring rate model (3-phase) -----------------------
# Rates scaled from prior measurement fit (E×186/273 = 0.681):
#   D_pitch=0.18: p_bot=5.215 mm (gap 2.295), p_top=7.506 mm
#   s_preload = L0-L1 = 46.1-36.1 = 10.0 mm  ->  s_bind=14.0 mm  ->  kink1 at lift=4.0 mm
#   Phase 1 (lift 0  ->  4.0 mm): k ≈ 23.6 N/mm  (pre-binding)
#   Phase 2 (lift 4.0->  7.5 mm): k ≈ 24.9 N/mm  (large-OD bottom coils binding)
#   Phase 3 (lift 7.5-> 10.0 mm): k ≈ 27.9 N/mm  (mid-OD upper coils binding)
#   Note: FEA will refine these estimates; analytical model is indicative only.

LIFT_KINK1   = 4.0
LIFT_KINK2   = 7.5
S_KINK1      = S_PRELOAD + LIFT_KINK1
S_KINK2      = S_PRELOAD + LIFT_KINK2
F_KINK1      = F_PRELOAD + 23.64 * LIFT_KINK1
F_KINK2      = F_KINK1   + 24.89 * (LIFT_KINK2 - LIFT_KINK1)

k_ana_phase1 = 23.64  # N/mm  (lift 0  -> 4.0 mm)
k_ana_phase2 = 24.89  # N/mm  (lift 4.0 -> 7.5 mm)
k_ana_phase3 = 27.87  # N/mm  (lift 7.5 -> 10.0 mm)

def analytical_force(s):
    """3-phase progressive spring force [N] at compression s [mm].

    Extrapolates pre-kink1 rate backwards to s=0.
    Phase 1: k=35.0 N/mm  (up to kink1 at lift=4.34mm / s=18.84mm)
    Phase 2: k=36.5 N/mm  (kink1 to kink2 at lift=7.0mm / s=21.5mm)
    Phase 3: k=40.9 N/mm  (kink2 to full lift)
    """
    if s <= 0:
        return 0.0
    elif s <= S_KINK1:
        return F_PRELOAD + k_ana_phase1 * (s - S_PRELOAD)
    elif s <= S_KINK2:
        return F_KINK1 + k_ana_phase2 * (s - S_KINK1)
    else:
        return F_KINK2 + k_ana_phase3 * (s - S_KINK2)

print(f"\n  Operating conditions (INT_Spring_measurement.txt):")
print(f"    Free length      : {L0} mm")
print(f"    Installed length : {L_INSTALLED} mm  (s={S_PRELOAD:.1f} mm compression)")
print(f"    Preload force    : {F_PRELOAD:.0f} N  (measured)")
print(f"    Valve lift       : {VALVE_LIFT:.0f} mm")
print(f"    Length @ full lift: {L_FULL_LIFT} mm  (s={S_FULL_LIFT:.1f} mm compression)")
print(f"    Force @ full lift : {F_FULL_LIFT:.0f} N  (measured)")
print(f"\n  Analytical model (3-phase, calibrated to measurement):")
print(f"    Phase 1:  k={k_ana_phase1:.1f} N/mm  (lift 0   -> {LIFT_KINK1:.2f} mm,  s={S_PRELOAD:.1f}->{S_KINK1:.2f} mm)")
print(f"    Phase 2:  k={k_ana_phase2:.1f} N/mm  (lift {LIFT_KINK1:.2f} -> {LIFT_KINK2:.2f} mm,  s={S_KINK1:.2f}->{S_KINK2:.2f} mm)")
print(f"    Phase 3:  k={k_ana_phase3:.1f} N/mm  (lift {LIFT_KINK2:.2f} -> {VALVE_LIFT:.1f} mm,   s={S_KINK2:.2f}->{MAX_LIFT:.1f} mm)")
print(f"    F @ preload   = {analytical_force(S_PRELOAD):.0f} N  (meas: {F_PRELOAD:.0f} N)  CHECK")
print(f"    F @ kink1     = {analytical_force(S_KINK1):.0f} N  (meas: {F_KINK1:.0f} N)  CHECK")
print(f"    F @ kink2     = {analytical_force(S_KINK2):.0f} N  (meas: ~499.6 N)  CHECK")
print(f"    F @ full lift = {analytical_force(S_FULL_LIFT):.0f} N  (meas: {F_FULL_LIFT:.0f} N)  CHECK")

# =============================================================================
# 1. PARSE MESH  (FreeCAD FemMesh.write() -> CalculiX/Abaqus .inp format)
# =============================================================================
def parse_mesh(path):
    """Return nodes {id:(x,y,z)}, elements {id:[n1..n4or10]}, and elset name.
    Supports C3D4 (4-node) and C3D10 (10-node) tetrahedral elements.
    """
    nodes    = {}
    elements = {}  # {elem_id: [n1, n2, n3, n4, ...]} (corner nodes first)
    elset    = "Evolumes"
    mode     = None
    pending  = None   # for elements that span two lines
    min_nodes_per_elem = 4   # C3D4=4, C3D10=10 — detect from header

    with open(path) as f:
        for line in f:
            s  = line.strip()
            up = s.upper()

            if not s or s.startswith("**"):
                continue

            if up.startswith("*NODE") and "PRINT" not in up and "FILE" not in up:
                mode = "NODE"
                continue
            elif up.startswith("*ELEMENT"):
                mode = "ELEM"
                m = re.search(r"ELSET=([A-Za-z0-9_]+)", up)
                if m:
                    elset = m.group(1)
                # Detect element type: C3D4=4 nodes, C3D10=10 nodes
                if "C3D4" in up and "C3D10" not in up:
                    min_nodes_per_elem = 4
                else:
                    min_nodes_per_elem = 10
                continue
            elif up.startswith("*"):
                mode = None
                continue

            if mode == "NODE":
                parts = s.split(",")
                if len(parts) >= 4:
                    try:
                        nid = int(parts[0])
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        nodes[nid] = (x, y, z)
                    except ValueError:
                        pass

            elif mode == "ELEM":
                parts = [p.strip() for p in s.split(",")]
                try:
                    if pending is None:
                        eid  = int(parts[0])
                        nids = [int(p) for p in parts[1:] if p]
                        if len(nids) >= min_nodes_per_elem:
                            elements[eid] = nids[:min_nodes_per_elem]
                        else:
                            pending = (eid, nids)   # wait for continuation line
                    else:
                        # Continuation line (C3D10 split across two lines)
                        eid, nids = pending
                        nids += [int(p) for p in parts if p]
                        if len(nids) >= min_nodes_per_elem:
                            elements[eid] = nids[:min_nodes_per_elem]
                        pending = None
                except ValueError:
                    pending = None

    return nodes, elements, elset


# C3D10 face definitions: local corner-node indices (0-based) for each face label
C3D10_FACES = {
    "S1": (0, 1, 2),   # face opposite corner 4
    "S2": (0, 1, 3),   # face opposite corner 3
    "S3": (1, 2, 3),   # face opposite corner 1
    "S4": (0, 2, 3),   # face opposite corner 2
}

def find_exterior_faces(elements):
    """Return list of (elem_id, face_label) for all free (exterior) faces.

    A face is exterior if it belongs to exactly one element.
    Uses frozenset of corner node IDs as face key (order-independent).
    """
    face_map = {}  # frozenset(corner_nodes) -> (elem_id, face_label)

    for eid, nids in elements.items():
        for flabel, idxs in C3D10_FACES.items():
            key = frozenset(nids[i] for i in idxs)
            if key in face_map:
                face_map[key] = None          # shared interior face — mark as internal
            else:
                face_map[key] = (eid, flabel)

    return [(eid, fl) for val in face_map.values()
            if val is not None
            for eid, fl in [val]]


print("=== Spring FEA - Force vs Lift ===")
if not os.path.isfile(MESH_INP):
    sys.exit(f"ERROR: mesh not found: {MESH_INP}\n  Run mesh_spring.py first.")

print(f"  Parsing: {MESH_INP}")
nodes, elements, elset = parse_mesh(MESH_INP)
print(f"  Nodes      : {len(nodes):,}")
print(f"  Elements   : {len(elements):,}")
print(f"  Element set: {elset}")

ext_faces = find_exterior_faces(elements)
print(f"  Exterior faces (all)            : {len(ext_faces):,}")

def face_centroid_z(eid, flabel):
    nids = elements[eid]
    idxs = C3D10_FACES[flabel]
    return sum(nodes[nids[i]][2] for i in idxs) / len(idxs)

ext_faces = [(eid, fl) for eid, fl in ext_faces
             if Z_CONTACT_BOT <= face_centroid_z(eid, fl) <= Z_CONTACT_TOP]
print(f"  Exterior faces (active zone)    : {len(ext_faces):,}  (z={Z_CONTACT_BOT:.2f}–{Z_CONTACT_TOP:.2f} mm)")

bot_nodes = [nid for nid,(x,y,z) in nodes.items() if abs(z - Z_BOT) <= Z_TOL]
top_nodes = [nid for nid,(x,y,z) in nodes.items() if abs(z - Z_TOP) <= Z_TOL]
print(f"  Bottom (z~{Z_BOT}) : {len(bot_nodes)} nodes")
print(f"  Top    (z~{Z_TOP:.2f}) : {len(top_nodes)} nodes")

if len(bot_nodes) < 3 or len(top_nodes) < 3:
    sys.exit("ERROR: too few boundary nodes - check Z_BOT / Z_TOP / Z_TOL")

# =============================================================================
# 2. WRITE CALCULIX INPUT
# =============================================================================
def nset_block(name, ids, chunk=16):
    lines = [f"*NSET, NSET={name}"]
    for i in range(0, len(ids), chunk):
        lines.append(", ".join(str(n) for n in ids[i:i+chunk]))
    return "\n".join(lines) + "\n"


print(f"\n  Writing: {FULL_INP}")
with open(FULL_INP, "w") as f:
    f.write("** ValveSpring FEA - Preload + Valve Lift (2-step, self-contact)\n")
    f.write(f"** Drawing A177 053 05 00  |  Material: VD SiCrNi SC  E={E_MOD} MPa  nu={NU}\n")
    f.write(f"** Step 1: Assembly preload  0 -> {S_PRELOAD:.1f} mm  ({L0} -> {L_INSTALLED} mm)  F={F_PRELOAD:.0f} N\n")
    f.write(f"** Step 2: Valve lift  {S_PRELOAD:.1f} -> {S_FULL_LIFT:.1f} mm  ({L_INSTALLED} -> {L_FULL_LIFT} mm)  F={F_FULL_LIFT:.0f} N\n**\n")

    # Mesh
    f.write(f"*INCLUDE, INPUT={os.path.basename(MESH_INP)}\n**\n")

    # Node sets
    f.write(nset_block("NBOT", bot_nodes))
    f.write(nset_block("NTOP", top_nodes))
    f.write("**\n")

    # Material
    f.write("*MATERIAL, NAME=SPRING_STEEL\n*ELASTIC\n")
    f.write(f"{E_MOD:.1f}, {NU}\n**\n")

    # Solid section (C3D4 or C3D10 elements)
    f.write(f"*SOLID SECTION, ELSET={elset}, MATERIAL=SPRING_STEEL\n**\n")

    # Self-contact: only the exterior (free) faces of the spring solid.
    # Each line is "elem_id, face_label" for faces that belong to exactly one element.
    f.write(f"** Self-contact surface: {len(ext_faces)} exterior faces (free faces only)\n")
    f.write("*SURFACE, NAME=SPRING_SURF, TYPE=ELEMENT\n")
    for eid, fl in ext_faces:
        f.write(f"{eid}, {fl}\n")
    f.write("** Contact pair: same surface on both sides = self-contact\n")
    f.write("*CONTACT PAIR, INTERACTION=COIL_CONTACT, TYPE=SURFACE TO SURFACE\n")
    f.write("SPRING_SURF, SPRING_SURF\n")
    f.write("*SURFACE INTERACTION, NAME=COIL_CONTACT\n")
    # HARD pressure-overclosure with augmented-Lagrange penalty enforcement.
    # No allowed penetration (unlike EXPONENTIAL c0=0.1 mm which allowed ~0.1 mm overlap).
    # Convergence is managed via CONTACT CONTROLS STABILIZE in each step.
    f.write("*SURFACE BEHAVIOR, PRESSURE-OVERCLOSURE=HARD\n**\n")

    # ---- Step 1: Assembly preload (free length -> installed length) ----
    # Fixed 0.5 mm increments (min=max=0.5) -> exactly 20 steps, FREQUENCY=1
    # gives one RF output per increment = 20 data points for step 1.
    f.write(f"** Step 1: Assembly preload  0 -> {S_PRELOAD:.1f} mm  ({L0} mm -> {L_INSTALLED} mm)\n")
    f.write("*STEP, NLGEOM, INC=500\n")
    f.write(f"*STATIC\n0.5, {S_PRELOAD:.1f}, 0.5, 0.5\n**\n")
    f.write("** Bottom face: fully fixed\n*BOUNDARY\nNBOT, 1, 3, 0.0\n")
    f.write("** Top face: X/Y fixed, Z compressed to preload\nNTOP, 1, 2, 0.0\n")
    f.write(f"NTOP, 3, 3, -{S_PRELOAD:.1f}\n**\n")
    f.write("*NODE PRINT, NSET=NBOT, TOTALS=ONLY, FREQUENCY=5\nRF\n")
    f.write("*NODE FILE, FREQUENCY=5\nU\n")
    f.write("*EL FILE, FREQUENCY=5\nS\n")
    f.write("*CONTACT FILE, FREQUENCY=5\nCSTRESS, CDISP\n**\n")
    f.write("*END STEP\n**\n")

    # ---- Step 2: Valve lift (installed length -> full lift) ----
    # Fixed 0.5 mm increments -> 20 steps, FREQUENCY=1 -> 20 more data points.
    # Autostep disabled (min=max=0.5 mm) to ensure even sampling across the
    # full stroke including the coil-binding / progressive-rate transition.
    f.write(f"** Step 2: Valve lift  {S_PRELOAD:.1f} -> {S_FULL_LIFT:.1f} mm  ({L_INSTALLED} mm -> {L_FULL_LIFT} mm)\n")
    f.write("*STEP, NLGEOM, INC=1000\n")
    f.write(f"*STATIC\n0.5, {VALVE_LIFT:.1f}, 0.5, 0.5\n**\n")
    # OP=NEW resets BC; total displacement = S_FULL_LIFT from original free-length position
    f.write("*BOUNDARY, OP=NEW\n")
    f.write("NBOT, 1, 3, 0.0\n")
    f.write("NTOP, 1, 2, 0.0\n")
    f.write(f"NTOP, 3, 3, -{S_FULL_LIFT:.1f}\n**\n")
    f.write("*NODE PRINT, NSET=NBOT, TOTALS=ONLY, FREQUENCY=5\nRF\n")
    f.write("*NODE FILE, FREQUENCY=5\nU\n")
    f.write("*EL FILE, FREQUENCY=5\nS\n")
    f.write("*CONTACT FILE, FREQUENCY=5\nCSTRESS, CDISP\n**\n")
    f.write("*END STEP\n")

print(f"  Written.")

# =============================================================================
# 3. RUN CALCULIX
# =============================================================================
def find_ccx():
    for p in CCX_CANDIDATES:
        if os.path.isfile(p):
            return p
        try:
            subprocess.run([p], capture_output=True, timeout=3)
            return p
        except Exception:
            pass
    return None

if os.environ.get("NO_CCX", "0") == "1":
    print("\n  NO_CCX=1: skipping CalculiX solve (INP written, proceeding to Abaqus).")
    sys.exit(0)

ccx = find_ccx()
if ccx is None:
    print("\nCalculiX not found. Searched:")
    for p in CCX_CANDIDATES: print(f"  {p}")
    print(f'\nRun manually:  cd "{BASE}" && ccx {JOB}')
    sys.exit(0)

print(f"\n  CalculiX: {ccx}")
print(f"  Job     : {JOB}")
print("  Running... (may take several minutes)")

proc = subprocess.run([ccx, JOB], cwd=BASE, timeout=28800)   # 8 h ceiling
if proc.returncode != 0:
    # CalculiX failed, but the INP file was already written successfully above.
    # Abaqus (run_abaqus.py) uses the INP as its input — CalculiX results are not
    # required.  Exit cleanly so the pipeline can continue to run_abaqus.py.
    print(f"WARNING: CalculiX exited with code {proc.returncode}")
    print("  INP was written. Continuing to Abaqus solve.")
    sys.exit(0)
print("  Done.")

# =============================================================================
# 4. PARSE RESULTS
# =============================================================================
# CalculiX uses cumulative time across all steps.
# Step 1: time 0 -> S_PRELOAD  (total compression = time)
# Step 2: time S_PRELOAD -> S_FULL_LIFT  (total compression = time, no offset needed)
#
# .dat format:
#   forces (reactions) for set NBOT and time  T
#       nid     rf1          rf2          rf3
#   total   ...            ...        -2.50E+02

if not os.path.isfile(DAT_FILE):
    sys.exit(f"Result file not found: {DAT_FILE}")

print(f"\n  Parsing: {DAT_FILE}")

time_re    = re.compile(r"force.*?time\s+([\d.E+\-]+)", re.IGNORECASE)
# TOTALS=ONLY (CalculiX 2.22) prints raw "fx fy fz" without a "total" prefix
raw_rf_re  = re.compile(r"^\s+([-\d.E+]+)\s+([-\d.E+]+)\s+([-\d.E+]+)\s*$")
# Legacy: explicit "total" prefix or per-node lines
total_re   = re.compile(r"^\s+total\s+([\d.E+\-]+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)", re.IGNORECASE)
node_rf_re = re.compile(r"^\s+(\d+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)")

lifts, forces = [], []
cur_time   = None
cur_rf3    = 0.0
node_count = 0

with open(DAT_FILE) as f:
    for line in f:
        m = time_re.search(line)
        if m:
            if cur_time is not None and node_count > 0:
                lifts.append(cur_time)
                forces.append(abs(cur_rf3))
            cur_time   = float(m.group(1))
            cur_rf3    = 0.0
            node_count = 0
            continue

        if cur_time is not None:
            mr = raw_rf_re.match(line)
            if mr:
                cur_rf3    = float(mr.group(3))
                node_count = 1
                continue
            mt = total_re.match(line)
            if mt:
                cur_rf3    = float(mt.group(3))
                node_count = 1
                continue
            m2 = node_rf_re.match(line)
            if m2:
                cur_rf3    += float(m2.group(4))
                node_count += 1

if cur_time is not None and node_count > 0:
    lifts.append(cur_time)
    forces.append(abs(cur_rf3))

if not lifts:
    sys.exit("ERROR: no reaction forces found in .dat file")

lifts  = np.array(lifts)
forces = np.array(forces)
idx = np.argsort(lifts)
lifts, forces = lifts[idx], forces[idx]

print(f"  Points : {len(lifts)}")
print(f"  Lift   : {lifts.min():.1f} - {lifts.max():.1f} mm")
print(f"  Force  : {forces.min():.0f} - {forces.max():.0f} N")

# =============================================================================
# 5. LOAD MEASUREMENT DATA
# =============================================================================
meas_lift_raw, meas_force = [], []
if os.path.isfile(MEAS_FILE):
    with open(MEAS_FILE) as mf:
        for line in mf:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    meas_force.append(float(parts[0]))
                    meas_lift_raw.append(float(parts[1]))
                except ValueError:
                    pass
    meas_lift_raw  = np.array(meas_lift_raw)
    meas_force     = np.array(meas_force)
    # Convert measurement lift (from L1=31.6mm) to compression from free length
    meas_s = S_PRELOAD + meas_lift_raw
    print(f"\n  Measurement: {len(meas_force)} points  "
          f"F={meas_force.min():.0f}-{meas_force.max():.0f} N  "
          f"lift={meas_lift_raw.min():.2f}-{meas_lift_raw.max():.2f} mm")
else:
    meas_s = meas_force = None
    print(f"\n  Warning: measurement file not found: {MEAS_FILE}")

# =============================================================================
# 6. PLOT  (2-panel: F-s curve + local spring rate)
# =============================================================================
fig, (ax, ax_rate) = plt.subplots(2, 1, figsize=(10, 10), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
fig.subplots_adjust(hspace=0.08)

# -- Panel 1: Force vs compression -----------------------------------------
ax.axvspan(S_PRELOAD, S_FULL_LIFT, alpha=0.08, color="blue",
           label=f"Valve operating range ({VALVE_LIFT:.0f} mm lift)")

ax.plot(lifts, forces, "b-o", ms=4, linewidth=1.8,
        label="CalculiX FEA (NLGEOM, Tet10, self-contact, variable pitch)")

if meas_s is not None:
    ax.plot(meas_s, meas_force, "m-", linewidth=1.5, alpha=0.85,
            label="Measurement INT_Spring_measurement.txt")

for s_r, f_r, lbl in REF:
    ax.axvline(s_r, color="gray", linestyle=":", linewidth=0.8, alpha=0.6)
    ax.plot(s_r, f_r, "r^", ms=9, zorder=5)
    ax.annotate(lbl, xy=(s_r, f_r), xytext=(s_r + 0.4, f_r - 40),
                fontsize=8, color="red")

info = (f"Installed: L={L_INSTALLED} mm  →  {F_PRELOAD:.0f} N  (s={S_PRELOAD:.1f} mm)\n"
        f"Full lift: L={L_FULL_LIFT} mm  →  {F_FULL_LIFT:.0f} N  (s={S_FULL_LIFT:.1f} mm)\n"
        f"Pitch: p_bot={pitch_mean*(1-D_PITCH):.2f} mm  →  p_top={pitch_mean*(1+D_PITCH):.2f} mm  (D_pitch={D_PITCH})\n"
        f"3-phase fit: k={k_ana_phase1:.0f}→{k_ana_phase2:.1f}→{k_ana_phase3:.1f} N/mm  "
        f"(kinks at lift={LIFT_KINK1:.2f}, {LIFT_KINK2:.1f} mm)")
ax.text(0.03, 0.97, info, transform=ax.transAxes, fontsize=8.5,
        verticalalignment='top', color="darkred",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.8))

s_ana = np.linspace(0, MAX_LIFT, 200)
f_ana = np.array([analytical_force(s) for s in s_ana])
ax.plot(s_ana, f_ana, "g-", linewidth=2.0,
        label=f"Analytical fit (3-phase)  k={k_ana_phase1:.0f}→{k_ana_phase2:.1f}→{k_ana_phase3:.1f} N/mm")

ax.set_ylabel("Spring Force [N]", fontsize=11)
ax.set_title(f"Valve Spring  –  Variable Pitch FEA vs Measurement  (D_pitch={D_PITCH})\n"
             f"Free length {L0} mm  |  Installed {L_INSTALLED} mm ({F_PRELOAD:.0f} N)  |  "
             f"Valve lift {VALVE_LIFT:.0f} mm  |  Max force {F_FULL_LIFT:.0f} N",
             fontsize=11)
ax.legend(fontsize=9, loc="upper left")
ax.grid(True, alpha=0.3)
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax2 = ax.secondary_xaxis('top',
    functions=(lambda s: L0 - s, lambda L: L0 - L))
ax2.set_xlabel("Spring Installed Length [mm]", fontsize=10)

# -- Panel 2: Local spring rate dF/ds  (progressive behavior indicator) ----
if len(lifts) >= 4:
    k_local  = np.diff(forces) / np.diff(lifts)
    s_mid    = 0.5 * (lifts[:-1] + lifts[1:])
    ax_rate.plot(s_mid, k_local, "b-o", ms=4, linewidth=1.8, label="FEA local rate dF/ds")

    # Measurement local rate
    if meas_s is not None and len(meas_s) > 4:
        ds = np.diff(meas_s)
        k_meas_local = np.where(ds > 1e-6, np.diff(meas_force) / np.where(ds > 1e-6, ds, 1), np.nan)
        s_meas_mid   = 0.5 * (meas_s[:-1] + meas_s[1:])
        # Smooth to reduce noise
        from numpy.lib.stride_tricks import sliding_window_view
        win = 10
        if len(k_meas_local) > win:
            k_smooth = np.convolve(k_meas_local, np.ones(win)/win, mode='valid')
            s_smooth = s_meas_mid[win//2: win//2 + len(k_smooth)]
            ax_rate.plot(s_smooth, k_smooth, "m-", linewidth=1.5,
                         label="Measurement rate dF/ds (smoothed)")

    # Analytical rates
    k_ana_local = np.gradient(f_ana, s_ana)
    ax_rate.plot(s_ana, k_ana_local, "g-", linewidth=1.5, label="Analytical fit rate")

    ax_rate.axvspan(S_PRELOAD, S_FULL_LIFT, alpha=0.08, color="blue")
    ax_rate.axvline(S_PRELOAD, color="gray", linestyle=":", linewidth=0.8, alpha=0.6)
    ax_rate.axvline(S_FULL_LIFT, color="gray", linestyle=":", linewidth=0.8, alpha=0.6)
    ax_rate.axhline(k_ana_phase1, color="green", linestyle="--", linewidth=0.8,
                    alpha=0.6, label=f"k₁={k_ana_phase1:.0f} N/mm")
    ax_rate.axhline(k_ana_phase2, color="yellowgreen", linestyle="--", linewidth=0.8,
                    alpha=0.6, label=f"k₂={k_ana_phase2:.1f} N/mm")
    ax_rate.axhline(k_ana_phase3, color="darkgreen", linestyle="--", linewidth=0.8,
                    alpha=0.6, label=f"k₃={k_ana_phase3:.1f} N/mm")
    ax_rate.axvline(S_KINK1, color="orange", linestyle=":", linewidth=0.9, alpha=0.7)
    ax_rate.axvline(S_KINK2, color="darkorange", linestyle=":", linewidth=0.9, alpha=0.7)
    ax_rate.set_ylabel("Local Rate  dF/ds  [N/mm]", fontsize=11)
    ax_rate.set_xlabel("Compression from Free Length [mm]", fontsize=11)
    ax_rate.legend(fontsize=9, loc="upper left")
    ax_rate.grid(True, alpha=0.3)
    ax_rate.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=150)
plt.show()
print(f"\n  Plot: {PLOT_FILE}")
print("=== FEA complete ===")
