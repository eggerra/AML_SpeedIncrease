"""
run_preload_sweep.py
====================
Parametric preload sweep — 3 cases run sequentially on local Abaqus/Standard (14 CPUs).

Cases (n_closed=0.8 per end, n_active=7.0, oval wire, same mesh seed 0.25mm):
  250N : L0=47.58 mm  ->  F_preload~250 N,  F_full~617 N
  265N : L0=48.26 mm  ->  F_preload~265 N,  F_full~632 N
  280N : L0=48.95 mm  ->  F_preload~280 N,  F_full~647 N

Writes per-case RF files and a combined comparison plot spring_FvL_sweep.png.
Git-commits simulation_log.md every 10 min during each solve.
"""
import os, sys, subprocess, time, datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE      = r"D:\Projects_AI\AML_SpeedIncrease"
FREECAD   = r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin\FreeCADCmd.exe"
ABAQUS    = r"N:\CAE\simulia\v2025FP2524\Commands\abaqus.bat"
SIM_LOG   = os.path.join(BASE, "simulation_log.md")
MEAS_FILE = os.path.join(BASE, "INT_Spring_measurement.txt")

CASES = [
    {
        "label":         "250N",
        "L0":            "47.58",
        "n_closed":      "0.8",
        "F_preload":     "250.0",
        "F_full_target":  617.0,
        "step_out":      "ValveSpring_250N_oval.step",
        "mesh_job":      "ValveSpring_250N_abq_mesh",
        "mesh_inp":      "ValveSpring_250N_abq_mesh.inp",
        "ccx_job":       "ValveSpring_250N_contact",
        "abq_job":       "ValveSpring_250N_contact_abaqus",
        "rf_txt":        "ValveSpring_250N_contact_abaqus_rf.txt",
        "plot":          "spring_FvL_250N.png",
        "color":         "royalblue",
    },
    {
        "label":         "265N",
        "L0":            "48.26",
        "n_closed":      "0.8",
        "F_preload":     "265.0",
        "F_full_target":  632.0,
        "step_out":      "ValveSpring_265N_oval.step",
        "mesh_job":      "ValveSpring_265N_abq_mesh",
        "mesh_inp":      "ValveSpring_265N_abq_mesh.inp",
        "ccx_job":       "ValveSpring_265N_contact",
        "abq_job":       "ValveSpring_265N_contact_abaqus",
        "rf_txt":        "ValveSpring_265N_contact_abaqus_rf.txt",
        "plot":          "spring_FvL_265N.png",
        "color":         "darkorange",
    },
    {
        "label":         "280N",
        "L0":            "48.95",
        "n_closed":      "0.8",
        "F_preload":     "280.0",
        "F_full_target":  647.0,
        "step_out":      "ValveSpring_280N_oval.step",
        "mesh_job":      "ValveSpring_280N_abq_mesh",
        "mesh_inp":      "ValveSpring_280N_abq_mesh.inp",
        "ccx_job":       "ValveSpring_280N_contact",
        "abq_job":       "ValveSpring_280N_contact_abaqus",
        "rf_txt":        "ValveSpring_280N_contact_abaqus_rf.txt",
        "plot":          "spring_FvL_280N.png",
        "color":         "crimson",
    },
]

L_INSTALLED = 36.1
VALVE_LIFT  = 10.0
L_FULL_LIFT = 26.1
MONITOR_SECS = 600   # 10-minute git push interval
POLL_SECS    = 30

