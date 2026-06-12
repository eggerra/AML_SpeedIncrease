"""
run_oval_pipeline.py
====================
Runs the full valve-spring FEA pipeline for the OVAL wire cross-section
(formula (40) from DFE6113_5004_00-MasterThesis-VATA, c=0.2, area-matched),
then calls compare_wire_profiles.py to produce the comparison report.

Steps
-----
1. Backup existing ellipse FEA results to ValveSpring_ellipse_contact.dat
2. Generate STEP for oval profile (FreeCADCmd generate_spring.py oval)
3. Mesh oval STEP (FreeCADCmd mesh_spring.py  via env vars)
4. Run CalculiX FEA  (spring_analysis.py via env vars)
5. Run comparison + report update (compare_wire_profiles.py)
6. Commit + push to git

Usage
-----
    python run_oval_pipeline.py
"""
import os, sys, shutil, subprocess, time

BASE     = r"D:\Projects_AI\AML_SpeedIncrease"
FREECAD  = r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\FreeCADCmd.exe"

# -- file paths ----------------------------------------------------------------
ELLIPSE_DAT  = os.path.join(BASE, "ValveSpring_contact.dat")
ELLIPSE_DAT_BAK = os.path.join(BASE, "ValveSpring_ellipse_contact.dat")
OVAL_STEP    = os.path.join(BASE, "ValveSpring_oval.step")
OVAL_MESH    = os.path.join(BASE, "ValveSpring_oval_mesh.inp")
OVAL_FCSTD   = os.path.join(BASE, "ValveSpring_oval_meshed.FCStd")
OVAL_JOB     = "ValveSpring_oval_contact"
OVAL_DAT     = os.path.join(BASE, OVAL_JOB + ".dat")
OVAL_PLOT    = os.path.join(BASE, "spring_FvL_oval.png")


def run(cmd, env=None, desc=""):
    print(f"\n--- {desc or ' '.join(str(c) for c in cmd)} ---")
    t0 = time.time()
    merged = {**os.environ, **(env or {})}
    r = subprocess.run(cmd, env=merged, cwd=BASE)
    elapsed = time.time() - t0
    if r.returncode != 0:
        sys.exit(f"ERROR: command failed (code {r.returncode})  [{elapsed:.0f}s]")
    print(f"  done in {elapsed:.0f}s")


# =============================================================================
# 1. Backup current ellipse results
# =============================================================================
if os.path.isfile(ELLIPSE_DAT):
    shutil.copy2(ELLIPSE_DAT, ELLIPSE_DAT_BAK)
    print(f"Backed up: {ELLIPSE_DAT_BAK}")
else:
    print(f"WARNING: no ellipse results found at {ELLIPSE_DAT}")

# =============================================================================
# 2. Generate oval STEP geometry
# =============================================================================
run(
    [FREECAD, os.path.join(BASE, "generate_spring.py")],
    env={"SPRING_PROFILE": "oval"},
    desc="Generate oval STEP",
)
if not os.path.isfile(OVAL_STEP):
    sys.exit(f"ERROR: STEP file not created: {OVAL_STEP}")
print(f"  STEP: {OVAL_STEP}  ({os.path.getsize(OVAL_STEP)//1024} kB)")

# =============================================================================
# 3. Mesh oval STEP
# =============================================================================
run(
    [FREECAD, os.path.join(BASE, "mesh_spring.py")],
    env={
        "SPRING_STEP":     OVAL_STEP,
        "SPRING_MESH_OUT": OVAL_MESH,
        "SPRING_FCSTD":    OVAL_FCSTD,
    },
    desc="Mesh oval STEP",
)
if not os.path.isfile(OVAL_MESH):
    sys.exit(f"ERROR: mesh not created: {OVAL_MESH}")
print(f"  Mesh: {OVAL_MESH}  ({os.path.getsize(OVAL_MESH)//1024} kB)")

# =============================================================================
# 4. Run CalculiX FEA for oval mesh
# =============================================================================
run(
    [sys.executable, os.path.join(BASE, "spring_analysis.py")],
    env={
        "SPRING_MESH_INP": OVAL_MESH,
        "SPRING_JOB":      OVAL_JOB,
        "SPRING_PLOT":     OVAL_PLOT,
        "SPRING_L0":       "39.887",   # oval L0 (adjusted for larger wire_a_eff)
        "SPRING_WIRE_A":   "3.209",    # oval effective axial wire extent
    },
    desc="Run FEA (oval)",
)
if not os.path.isfile(OVAL_DAT):
    sys.exit(f"ERROR: FEA results not created: {OVAL_DAT}")
print(f"  DAT: {OVAL_DAT}  ({os.path.getsize(OVAL_DAT)} bytes)")

# =============================================================================
# 5. Comparison analysis + standalone comparison PDF
# =============================================================================
run(
    [sys.executable, os.path.join(BASE, "compare_wire_profiles.py")],
    desc="Compare profiles + write ValveSpring_WireComparison.pdf",
)

# =============================================================================
# 6. Regenerate main FEA report (now reflects oval geometry)
# =============================================================================
run(
    [sys.executable, os.path.join(BASE, "generate_report.py")],
    desc="Regenerate main FEA report (oval results)",
)

# =============================================================================
# 7. Git commit + push
# =============================================================================
files_to_stage = [
    "generate_spring.py", "mesh_spring.py", "spring_analysis.py",
    "run_oval_pipeline.py", "compare_wire_profiles.py",
    "ValveSpring_ellipse_contact.dat",
    "ValveSpring_FEA_Report.pdf",
    "ValveSpring_WireComparison.pdf",
    "spring_FvL_oval_comparison.png",
    "wire_crosssection_comparison.png",
    "README.md",
]
subprocess.run(
    ["git", "-C", BASE, "add"] + files_to_stage,
    check=False,
)
subprocess.run(
    ["git", "-C", BASE, "commit", "-m",
     "feat: oval wire cross-section FEA (formula 40) + comparison vs ellipse\n\n"
     "- generate_spring.py: oval profile via GeomAPI_Interpolate periodic spline\n"
     "  formula (40) DFE6113_5004_00, c=0.2, area-matched b=1.43585 mm\n"
     "- mesh_spring.py / spring_analysis.py: env-var parameterisation\n"
     "- compare_wire_profiles.py: oval vs ellipse vs measurement + WireComparison PDF\n"
     "- run_oval_pipeline.py: end-to-end pipeline runner\n"
     "- ValveSpring_FEA_Report.pdf: regenerated for oval geometry\n"
     "- ValveSpring_WireComparison.pdf: new cross-section comparison document\n\n"
     "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"],
    check=False,
)
subprocess.run(["git", "-C", BASE, "push"], check=False)
print("\n=== Oval pipeline complete ===")
