"""
run_abaqus.py
=============
Valve spring FEA pipeline using Abaqus/Standard (replaces CalculiX).

Steps
-----
1. Convert ValveSpring_oval_contact.inp (CalculiX) -> ValveSpring_oval_contact_abaqus.inp
   - Replace *NODE FILE / *EL FILE / *CONTACT FILE with Abaqus *OUTPUT requests
   - Fix *STEP, NLGEOM flag syntax
2. Run Abaqus/Standard solver
3. Extract reaction forces from .odb (via  abaqus python postprocess_abaqus.py)
4. Plot F-L characteristic vs measurement + analytical model

Usage
-----
    python run_abaqus.py [cpus]        # cpus defaults to 4
"""
import os, sys, subprocess, time
import numpy as np
import matplotlib.pyplot as plt

# ── Paths ──────────────────────────────────────────────────────────────────
BASE        = r"D:\Projects_AI\AML_SpeedIncrease"
ABAQUS      = r"N:\CAE\simulia\v2025FP2524\Commands\abaqus.bat"
CCX_JOB     = "ValveSpring_oval_contact"
ABQ_JOB     = "ValveSpring_oval_contact_abaqus"
CCX_INP     = os.path.join(BASE, CCX_JOB + ".inp")
ABQ_INP     = os.path.join(BASE, ABQ_JOB + ".inp")
RF_TXT      = os.path.join(BASE, ABQ_JOB + "_rf.txt")
PLOT_FILE   = os.path.join(BASE, "spring_FvL_abaqus.png")
MEAS_FILE   = os.path.join(BASE, "INT_Spring_measurement.txt")
POST_SCRIPT = os.path.join(BASE, "postprocess_abaqus.py")

CPUS_DEFAULT = 14

# ── Spring parameters (drawing values, oval wire, n_closed=1.25) ──
# L0=46.1 mm drawing value; wire_a=2.92 mm used for coil pitch (no oval inflation).
# s_preload=10.0 mm (46.1->36.1), s_full_lift=20.0 mm (46.1->26.1).
L0          = 47.43    # free length [mm]  (drawing 46.1mm + 1.33mm for 280N preload)
L_INSTALLED = 36.1     # installed length [mm]  (fixed by engine)
VALVE_LIFT  = 10.0
L_FULL_LIFT = 26.1     # spring length at full valve lift [mm]
F_PRELOAD   = 280.0    # preload force target [N]  (raised from 250N)
F_FULL_LIFT = 620.7    # force at full lift [N]  (measurement)
S_PRELOAD   = L0 - L_INSTALLED    # 10.0 mm
S_FULL_LIFT = L0 - L_FULL_LIFT    # 20.0 mm

LIFT_KINK1 = 5.2
LIFT_KINK2 = 8.0
S_KINK1    = S_PRELOAD + LIFT_KINK1
S_KINK2    = S_PRELOAD + LIFT_KINK2
k1, k2, k3 = 22.60, 23.80, 26.70
F_KINK1    = F_PRELOAD + k1 * LIFT_KINK1
F_KINK2    = F_KINK1   + k2 * (LIFT_KINK2 - LIFT_KINK1)


def analytical_force(s):
    if s <= 0:         return 0.0
    elif s <= S_KINK1: return F_PRELOAD + k1 * (s - S_PRELOAD)
    elif s <= S_KINK2: return F_KINK1   + k2 * (s - S_KINK1)
    else:              return F_KINK2   + k3 * (s - S_KINK2)


# =============================================================================
# 1. GENERATE ABAQUS INPUT FILE
# =============================================================================
# CalculiX output block to remove (appears twice, once per step)
_CCX_OUT_LINES = [
    "*NODE FILE, FREQUENCY=5",
    "U",
    "*EL FILE, FREQUENCY=5",
    "S",
    "*CONTACT FILE, FREQUENCY=5",
    "CSTRESS, CDISP",
]