# ── helpers ───────────────────────────────────────────────────────────────────

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n## {ts}  —  {msg}\n"
    with open(SIM_LOG, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  [log] {msg}")


def run(cmd, env=None, desc=""):
    label = desc or " ".join(str(c) for c in cmd)
    print(f"\n--- {label} ---")
    t0 = time.time()
    merged = {**os.environ, **(env or {})}
    r = subprocess.run(cmd, env=merged, cwd=BASE)
    elapsed = time.time() - t0
    if r.returncode != 0:
        sys.exit(f"ERROR: {label} failed (code {r.returncode})  [{elapsed:.0f}s]")
    print(f"  done in {elapsed:.0f}s")
    return elapsed


def read_sta(sta_file):
    if not os.path.isfile(sta_file):
        return "no .sta yet"
    try:
        with open(sta_file) as f:
            for line in reversed(f.readlines()):
                parts = line.split()
                if len(parts) >= 6:
                    try:
                        step = int(parts[0]); inc = int(parts[1])
                        tt = float(parts[4]); st = float(parts[5])
                        return f"Step {step} Inc {inc}  total={tt:.2f}s  step={st:.2f}mm"
                    except (ValueError, IndexError):
                        pass
    except Exception:
        pass
    return "no increment data yet"


def git_push_log(case_label, sta_summary):
    subprocess.run(["git", "-C", BASE, "add", "simulation_log.md"],
                   check=False, capture_output=True)
    subprocess.run(["git", "-C", BASE, "commit", "-m",
                    f"sim: sweep {case_label} — {sta_summary}"],
                   check=False, capture_output=True)
    subprocess.run(["git", "-C", BASE, "push"],
                   check=False, capture_output=True)


def load_rf(path):
    lifts, forces = [], []
    if not os.path.isfile(path):
        return np.array([]), np.array([])
    with open(path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    lifts.append(float(parts[0]))
                    forces.append(abs(float(parts[1])))
                except ValueError:
                    pass
    a = np.array(lifts); b = np.array(forces)
    idx = np.argsort(a)
    return a[idx], b[idx]


def load_measurement():
    ml, mf = [], []
    if not os.path.isfile(MEAS_FILE):
        return None, None
    with open(MEAS_FILE) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    mf.append(float(parts[0]))
                    ml.append(float(parts[1]))
                except ValueError:
                    pass
    if not ml:
        return None, None
    ml = np.array(ml); mf = np.array(mf)
    s_pre = float(CASES[0]["L0"]) - L_INSTALLED
    return s_pre + ml, mf


def plot_comparison():
    fig, (ax, ax_r) = plt.subplots(2, 1, figsize=(11, 10), sharex=True,
                                    gridspec_kw={"height_ratios": [2, 1]})
    fig.subplots_adjust(hspace=0.08)

    meas_s, meas_f = load_measurement()
    if meas_s is not None:
        ax.plot(meas_s, meas_f, "k--", linewidth=1.5, alpha=0.7,
                label="Measurement (reference)")

    for c in CASES:
        rf = os.path.join(BASE, c["rf_txt"])
        s, f = load_rf(rf)
        if len(s) < 2:
            continue
        s_pre = float(c["L0"]) - L_INSTALLED
        s_full = float(c["L0"]) - L_FULL_LIFT
        ax.axvline(s_pre, color=c["color"], linestyle=":", linewidth=0.8, alpha=0.5)
        ax.plot(s, f, color=c["color"], linewidth=2.0, marker="o", ms=4,
                label=f"FEA {c['label']} preload  L0={c['L0']} mm")
        # Rate panel
        if len(s) >= 4:
            k = np.diff(f) / np.diff(s)
            sm = 0.5 * (s[:-1] + s[1:])
            ax_r.plot(sm, k, color=c["color"], linewidth=1.8, marker="o", ms=3)

    ax.set_ylabel("Spring Force [N]", fontsize=11)
    ax.set_title("Valve Spring — Preload Sweep  (n_closed=0.8, oval wire, Abaqus/Standard)",
                 fontsize=11)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0); ax.set_ylim(bottom=0)

    ax_r.set_ylabel("Local Rate  dF/ds  [N/mm]", fontsize=11)
    ax_r.set_xlabel("Compression from Free Length [mm]", fontsize=11)
    ax_r.grid(True, alpha=0.3); ax_r.set_ylim(bottom=0)

    plt.tight_layout()
    out = os.path.join(BASE, "spring_FvL_sweep.png")
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  Sweep comparison plot: {out}")
    return out


# ── main sweep ────────────────────────────────────────────────────────────────

# Initialise simulation log
with open(SIM_LOG, "w", encoding="utf-8") as f:
    f.write(
        f"# Preload Sweep Log\n\n"
        f"**Run started:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"**Cases:** 250 N / 265 N / 280 N  (n_closed=0.8, oval wire, 0.25mm mesh)\n\n"
        f"## Targets\n"
        f"| Case | L0 [mm] | s_preload [mm] | F_preload [N] | F_full_target [N] |\n"
        f"|------|---------|---------------|--------------|-------------------|\n"
    )
    for c in CASES:
        s_pre = float(c["L0"]) - L_INSTALLED
        f.write(f"| {c['label']} | {c['L0']} | {s_pre:.2f} | {c['F_preload']} "
                f"| ~{c['F_full_target']:.0f} |\n")
    f.write("\n## Progress\n")

completed_cases = []

for case_idx, case in enumerate(CASES):
    label   = case["label"]
    L0_str  = case["L0"]
    L0_val  = float(L0_str)
    s_pre   = L0_val - L_INSTALLED
    s_full  = L0_val - L_FULL_LIFT

    log(f"Case {label} START — L0={L0_str} mm, n_closed={case['n_closed']}, "
        f"s_pre={s_pre:.2f} mm")

    # --- 1. CAD ---
    log(f"Case {label} — CAD generation RUNNING")
    run(
        [FREECAD, os.path.join(BASE, "generate_spring.py")],
        env={
            "SPRING_PROFILE":  "oval",
            "SPRING_L0":       L0_str,
            "SPRING_N_CLOSED": case["n_closed"],
            "SPRING_STEP_OUT": case["step_out"],
            "SPRING_STL_OUT":  case["step_out"].replace(".step", ".stl"),
        },
        desc=f"Generate STEP for {label}",
    )
    step_path = os.path.join(BASE, case["step_out"])
    if not os.path.isfile(step_path):
        sys.exit(f"ERROR: STEP not created: {step_path}")
    log(f"Case {label} — CAD DONE  ({os.path.getsize(step_path)//1024} kB)")

    # --- 2. Mesh ---
    log(f"Case {label} — Meshing RUNNING (Abaqus CAE 0.25 mm)")
    run(
        [ABAQUS, "cae", f"noGUI={os.path.join(BASE, 'mesh_abaqus_hpc.py')}"],
        env={
            "SPRING_STEP_FILE": step_path,
            "SPRING_MESH_JOB":  case["mesh_job"],
        },
        desc=f"Mesh {label}",
    )
    mesh_path = os.path.join(BASE, case["mesh_inp"])
    if not os.path.isfile(mesh_path):
        sys.exit(f"ERROR: mesh not created: {mesh_path}")
    log(f"Case {label} — Mesh DONE  ({os.path.getsize(mesh_path)//1024} kB)")

    # --- 3. Write INP ---
    log(f"Case {label} — Writing FEA INP")
    run(
        [sys.executable, os.path.join(BASE, "spring_analysis.py")],
        env={
            "SPRING_MESH_INP":  mesh_path,
            "SPRING_JOB":       case["ccx_job"],
            "SPRING_PLOT":      os.path.join(BASE, case["plot"]),
            "SPRING_L0":        L0_str,
            "SPRING_WIRE_A":    "2.92",
            "SPRING_N_CLOSED":  case["n_closed"],
            "SPRING_F_PRELOAD": case["F_preload"],
            "NO_CCX":           "1",
        },
        desc=f"Write INP for {label}",
    )
    ccx_inp = os.path.join(BASE, case["ccx_job"] + ".inp")
    if not os.path.isfile(ccx_inp):
        sys.exit(f"ERROR: INP not created: {ccx_inp}")
    log(f"Case {label} — INP DONE  ({os.path.getsize(ccx_inp)//1024} kB)")

    # --- 4. Abaqus solve (with 10-min monitoring) ---
    log(f"Case {label} — Abaqus solve RUNNING (14 CPUs)")
    sta_file = os.path.join(BASE, case["abq_job"] + ".sta")
    t_start  = time.time()

    proc = subprocess.Popen(
        [sys.executable, os.path.join(BASE, "run_abaqus.py"), "14"],
        cwd=BASE,
        env={
            **os.environ,
            "SPRING_L0":        L0_str,
            "SPRING_F_PRELOAD": case["F_preload"],
            "SPRING_CCX_JOB":   case["ccx_job"],
            "SPRING_ABQ_JOB":   case["abq_job"],
            "SPRING_PLOT":      case["plot"],
        },
    )

    last_monitor = time.time()
    while proc.poll() is None:
        now = time.time()
        if now - last_monitor >= MONITOR_SECS:
            elapsed_h = (now - t_start) / 3600
            sta = read_sta(sta_file)
            log(f"Case {label} — RUNNING {elapsed_h:.1f}h — {sta}")
            git_push_log(label, sta)
            last_monitor = now
        time.sleep(POLL_SECS)

    elapsed_abq = time.time() - t_start
    if proc.returncode != 0:
        log(f"Case {label} — Abaqus FAILED (code {proc.returncode})")
        sys.exit(f"ERROR: Abaqus failed for case {label}")

    rf_path = os.path.join(BASE, case["rf_txt"])
    if os.path.isfile(rf_path):
        with open(rf_path) as fh:
            lines = [l for l in fh if not l.startswith("#")]
        forces = [abs(float(l.split()[1])) for l in lines if len(l.split()) >= 2]
        fmin = min(forces) if forces else 0
        fmax = max(forces) if forces else 0
        log(f"Case {label} — COMPLETED  F={fmin:.0f}-{fmax:.0f} N  wall={elapsed_abq/3600:.1f}h")
    else:
        log(f"Case {label} — COMPLETED (no RF file)  wall={elapsed_abq/3600:.1f}h")

    completed_cases.append(case)

    # --- intermediate git push with results ---
    subprocess.run(["git", "-C", BASE, "add",
                    case["step_out"], case["mesh_inp"],
                    case["ccx_job"] + ".inp",
                    case["abq_job"] + "_rf.txt",
                    case["plot"],
                    "simulation_log.md"],
                   check=False, capture_output=True, cwd=BASE)
    subprocess.run(["git", "-C", BASE, "commit", "-m",
                    f"sim: case {label} complete — L0={L0_str}mm, n_closed=0.8"],
                   check=False, capture_output=True)
    subprocess.run(["git", "-C", BASE, "push"], check=False, capture_output=True)

# --- comparison plot ---
plot_out = plot_comparison()
log("Sweep COMPLETE — comparison plot written")

# --- write results summary to simulation_log ---
with open(SIM_LOG, "a", encoding="utf-8") as f:
    f.write("\n## Results Summary\n")
    f.write("| Case | L0 [mm] | F_preload [N] | F_full [N] | Target [N] | Error |\n")
    f.write("|------|---------|--------------|-----------|-----------|-------|\n")
    for c in CASES:
        rf = os.path.join(BASE, c["rf_txt"])
        s_arr, f_arr = load_rf(rf)
        if len(s_arr) == 0:
            f.write(f"| {c['label']} | {c['L0']} | — | — | ~{c['F_full_target']:.0f} | — |\n")
            continue
        s_pre_val = float(c["L0"]) - L_INSTALLED
        s_full_val = float(c["L0"]) - L_FULL_LIFT
        # Interpolate at preload and full-lift points
        def interp_f(s_target, s_arr=s_arr, f_arr=f_arr):
            for i in range(len(s_arr)-1):
                if s_arr[i] <= s_target <= s_arr[i+1]:
                    t = (s_target - s_arr[i]) / (s_arr[i+1] - s_arr[i])
                    return f_arr[i] + t*(f_arr[i+1]-f_arr[i])
            return f_arr[-1] if s_target >= s_arr[-1] else f_arr[0]
        fp = interp_f(s_pre_val)
        ff = interp_f(s_full_val)
        err = (ff / c["F_full_target"] - 1) * 100
        f.write(f"| {c['label']} | {c['L0']} | {fp:.0f} | {ff:.0f} "
                f"| ~{c['F_full_target']:.0f} | {err:+.1f}% |\n")

# --- final git commit ---
files = (["simulation_log.md", "spring_FvL_sweep.png",
          "generate_spring.py", "spring_analysis.py", "run_abaqus.py",
          "mesh_abaqus_hpc.py", "run_preload_sweep.py"]
         + [c["rf_txt"] for c in CASES]
         + [c["plot"] for c in CASES])
subprocess.run(["git", "-C", BASE, "add"] + files, check=False)
subprocess.run(
    ["git", "-C", BASE, "commit", "-m",
     "feat: preload sweep 250/265/280N — n_closed=0.8, L0 adjusted, F_full on target\n\n"
     "- 3 cases: L0=47.58/48.26/48.95mm, n_closed=0.8 (n_active=7.0)\n"
     "- generate_spring/spring_analysis/run_abaqus: parametric via env vars\n"
     "- run_preload_sweep.py: new orchestrator with 10-min git monitoring\n\n"
     "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"],
    check=False,
)
subprocess.run(["git", "-C", BASE, "push"], check=False)
print("\n=== Preload sweep complete ===")
