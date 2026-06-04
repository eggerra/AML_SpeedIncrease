"""
spring_analysis.py  -  Valve spring FEA: Force vs Lift

Reads ValveSpring_mesh.inp (exported by mesh_spring.py),
identifies top/bottom face nodes, writes a CalculiX input file,
runs the solver, parses reaction forces, and plots the F-L characteristic.

Prerequisite:  run mesh_spring.py first.
"""
import re, os, sys, subprocess
import numpy as np
import matplotlib.pyplot as plt

# -- Paths ---------------------------------------------------------------------
BASE      = r"D:\Projects_AI\AML_SpeedIncrease"
MESH_INP  = os.path.join(BASE, "ValveSpring_mesh.inp")
FULL_INP  = os.path.join(BASE, "ValveSpring_fea.inp")
JOB       = "ValveSpring_fea"
DAT_FILE  = os.path.join(BASE, JOB + ".dat")
PLOT_FILE = os.path.join(BASE, "spring_FvL.png")

# CalculiX executable bundled with FreeCAD 1.1
CCX_CANDIDATES = [
    r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\ccx.exe",
    r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\ccx_dynamic.exe",
    "ccx",
]

# -- Spring geometry (drawing A177 053 05 00) ----------------------------------
L0      = 46.1
grind_z = 0.75
Z_BOT   = grind_z           # 0.75 mm
Z_TOP   = L0 - grind_z     # 45.35 mm
Z_TOL   = 0.40              # node selection tolerance [mm]
MAX_LIFT = 20.0             # max compression to simulate [mm]

# Material: VD SiCrNi SC  (G = 79500 N/mm2 -> E = 2G(1+nu) = 206700 ~ 206000)
E_MOD = 206000.0
NU    = 0.30

# Drawing reference points for verification
REF = [(10.0, 250.0, "F1 = 250 N @ L1"), (20.0, 620.0, "F2 = 620 N @ L2")]

# -- Analytical progressive spring rate model ----------------------------------
# Beehive spring with variable pitch: top/small-OD coils bind first.
# Drawing data (A177 053 05 00):
#   na at L1 (s=10mm) = 4.4 active coils  -> 1.7 of 6.1 coils have bound
#   na at L2 (s=20mm) = 3.1 active coils  -> 1.3 more bind between L1 and L2
#
# Two-phase piecewise linear model calibrated directly to drawing references:
#   Phase 1 (0 to s1=10mm):  secant k = F1/s1 = 250/10 = 25 N/mm  (6.1 active)
#   Phase 2 (s1 to s2=20mm): secant k = (F2-F1)/(s2-s1) = 37 N/mm (4.4->3.1)
# This exactly reproduces F1=250N and F2=620N by construction.
#
# Note: the FEA (solid elastic, no contact) gives the LINEAR elastic rate
# with all 8.6 coils contributing.  The analytical model captures the
# progressive stiffening from coil binding that the solid FEA cannot.

k_ana_phase1 = (REF[0][1]) / (REF[0][0])               # 250/10 = 25 N/mm
k_ana_phase2 = (REF[1][1] - REF[0][1]) / (REF[1][0] - REF[0][0])   # 37 N/mm
s_ana_break  = REF[0][0]   # 10 mm

na_phase1 = 6.1   # total active coils at free length
na_phase2 = 4.4   # drawing: active at L1
na_phase3 = 3.1   # drawing: active at L2

def analytical_force(s):
    """Progressive spring force [N] at compression s [mm].
    Calibrated to drawing: F(10)=250N, F(20)=620N."""
    if s <= 0:
        return 0.0
    elif s <= s_ana_break:
        return k_ana_phase1 * s
    else:
        return REF[0][1] + k_ana_phase2 * (s - s_ana_break)

print(f"\n  Analytical model (calibrated to drawing, 2-phase progressive):")
print(f"    Phase 1:  na={na_phase1}  k={k_ana_phase1:.1f} N/mm  (0 -> {s_ana_break:.0f} mm)")
print(f"    Phase 2:  na={na_phase2}->{na_phase3}  k={k_ana_phase2:.1f} N/mm  ({s_ana_break:.0f} -> {MAX_LIFT:.0f} mm)")
print(f"    F1 @ 10mm = {analytical_force(10):.0f} N  (dwg: 250 N)  CHECK")
print(f"    F2 @ 20mm = {analytical_force(20):.0f} N  (dwg: 620 N)  CHECK")

# =============================================================================
# 1. PARSE MESH  (FreeCAD FemMesh.write() -> CalculiX/Abaqus .inp format)
# =============================================================================
def parse_mesh(path):
    """Return nodes {id:(x,y,z)} and the C3D10 element set name."""
    nodes = {}
    elset = "Evolumes"
    mode  = None

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
    return nodes, elset


print("=== Spring FEA - Force vs Lift ===")
if not os.path.isfile(MESH_INP):
    sys.exit(f"ERROR: mesh not found: {MESH_INP}\n  Run mesh_spring.py first.")