# Abaqus output block to insert in its place (after the NODE PRINT / RF lines)
# RF is in FIELD output so postprocess_abaqus.py can access frame.fieldOutputs['RF']
_ABQ_OUTPUT_BLOCK = """\
*OUTPUT, FIELD, FREQUENCY=5
*NODE OUTPUT
U, RF
*ELEMENT OUTPUT
S, MISES
*CONTACT OUTPUT
CSTRESS, CDISP
*OUTPUT, HISTORY, FREQUENCY=1
*ENERGY OUTPUT
ALLSE, ALLKE, ALLWK, ALLSD, ALLAE, ETOTAL"""


def generate_abaqus_inp():
    """Line-by-line conversion: CalculiX -> Abaqus output syntax."""
    if not os.path.isfile(CCX_INP):
        sys.exit(f"ERROR: CalculiX input not found: {CCX_INP}")

    with open(CCX_INP, "r", newline="") as f:
        lines = f.read().splitlines()

    out_lines = []
    i = 0
    node_print_freq = 5
    replacements = 0
    after_static = False

    while i < len(lines):
        line = lines[i]
        up   = line.strip().upper()

        # Capture FREQUENCY from NODE PRINT; fix TOTALS=ONLY -> TOTALS=YES
        if up.startswith("*NODE PRINT"):
            for token in line.split(","):
                t = token.strip().upper()
                if t.startswith("FREQUENCY="):
                    try:
                        node_print_freq = int(t.split("=")[1])
                    except ValueError:
                        pass
            # Abaqus 2025 does not support TOTALS=ONLY; use TOTALS=YES
            line = line.replace("TOTALS=ONLY", "TOTALS=YES")
            out_lines.append(line)
            i += 1
            continue

        # Fix NLGEOM flag: *STEP, NLGEOM, -> *STEP, NLGEOM=YES,
        if up.startswith("*STEP") and "NLGEOM" in up and "NLGEOM=YES" not in up:
            line = line.replace("NLGEOM,", "NLGEOM=YES,").replace(
                "NLGEOM ", "NLGEOM=YES ")
            out_lines.append(line)
            i += 1
            continue

        # Using EXPONENTIAL pressure-overclosure (c0=0.1mm, p0=0).
        # HARD contact with penalty enforcement — allow Abaqus to cut increments freely.
        # Min increment 0.001 mm; STABILIZE=0.0001 (reduced from 0.001 to keep
        # artificial stabilisation energy ALLSD < 5% of ALLWK per step.
        if after_static and not up.startswith("*"):
            after_static = False
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 4:
                try:
                    parts[2] = "0.001"  # min increment: 0.5 -> 0.001 mm
                    line = ", ".join(parts)
                except Exception:
                    pass
            out_lines.append(line)
            out_lines.append("*CONTACT CONTROLS, STABILIZE=0.0001")
            i += 1
            continue

        # Track *STATIC card so next data line can be modified
        if up.startswith("*STATIC"):
            after_static = True
            out_lines.append(line)
            i += 1
            continue

        # Skip CalculiX FILE output keywords and their data lines
        if up.startswith("*NODE FILE") or up.startswith("*EL FILE") or up.startswith("*CONTACT FILE"):
            i += 1
            # Skip the data line(s) that follow (not starting with *)
            while i < len(lines) and not lines[i].strip().startswith("*"):
                i += 1
            continue

        # After the RF data line of NODE PRINT, inject Abaqus OUTPUT block
        # (detect: previous line was *NODE PRINT and this line contains RF)
        if (out_lines and out_lines[-1].strip().upper().startswith("*NODE PRINT")
                and line.strip().upper() == "RF"):
            out_lines.append(line)  # keep "RF" for the NODE PRINT
            out_lines.append("**")
            # Inject Abaqus output block with the correct frequency
            abq_block = _ABQ_OUTPUT_BLOCK.replace(
                "FREQUENCY=5", f"FREQUENCY={node_print_freq}")
            out_lines.extend(abq_block.splitlines())
            replacements += 1
            i += 1
            continue

        out_lines.append(line)
        i += 1

    if replacements == 0:
        print("  WARNING: no CalculiX output blocks found to convert — check inp format")
    else:
        print(f"  Converted {replacements} step output block(s) to Abaqus syntax")

    with open(ABQ_INP, "w", newline="\n") as f:
        f.write("\n".join(out_lines) + "\n")

    kb = os.path.getsize(ABQ_INP) // 1024
    print(f"  Written: {ABQ_INP}  ({kb} kB)")


