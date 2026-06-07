"""
spring_analysis.py  -  Valve spring FEA: Preload + Valve Lift  (2-step, self-contact)

Operating conditions (drawing A177 053 05 00):
  Step 1 - Assembly preload : compress free length 46.1 mm -> installed 36.1 mm
                               compression s1 = 10 mm,  F_preload = 250 N
  Step 2 - Valve lift       : additional 10 mm compression (36.1 -> 26.1 mm)
                               total compression s2 = 20 mm,  F_max = 620 N

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
MESH_INP  = os.path.join(BASE, "ValveSpring_mesh.inp")
FULL_INP  = os.path.join(BASE, "ValveSpring_contact.inp")
JOB       = "ValveSpring_contact"
DAT_FILE  = os.path.join(BASE, JOB + ".dat")
PLOT_FILE = os.path.join(BASE, "spring_FvL.png")

# CalculiX executable bundled with FreeCAD 1.1
CCX_CANDIDATES = [
    r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\ccx.exe",
    r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\ccx_dynamic.exe",
    "ccx",
]

# -- Spring geometry (drawing A177 053 05 00) ----------------------------------
L0      = 46.1    # free length [mm]
grind_z = 0.75
Z_BOT   = grind_z           # 0.75 mm
Z_TOP   = L0 - grind_z     # 45.35 mm
Z_TOL   = 0.40              # node selection tolerance [mm]

# Contact surface: active coil zone only (exclude closed/ground end coils)
# Closed ends: n_closed=1.25 coils * wire_a=2.92mm = 3.65 mm each end
N_CLOSED = 1.25
WIRE_A   = 2.92
H_CLOSED = N_CLOSED * WIRE_A                 # 3.65 mm per dead end
Z_CONTACT_BOT = H_CLOSED + 0.5              # 4.15 mm — small buffer above ground end
Z_CONTACT_TOP = L0 - H_CLOSED - 0.5        # 41.95 mm — small buffer below top end

# -- Operating conditions (engine assembly) ------------------------------------
L_INSTALLED = 36.1    # installed / preload length [mm]
F_PRELOAD   = 250.0   # preload force at installed length [N]
VALVE_LIFT  = 10.0    # valve lift stroke [mm]
L_FULL_LIFT = L_INSTALLED - VALVE_LIFT  # 26.1 mm  (spring length at full lift)
F_FULL_LIFT = 620.0   # spring force at full valve lift [N]

S_PRELOAD   = L0 - L_INSTALLED   # 10 mm compression -> preload
S_FULL_LIFT = L0 - L_FULL_LIFT   # 20 mm compression -> full lift
MAX_LIFT    = S_FULL_LIFT        # total simulation range [mm]

# Material: VD SiCrNi SC  (G = 79500 N/mm2 -> E = 2G(1+nu) = 206700 ~ 206000)
E_MOD = 206000.0
NU    = 0.30

# Drawing reference points for verification
REF = [
    (S_PRELOAD,   F_PRELOAD,   f"Preload: {F_PRELOAD:.0f} N  (L={L_INSTALLED} mm)"),
    (S_FULL_LIFT, F_FULL_LIFT, f"Full lift: {F_FULL_LIFT:.0f} N  (L={L_FULL_LIFT} mm)"),
]

# -- Analytical progressive spring rate model ----------------------------------
# Beehive spring with variable pitch: bottom/large-OD coils bind first.
# As large-OD coils go inactive, remaining active coils are the stiffer small-OD
# top coils -> spring rate increases (progressive behaviour).
# Drawing data (A177 053 05 00):
#   na at L1 (s=10mm) = 4.4 active coils  -> 1.7 of 6.1 coils have bound
#   na at L2 (s=20mm) = 3.1 active coils  -> 1.3 more bind between L1 and L2
#
# Two-phase piecewise linear model calibrated directly to drawing references:
#   Phase 1 (0 -> 10mm): secant k = 250/10 = 25 N/mm  (6.1 active coils)
#   Phase 2 (10 -> 20mm): secant k = (620-250)/10 = 37 N/mm  (4.4 -> 3.1 active)

k_ana_phase1 = F_PRELOAD / S_PRELOAD                          # 25 N/mm
k_ana_phase2 = (F_FULL_LIFT - F_PRELOAD) / VALVE_LIFT        # 37 N/mm
s_ana_break  = S_PRELOAD                                      # 10 mm

na_phase1 = 6.1   # total active coils at free length
na_phase2 = 4.4   # drawing: active at preload (L=36.1mm)
na_phase3 = 3.1   # drawing: active at full lift (L=26.1mm)

def analytical_force(s):
    """Progressive spring force [N] at compression s [mm]."""
    if s <= 0:
        return 0.0
    elif s <= s_ana_break:
        return k_ana_phase1 * s
    else:
        return F_PRELOAD + k_ana_phase2 * (s - s_ana_break)

print(f"\n  Operating conditions (drawing A177 053 05 00):")
print(f"    Free length      : {L0} mm")
print(f"    Installed length : {L_INSTALLED} mm  (s={S_PRELOAD:.0f} mm compression)")
print(f"    Preload force    : {F_PRELOAD:.0f} N")
print(f"    Valve lift       : {VALVE_LIFT:.0f} mm")
print(f"    Length @ full lift: {L_FULL_LIFT} mm  (s={S_FULL_LIFT:.0f} mm compression)")
print(f"    Force @ full lift : {F_FULL_LIFT:.0f} N")
print(f"\n  Analytical model (2-phase progressive):")
print(f"    Phase 1:  na={na_phase1}  k={k_ana_phase1:.1f} N/mm  (0 -> {s_ana_break:.0f} mm)")
print(f"    Phase 2:  na={na_phase2}->{na_phase3}  k={k_ana_phase2:.1f} N/mm  ({s_ana_break:.0f} -> {MAX_LIFT:.0f} mm)")
print(f"    F @ preload  = {analytical_force(S_PRELOAD):.0f} N  (dwg: {F_PRELOAD:.0f} N)  CHECK")
print(f"    F @ full lift = {analytical_force(S_FULL_LIFT):.0f} N  (dwg: {F_FULL_LIFT:.0f} N)  CHECK")

# =============================================================================
# 1. PARSE MESH  (FreeCAD FemMesh.write() -> CalculiX/Abaqus .inp format)
# =============================================================================
def parse_mesh(path):
    """Return nodes {id:(x,y,z)}, elements {id:[n1..n10]}, and C3D10 elset name."""
    nodes    = {}
    elements = {}  # {elem_id: [n1, n2, n3, n4, ...]} (corner nodes first)
    elset    = "Evolumes"
    mode     = None
    pending  = None   # for elements that span two lines

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
                        # First line: element id + up to 9 nodes (C3D10 often split)
                        eid  = int(parts[0])
                        nids = [int(p) for p in parts[1:] if p]
                        if len(nids) >= 10:
                            elements[eid] = nids[:10]
                        else:
                            pending = (eid, nids)   # wait for continuation line
                    else:
                        # Continuation line
                        eid, nids = pending
                        nids += [int(p) for p in parts if p]
                        if len(nids) >= 10:
                            elements[eid] = nids[:10]
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

    # Solid section (C3D10 elements)
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
    # LINEAR overclosure: penalty K = 10000 N/mm^3 (~5% of E/element_size).
    # HARD contact defaults to 10.3e6 N/mm^3 which causes chattering; this is
    # deliberately softer to ensure convergence while still capturing coil contact.
    f.write("*SURFACE BEHAVIOR, PRESSURE-OVERCLOSURE=LINEAR\n1000.\n**\n")

    # ---- Step 1: Assembly preload (free length -> installed length) ----
    # Compress from 0 to S_PRELOAD (10 mm) to establish 250 N preload.
    # Coarser increments are acceptable here; contact not yet active.
    f.write(f"** Step 1: Assembly preload  0 -> {S_PRELOAD:.1f} mm  ({L0} mm -> {L_INSTALLED} mm)\n")
    f.write("*STEP, NLGEOM, INC=500\n")
    f.write(f"*STATIC\n0.5, {S_PRELOAD:.1f}, 0.05, 1.0\n**\n")
    f.write("** Bottom face: fully fixed\n*BOUNDARY\nNBOT, 1, 3, 0.0\n")
    f.write("** Top face: X/Y fixed, Z compressed to preload\nNTOP, 1, 2, 0.0\n")
    f.write(f"NTOP, 3, 3, -{S_PRELOAD:.1f}\n**\n")
    f.write("*NODE PRINT, NSET=NBOT, TOTALS=YES, FREQUENCY=1\nRF\n")
    f.write("*NODE FILE, FREQUENCY=5\nU\n")
    f.write("*EL FILE, FREQUENCY=5\nS\n")
    f.write("*CONTACT FILE, FREQUENCY=5\nCSTRESS, CDISP\n**\n")
    f.write("*END STEP\n**\n")

    # ---- Step 2: Valve lift (installed length -> full lift) ----
    # Continue from preloaded state, compress additional VALVE_LIFT (10 mm).
    # Finer increments to resolve progressive stiffening from coil contact.
    f.write(f"** Step 2: Valve lift  {S_PRELOAD:.1f} -> {S_FULL_LIFT:.1f} mm  ({L_INSTALLED} mm -> {L_FULL_LIFT} mm)\n")
    f.write("*STEP, NLGEOM, INC=1000\n")
    f.write(f"*STATIC\n0.1, {VALVE_LIFT:.1f}, 0.005, 0.5\n**\n")
    # OP=NEW resets BC; total displacement = S_FULL_LIFT from original free-length position
    f.write("*BOUNDARY, OP=NEW\n")
    f.write("NBOT, 1, 3, 0.0\n")
    f.write("NTOP, 1, 2, 0.0\n")
    f.write(f"NTOP, 3, 3, -{S_FULL_LIFT:.1f}\n**\n")
    f.write("*NODE PRINT, NSET=NBOT, TOTALS=YES, FREQUENCY=1\nRF\n")
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

ccx = find_ccx()
if ccx is None:
    print("\nCalculiX not found. Searched:")
    for p in CCX_CANDIDATES: print(f"  {p}")
    print(f'\nRun manually:  cd "{BASE}" && ccx {JOB}')
    sys.exit(0)

print(f"\n  CalculiX: {ccx}")
print(f"  Job     : {JOB}")
print("  Running... (may take several minutes)")

proc = subprocess.run([ccx, JOB], cwd=BASE, timeout=7200)
if proc.returncode != 0:
    sys.exit(f"CalculiX exited with code {proc.returncode}")
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

time_re    = re.compile(r"forces.*?time\s+([\d.E+\-]+)", re.IGNORECASE)
node_rf_re = re.compile(
    r"^\s+(\d+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)"
)

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
# 5. PLOT
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

# Shade the actual valve operating range (Step 2: preload -> full lift)
ax.axvspan(S_PRELOAD, S_FULL_LIFT, alpha=0.08, color="blue",
           label=f"Valve operating range ({VALVE_LIFT:.0f} mm lift)")

ax.plot(lifts, forces, "b-o", ms=4, linewidth=1.8,
        label="CalculiX FEA (NLGEOM, Tet10, self-contact)")

# Reference markers: preload and full-lift operating points
for s_r, f_r, lbl in REF:
    ax.axvline(s_r, color="gray", linestyle=":", linewidth=0.8, alpha=0.6)
    ax.plot(s_r, f_r, "r^", ms=9, zorder=5)
    ax.annotate(lbl, xy=(s_r, f_r), xytext=(s_r + 0.4, f_r - 40),
                fontsize=8, color="red")

# Operating condition summary box
info = (f"Preload:   L={L_INSTALLED} mm  →  {F_PRELOAD:.0f} N  (s={S_PRELOAD:.0f} mm)\n"
        f"Full lift: L={L_FULL_LIFT} mm  →  {F_FULL_LIFT:.0f} N  (s={S_FULL_LIFT:.0f} mm)\n"
        f"Valve lift stroke: {VALVE_LIFT:.0f} mm")
ax.text(0.03, 0.97, info, transform=ax.transAxes, fontsize=8.5,
        verticalalignment='top', color="darkred",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.8))

# FEA linear fit over operating range only (Step 2 data)
op_mask = (np.array(lifts) >= S_PRELOAD)
if op_mask.sum() >= 3:
    l_op = np.array(lifts)[op_mask]
    f_op = np.array(forces)[op_mask]
    k_coeff = np.polyfit(l_op, f_op, 1)
    k_fea   = k_coeff[0]
    ax.plot(l_op, np.polyval(k_coeff, l_op), "b--",
            alpha=0.5, linewidth=1, label=f"FEA linear fit (operating range) k={k_fea:.1f} N/mm")
    ax.text(0.55, 0.12, f"FEA rate (operating range): {k_fea:.0f} N/mm",
            transform=ax.transAxes, fontsize=9, color="blue")
elif len(lifts) >= 4:
    k_coeff = np.polyfit(lifts, forces, 1)
    k_fea   = k_coeff[0]
    ax.plot(lifts, np.polyval(k_coeff, lifts), "b--",
            alpha=0.5, linewidth=1, label=f"FEA linear fit k={k_fea:.1f} N/mm")

# Analytical progressive spring rate
s_ana = np.linspace(0, MAX_LIFT, 200)
f_ana = np.array([analytical_force(s) for s in s_ana])
ax.plot(s_ana, f_ana, "g-", linewidth=2.0,
        label=f"Analytical progressive (na: {na_phase1}->{na_phase2}->{na_phase3} coils)")
ax.text(0.55, 0.06,
        f"Analytical: k={k_ana_phase1:.0f} N/mm → {k_ana_phase2:.0f} N/mm (binding at s={s_ana_break:.0f} mm)",
        transform=ax.transAxes, fontsize=9, color="green")

ax.set_xlabel("Compression from Free Length [mm]", fontsize=11)
ax.set_ylabel("Spring Force [N]", fontsize=11)
ax.set_title(f"Valve Spring A177 053 05 00  –  Preload + Valve Lift FEA\n"
             f"Free length {L0} mm  |  Installed {L_INSTALLED} mm ({F_PRELOAD:.0f} N)  |  "
             f"Valve lift {VALVE_LIFT:.0f} mm  |  Max force {F_FULL_LIFT:.0f} N",
             fontsize=11)
ax.legend(fontsize=9, loc="upper left")
ax.grid(True, alpha=0.3)
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

# Secondary x-axis: installed spring length
ax2 = ax.secondary_xaxis('top',
    functions=(lambda s: L0 - s, lambda L: L0 - L))
ax2.set_xlabel("Spring Installed Length [mm]", fontsize=10)

plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=150)
plt.show()
print(f"\n  Plot: {PLOT_FILE}")
print("=== FEA complete ===")