print(f"  Parsing: {MESH_INP}")
nodes, elset = parse_mesh(MESH_INP)
print(f"  Nodes      : {len(nodes):,}")
print(f"  Element set: {elset}")

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
    f.write("** ValveSpring FEA - Force vs Lift\n")
    f.write(f"** Material: VD SiCrNi SC  E={E_MOD} MPa  nu={NU}\n")
    f.write(f"** Compression ramp 0 -> {MAX_LIFT} mm  (1 mm increments)\n**\n")

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

    # Step: nonlinear static, time = lift in mm
    f.write("*STEP, NLGEOM, INC=200\n")
    f.write(f"*STATIC\n1.0, {MAX_LIFT:.1f}, 0.1, 1.0\n**\n")

    # Boundary conditions
    f.write("** Bottom face: fully fixed\n*BOUNDARY\nNBOT, 1, 3, 0.0\n")
    f.write("** Top face: X/Y fixed, Z compressed\nNTOP, 1, 2, 0.0\n")
    f.write(f"NTOP, 3, 3, -{MAX_LIFT:.1f}\n**\n")

    # Output: individual node RF at bottom (sum in post-processing), every step
    f.write("*NODE PRINT, NSET=NBOT, TOTALS=YES, FREQUENCY=1\nRF\n")
    # Displacement + stress fields for visualisation (every 5 mm)
    f.write("*NODE FILE, FREQUENCY=5\nU\n")
    f.write("*EL FILE, FREQUENCY=5\nS\n**\n")

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
# .dat format with TOTALS=YES per increment (time = lift in mm):
#
#   forces (reactions) for set NBOT and time  T
#       nid     rf1          rf2          rf3
#         1   0.00E+00    0.00E+00    -1.23E+01
#         ...
#    total   0.00E+00    0.00E+00    -2.50E+02
#
# Strategy: sum all RF3 values in each time block (robust regardless of
# whether "total" line format varies between CalculiX versions).

if not os.path.isfile(DAT_FILE):
    sys.exit(f"Result file not found: {DAT_FILE}")

print(f"\n  Parsing: {DAT_FILE}")

time_re  = re.compile(r"forces.*?time\s+([\d.E+\-]+)", re.IGNORECASE)
node_rf_re = re.compile(
    r"^\s+(\d+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)"
)

lifts, forces = [], []
cur_time  = None
cur_rf3   = 0.0
node_count = 0

with open(DAT_FILE) as f:
    for line in f:
        m = time_re.search(line)
        if m:
            # Save previous block
            if cur_time is not None and node_count > 0:
                lifts.append(cur_time)
                forces.append(abs(cur_rf3))
            cur_time  = float(m.group(1))
            cur_rf3   = 0.0
            node_count = 0
            continue

        if cur_time is not None:
            m2 = node_rf_re.match(line)
            if m2:
                cur_rf3   += float(m2.group(4))
                node_count += 1

# Save last block
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
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(lifts, forces, "b-o", ms=4, linewidth=1.8, label="CalculiX FEA (NLGEOM, Tet10)")

for lift_r, force_r, lbl in REF:
    ax.axvline(lift_r, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.plot(lift_r, force_r, "r^", ms=9, zorder=5)
    ax.annotate(lbl, xy=(lift_r, force_r), xytext=(lift_r+0.4, force_r-35),
                fontsize=8, color="red")

k_dwg = (REF[1][1] - REF[0][1]) / (REF[1][0] - REF[0][0])
ax.text(0.04, 0.93, f"Drawing rate (F1->F2): {k_dwg:.0f} N/mm",
        transform=ax.transAxes, fontsize=9, color="red")

if len(lifts) >= 4:
    k_coeff = np.polyfit(lifts, forces, 1)
    k_fea   = k_coeff[0]
    ax.plot(lifts, np.polyval(k_coeff, lifts), "b--",
            alpha=0.5, linewidth=1, label=f"Linear fit k = {k_fea:.1f} N/mm")
    ax.text(0.04, 0.86, f"FEA rate (linear fit): {k_fea:.0f} N/mm",
            transform=ax.transAxes, fontsize=9, color="blue")

# Analytical progressive spring rate
s_ana = np.linspace(0, MAX_LIFT, 200)
f_ana = np.array([analytical_force(s) for s in s_ana])
ax.plot(s_ana, f_ana, "g-", linewidth=2.0,
        label=f"Analytical progressive (na: {na_phase1}->{na_phase2}->{na_phase3} coils)")
ax.text(0.04, 0.79,
        f"Analytical: k={k_ana_phase1:.0f} N/mm -> {k_ana_phase2:.0f} N/mm (binding at s={s_ana_break:.0f} mm)",
        transform=ax.transAxes, fontsize=9, color="green")

ax.set_xlabel("Spring Lift / Compression [mm]", fontsize=11)
ax.set_ylabel("Spring Force [N]", fontsize=11)
ax.set_title("Valve Spring A177 053 05 00 - Force vs Lift (FEA)", fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=150)
plt.show()
print(f"\n  Plot: {PLOT_FILE}")
print("=== FEA complete ===")