# =============================================================================
# 2. RUN ABAQUS SOLVER
# =============================================================================
def run_abaqus(cpus):
    # mp_mode=threads avoids the MPI launcher requirement on machines without NATIVE MPI
    cmd = [ABAQUS, f"job={ABQ_JOB}", f"cpus={cpus}", "mp_mode=threads", "interactive"]
    print(f"\n--- Running Abaqus: {' '.join(cmd)} ---")
    t0 = time.time()
    # Remove stale odb so a fast-fail is unambiguous and postprocess can't use old data.
    odb = os.path.join(BASE, ABQ_JOB + ".odb")
    if os.path.isfile(odb):
        try:
            os.remove(odb)
        except OSError:
            pass
    r = subprocess.run(cmd, cwd=BASE)
    elapsed = time.time() - t0
    if r.returncode not in (0, 2):   # Abaqus returns 2 on warning-only completion
        sys.exit(f"Abaqus solver failed (code {r.returncode})  [{elapsed:.0f}s]")
    # Verify the odb was actually created — exit code 2 can mask a pre-run error
    if not os.path.isfile(odb):
        sys.exit(f"Abaqus solver exited (code {r.returncode}) but no .odb was created "
                 f"[{elapsed:.0f}s] — check cpus, licensing, or input errors")
    print(f"  Solver done in {elapsed:.0f}s")


# =============================================================================
# 3. EXTRACT RESULTS FROM ODB
# =============================================================================
def extract_odb():
    """Run  abaqus python postprocess_abaqus.py  to write _rf.txt from .odb."""
    cmd = [ABAQUS, "python", POST_SCRIPT, ABQ_JOB]
    print(f"\n--- Extracting ODB: {' '.join(cmd)} ---")
    r = subprocess.run(cmd, cwd=BASE)
    if r.returncode != 0:
        print(f"  WARNING: ODB extraction returned code {r.returncode}")
        return False
    return os.path.isfile(RF_TXT)


# =============================================================================
# 4. PARSE RESULT FILE
# =============================================================================
def parse_results():
    if not os.path.isfile(RF_TXT):
        sys.exit(f"ERROR: result file not found: {RF_TXT}")
    lifts, forces = [], []
    with open(RF_TXT) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    lifts.append(float(parts[0]))
                    forces.append(abs(float(parts[1])))
                except ValueError:
                    pass
    if not lifts:
        sys.exit(f"ERROR: no data in {RF_TXT}")
    lifts  = np.array(lifts)
    forces = np.array(forces)
    idx    = np.argsort(lifts)
    return lifts[idx], forces[idx]


# =============================================================================
# 5. LOAD MEASUREMENT DATA
# =============================================================================
def load_measurement():
    if not os.path.isfile(MEAS_FILE):
        return None, None
    ml, mf = [], []
    with open(MEAS_FILE) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    mf.append(float(parts[0]))
                    ml.append(float(parts[1]))
                except ValueError:
                    pass
    ml = np.array(ml)
    mf = np.array(mf)
    return S_PRELOAD + ml, mf   # convert lift to compression from L0


