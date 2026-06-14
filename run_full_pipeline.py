"""
run_full_pipeline.py
====================
Full valve-spring FEA pipeline: CAD → mesh → Abaqus/Standard solve.

Fix applied (2026-06-14):
  n_closed=1.25 (drawing value, replaces calibrated 2.026).
  With n_closed=2.026 the spring had only 4.548 active coils and went solid at
  s≈14 mm causing force spikes to 3400–5900 N (target F2=621 N at s=17.1 mm).
  With n_closed=1.25: n_active=6.1, spring stays progressive through full lift.
  D_pitch recalculated to 0.0776 (from 0.0907) to keep kink1 at lift=4.05 mm.
  Contact tightened: EXPONENTIAL c0=0.01 mm (from 0.1 mm) to reduce penetration.

Steps
-----
1. Generate oval STEP geometry  (FreeCADCmd + generate_spring.py)
2. Mesh oval STEP               (FreeCADCmd + mesh_spring.py)
3. Write CalculiX/Abaqus INP   (spring_analysis.py — writes INP, may run CCX)
4. Run Abaqus/Standard solve    (run_abaqus.py — converts INP, runs Abaqus, plots)
5. Update simulation_log.md
6. Git commit + push

Usage
-----
    python run_full_pipeline.py
"""
import os, sys, subprocess, time, datetime

BASE    = r"D:\Projects_AI\AML_SpeedIncrease"
FREECAD = r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\FreeCADCmd.exe"

OVAL_STEP  = os.path.join(BASE, "ValveSpring_oval.step")
OVAL_MESH  = os.path.join(BASE, "ValveSpring_oval_mesh.inp")
OVAL_FCSTD = os.path.join(BASE, "ValveSpring_oval_meshed.FCStd")
OVAL_JOB   = "ValveSpring_oval_contact"
OVAL_INP   = os.path.join(BASE, OVAL_JOB + ".inp")          # CalculiX INP
ABQ_JOB    = "ValveSpring_oval_contact_abaqus"
ABQ_INP    = os.path.join(BASE, ABQ_JOB + ".inp")           # Abaqus INP
ABQ_RF     = os.path.join(BASE, ABQ_JOB + "_rf.txt")
PLOT_FILE  = os.path.join(BASE, "spring_FvL_abaqus.png")
SIM_LOG    = os.path.join(BASE, "simulation_log.md")


def run(cmd, env=None, desc=""):
    label = desc or " ".join(str(c) for c in cmd)
    print(f"\n--- {label} ---")
    t0 = time.time()
    merged = {**os.environ, **(env or {})}
    r = subprocess.run(cmd, env=merged, cwd=BASE)
    elapsed = time.time() - t0
    if r.returncode != 0:
        sys.exit(f"ERROR: command failed (code {r.returncode})  [{elapsed:.0f}s]  —  {label}")
    print(f"  done in {elapsed:.0f}s")
    return elapsed


def update_log(stage, status, extra=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n## {now}  —  {stage}\n"
        f"**Status:** {status}\n"
    )
    if extra:
        entry += f"{extra}\n"
    with open(SIM_LOG, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  [simulation_log] {stage}: {status}")



# =============================================================================
# Initialise log for this run
# =============================================================================
with open(SIM_LOG, "w", encoding="utf-8") as f:
    f.write(
        f"# Simulation Run Log — {ABQ_JOB}\n\n"
        f"**Run started:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"**Job:** {ABQ_JOB}\n\n"
        f"## Change applied\n"
        f"- `L0`:       38.717 → 46.1 mm (drawing value restored)\n"
        f"- `L0_oval`:  39.182 → 46.565 mm (38.8 + 2×1.25×3.106)\n"
        f"- `D_pitch`:  0.0776 → 0.0629 (kink1 preserved at lift=4.05 mm; s_bind=18.55 mm)\n"
        f"- `n_closed`: 1.25 (drawing, unchanged)\n\n"
        f"## Progress\n"
    )

# =============================================================================
# 1. Generate oval STEP geometry
# =============================================================================
update_log("CAD generation", "RUNNING")
run(
    [FREECAD, os.path.join(BASE, "generate_spring.py")],
    env={"SPRING_PROFILE": "oval"},
    desc="Generate oval STEP (n_closed=1.25, L0=46.1, D_pitch=0.0629)",
)
if not os.path.isfile(OVAL_STEP):
    update_log("CAD generation", "FAILED — STEP file not created")
    sys.exit(f"ERROR: STEP not created: {OVAL_STEP}")
sz = os.path.getsize(OVAL_STEP) // 1024
update_log("CAD generation", f"DONE — {OVAL_STEP} ({sz} kB)")

# =============================================================================
# 2. Mesh oval STEP
# =============================================================================
update_log("Meshing", "RUNNING — maxh=1.0 mm, Netgen (may take 5-15 min)")
run(
    [FREECAD, os.path.join(BASE, "mesh_netgen.py")],
    env={
        "SPRING_STEP":     OVAL_STEP,
        "SPRING_MESH_OUT": OVAL_MESH,
        "SPRING_MAXH":     "1.0",
    },
    desc="Mesh oval STEP (Netgen maxh=1.0 mm)",
)
if not os.path.isfile(OVAL_MESH):
    update_log("Meshing", "FAILED — mesh file not created")
    sys.exit(f"ERROR: mesh not created: {OVAL_MESH}")
sz = os.path.getsize(OVAL_MESH) // (1024 * 1024)
update_log("Meshing", f"DONE — {OVAL_MESH} ({sz} MB)")

# =============================================================================
# 3. Write FEA input file (spring_analysis.py)
#    Also runs CalculiX if available; we need the .inp regardless.
# =============================================================================
update_log("FEA input", "RUNNING — writing Abaqus/CalculiX INP")
run(
    [sys.executable, os.path.join(BASE, "spring_analysis.py")],
    env={
        "SPRING_MESH_INP": OVAL_MESH,
        "SPRING_JOB":      OVAL_JOB,
        "SPRING_PLOT":     os.path.join(BASE, "spring_FvL_ccx.png"),
        "SPRING_L0":       "46.565",   # oval L0: 38.8 + 2*1.25*3.106 (drawing L0=46.1)
        "SPRING_WIRE_A":   "3.106",    # oval wire eff. axial extent (c=0.1)
    },
    desc="Write FEA INP (spring_analysis.py)",
)
if not os.path.isfile(OVAL_INP):
    update_log("FEA input", "FAILED — INP not created")
    sys.exit(f"ERROR: INP not created: {OVAL_INP}")
sz = os.path.getsize(OVAL_INP) // 1024
update_log("FEA input", f"DONE — {OVAL_INP} ({sz} kB)")

# =============================================================================
# 4. Run Abaqus/Standard solve
#    run_abaqus.py converts INP to Abaqus format, runs solver, extracts RF, plots.
# =============================================================================
update_log("Abaqus solve", "RUNNING — this typically takes 10-20 hours")
t_abq_start = time.time()
run(
    [sys.executable, os.path.join(BASE, "run_abaqus.py"), "16"],
    desc="Abaqus/Standard solve + postprocess (16 cpus)",
)
elapsed_abq = time.time() - t_abq_start

if os.path.isfile(ABQ_RF):
    with open(ABQ_RF) as fh:
        lines = [l for l in fh if not l.startswith("#")]
    npts = len(lines)
    forces = [abs(float(l.split()[1])) for l in lines if len(l.split()) >= 2]
    fmin = min(forces) if forces else 0
    fmax = max(forces) if forces else 0
    update_log(
        "Abaqus solve",
        f"COMPLETED — {npts} result points  F={fmin:.0f}–{fmax:.0f} N  "
        f"wall={elapsed_abq/3600:.1f}h",
    )
else:
    update_log("Abaqus solve", f"COMPLETED (no RF file found)  wall={elapsed_abq/3600:.1f}h")

# =============================================================================
# 5. Final simulation log entry
# =============================================================================
with open(SIM_LOG, "a", encoding="utf-8") as f:
    f.write(
        f"\n## Summary\n"
        f"- Total wall time: {(time.time()-t_abq_start)/3600:.1f}h (Abaqus only)\n"
        f"- Plot: {PLOT_FILE}\n"
        f"- RF data: {ABQ_RF}\n"
    )

# =============================================================================
# 6. Git commit + push
# =============================================================================
files_to_stage = [
    "generate_spring.py",
    "spring_analysis.py",
    "run_abaqus.py",
    "run_oval_pipeline.py",
    "run_full_pipeline.py",
    "simulation_log.md",
    "spring_FvL_abaqus.png",
    "ValveSpring_oval_contact_abaqus_rf.txt",
    "README.md",
    "AML_Valvetrain_Model_Analysis.md",
]
subprocess.run(["git", "-C", BASE, "add"] + files_to_stage, check=False)
commit_msg = (
    "feat: drawing L0=46.1 mm, fix contact blowup, switch to Netgen mesher\n\n"
    "- L0 38.717->46.1 mm (drawing value; was calibrated to measured spring)\n"
    "- L0_oval 39.182->46.565 mm: 38.8 + 2*1.25*3.106 mm\n"
    "- D_pitch 0.0776->0.0629: kink1 preserved at lift=4.05 mm (s_bind=18.55 mm)\n"
    "- Contact EXPONENTIAL c0 0.01->0.1 mm: fixes force blowup at s~14 mm\n"
    "  (c0=0.01 gave p=2202 N/mm2 at 0.1 mm overclosure -> non-physical coil forces)\n"
    "- Mesher: mesh_spring.py (Gmsh, 0 vol elems) -> mesh_netgen.py (Netgen maxh=1.0)\n"
    "- Abaqus solver: 16 cpus (mp_mode=threads)\n\n"
    "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
)
subprocess.run(["git", "-C", BASE, "commit", "-m", commit_msg], check=False)
subprocess.run(["git", "-C", BASE, "push"], check=False)
print("\n=== Full pipeline complete ===")