# =============================================================================
# 6. PLOT F-L CHARACTERISTIC
# =============================================================================
def plot(lifts, forces, meas_s, meas_force):
    fig, (ax, ax_rate) = plt.subplots(2, 1, figsize=(10, 10), sharex=True,
                                       gridspec_kw={"height_ratios": [2, 1]})
    fig.subplots_adjust(hspace=0.08)

    ax.axvspan(S_PRELOAD, S_FULL_LIFT, alpha=0.08, color="blue",
               label=f"Valve operating range ({VALVE_LIFT:.0f} mm lift)")
    ax.plot(lifts, forces, "b-o", ms=4, linewidth=1.8,
            label="Abaqus/Standard FEA (NLGEOM, C3D10, self-contact, variable pitch)")

    if meas_s is not None:
        ax.plot(meas_s, meas_force, "m-", linewidth=1.5, alpha=0.85,
                label="Measurement INT_Spring_measurement.txt")

    s_ana = np.linspace(0, S_FULL_LIFT, 200)
    f_ana = np.array([analytical_force(s) for s in s_ana])
    ax.plot(s_ana, f_ana, "g-", linewidth=2.0,
            label=f"Analytical fit (3-phase)  k={k1:.0f}→{k2:.1f}→{k3:.1f} N/mm")

    for s_r, f_r, lbl in [
        (S_PRELOAD,   F_PRELOAD,   f"Preload: {F_PRELOAD:.0f} N  (L={L_INSTALLED} mm)"),
        (S_FULL_LIFT, F_FULL_LIFT, f"Full lift: {F_FULL_LIFT:.0f} N  (L={L_FULL_LIFT} mm)"),
    ]:
        ax.axvline(s_r, color="gray", linestyle=":", linewidth=0.8, alpha=0.6)
        ax.plot(s_r, f_r, "r^", ms=9, zorder=5)
        ax.annotate(lbl, xy=(s_r, f_r), xytext=(s_r + 0.4, f_r - 40),
                    fontsize=8, color="red")

    ax.set_ylabel("Spring Force [N]", fontsize=11)
    ax.set_title(
        "Valve Spring  –  Abaqus/Standard FEA vs Measurement\n"
        f"Free length {L0} mm  |  Installed {L_INSTALLED} mm ({F_PRELOAD:.0f} N)  |  "
        f"Valve lift {VALVE_LIFT:.0f} mm  |  Max force {F_FULL_LIFT:.0f} N",
        fontsize=11)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    ax2 = ax.secondary_xaxis("top",
        functions=(lambda s: L0 - s, lambda L: L0 - L))
    ax2.set_xlabel("Spring Installed Length [mm]", fontsize=10)

    if len(lifts) >= 4:
        k_local = np.diff(forces) / np.diff(lifts)
        s_mid   = 0.5 * (lifts[:-1] + lifts[1:])
        ax_rate.plot(s_mid, k_local, "b-o", ms=4, linewidth=1.8, label="FEA local rate")

        if meas_s is not None and len(meas_s) > 10:
            ds = np.diff(meas_s)
            k_m = np.where(ds > 1e-6, np.diff(meas_force) / np.where(ds > 1e-6, ds, 1), np.nan)
            win = 10
            if len(k_m) > win:
                k_sm = np.convolve(k_m, np.ones(win) / win, mode="valid")
                s_sm = 0.5 * (meas_s[:-1] + meas_s[1:])[win // 2:win // 2 + len(k_sm)]
                ax_rate.plot(s_sm, k_sm, "m-", linewidth=1.5, label="Measurement rate (smoothed)")

        k_ana_local = np.gradient(f_ana, s_ana)
        ax_rate.plot(s_ana, k_ana_local, "g-", linewidth=1.5, label="Analytical fit rate")
        ax_rate.axvspan(S_PRELOAD, S_FULL_LIFT, alpha=0.08, color="blue")
        ax_rate.set_ylabel("Local Rate  dF/ds  [N/mm]", fontsize=11)
        ax_rate.set_xlabel("Compression from Free Length [mm]", fontsize=11)
        ax_rate.legend(fontsize=9, loc="upper left")
        ax_rate.grid(True, alpha=0.3)
        ax_rate.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(PLOT_FILE, dpi=150)
    print(f"  Plot saved: {PLOT_FILE}")
    plt.show()


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    cpus = int(sys.argv[1]) if len(sys.argv) > 1 else CPUS_DEFAULT

    print("=== ValveSpring FEA  –  Abaqus/Standard Pipeline ===\n")

    print("[1/4] Generating Abaqus input file ...")
    generate_abaqus_inp()

    print(f"\n[2/4] Running Abaqus/Standard  (cpus={cpus}) ...")
    run_abaqus(cpus)

    print("\n[3/4] Extracting results from .odb ...")
    if not extract_odb():
        sys.exit(f"ERROR: result extraction failed.  Check {ABQ_JOB}.log")

    print("\n[4/4] Parsing & plotting ...")
    lifts, forces = parse_results()
    meas_s, meas_force = load_measurement()

    print(f"  FEA points  : {len(lifts)}")
    if len(forces) > 0:
        print(f"  Force range : {forces.min():.0f} – {forces.max():.0f} N")
    plot(lifts, forces, meas_s, meas_force)

    print("\n=== Abaqus pipeline complete ===")
