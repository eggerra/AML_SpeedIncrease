"""
postprocess_fea.py  -  Parse ValveSpring_contact.dat and compare to measurement.

Reads:
  ValveSpring_contact.dat   (CalculiX reaction force output)
  INT_Spring_measurement.txt  (col1=Force[N], col2=lift from installed [mm])

Produces:
  spring_FvL_comparison.png  (force vs lift + local rate + error panels)
"""
import re, os
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

BASE = r"D:\Projects_AI\AML_SpeedIncrease"

DAT_FILE  = os.path.join(BASE, "ValveSpring_contact.dat")
MEAS_FILE = os.path.join(BASE, "INT_Spring_measurement.txt")
PLOT_FILE = os.path.join(BASE, "spring_FvL_comparison.png")

L0          = 46.1    # free length [mm]
L_INSTALLED = 31.6    # installed length [mm]
VALVE_LIFT  = 10.0    # valve lift stroke [mm]
S_PRELOAD   = L0 - L_INSTALLED        # 14.5 mm compression at preload
S_FULL_LIFT = S_PRELOAD + VALVE_LIFT  # 24.5 mm compression at full lift

# ── 1.  Parse .dat  ────────────────────────────────────────────────────────────
# Format produced by *NODE PRINT, TOTALS=ONLY  (or un-summed per-node lines):
#   total force (fx,fy,fz) for set NBOT and time  T
#       fx   fy   fz
time_re  = re.compile(r"total force.*?time\s+([\d.E+\-]+)", re.IGNORECASE)
force_re = re.compile(r"^\s+([\d.E+\-]+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)\s*$")

fea_s, fea_f = [], []
cur_time = None

with open(DAT_FILE) as fh:
    for line in fh:
        m = time_re.search(line)
        if m:
            cur_time = float(m.group(1))
            continue
        if cur_time is not None:
            m2 = force_re.match(line)
            if m2:
                fz = float(m2.group(3))
                fea_s.append(cur_time)
                fea_f.append(abs(fz))
                cur_time = None

fea_s = np.array(fea_s)
fea_f = np.array(fea_f)
idx = np.argsort(fea_s)
fea_s, fea_f = fea_s[idx], fea_f[idx]

# convert compression from free length  ->  valve lift from installed (for x-axis)
fea_lift = fea_s - S_PRELOAD   # negative = before preload, 0..10 = operating range

print(f"FEA data points : {len(fea_s)}")
for s, f in zip(fea_s, fea_f):
    lift = s - S_PRELOAD
    print(f"  s={s:5.1f} mm  (lift={lift:+.1f} mm)  F={f:.1f} N")

# ── 2.  Load measurement  ──────────────────────────────────────────────────────
meas_raw = np.loadtxt(MEAS_FILE)
meas_f_raw   = meas_raw[:, 0]   # Force [N]
meas_lift_raw = meas_raw[:, 1]  # lift from installed [mm]

# Remove duplicate x values (keep last)
_, uniq = np.unique(meas_lift_raw, return_index=True)
meas_lift = meas_lift_raw[uniq]
meas_f    = meas_f_raw[uniq]
meas_s    = S_PRELOAD + meas_lift   # compression from free length

meas_interp = interp1d(meas_lift, meas_f, kind='linear', bounds_error=False,
                       fill_value='extrapolate')

print(f"\nMeasurement: {len(meas_f)} points  "
      f"F={meas_f.min():.1f}-{meas_f.max():.1f} N  "
      f"lift={meas_lift.min():.3f}-{meas_lift.max():.2f} mm")

# ── 3.  Error at FEA points in operating range  ────────────────────────────────
in_range = (fea_lift >= -0.01) & (fea_lift <= VALVE_LIFT + 0.01)
print(f"\n{'Lift [mm]':>10}  {'FEA [N]':>10}  {'Meas [N]':>10}  {'Err [N]':>9}  {'Err [%]':>8}")
print("-" * 55)
for lift, f_fea in zip(fea_lift[in_range], fea_f[in_range]):
    f_meas = float(meas_interp(lift))
    err    = f_fea - f_meas
    err_pct = 100.0 * err / f_meas
    print(f"  {lift:7.2f}    {f_fea:8.1f}    {f_meas:8.1f}   {err:+8.1f}   {err_pct:+7.1f}%")

# ── 4.  Plot  ──────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(11, 12),
                         gridspec_kw={"height_ratios": [3, 1.5, 1.5]},
                         sharex=True)
fig.subplots_adjust(hspace=0.08)

ax, ax_rate, ax_err = axes

# ── Panel 1: Force vs lift  ────────────────────────────────────────────────────
ax.axvspan(0, VALVE_LIFT, alpha=0.07, color="steelblue", label="Valve operating range")
ax.axvline(0, color="gray", lw=0.8, ls=":")
ax.axvline(VALVE_LIFT, color="gray", lw=0.8, ls=":")

ax.plot(meas_lift, meas_f, "m-", lw=1.8, alpha=0.85, label="Measurement")
ax.plot(fea_lift, fea_f, "b-o", ms=7, lw=1.8, label="CalculiX FEA (Tet10, self-contact)")

# Reference points
ax.plot(0,          meas_f[0],  "r^", ms=9, zorder=6)
ax.plot(VALVE_LIFT, meas_f[-1], "r^", ms=9, zorder=6)
ax.annotate(f"Preload  {meas_f[0]:.0f} N", xy=(0, meas_f[0]),
            xytext=(0.5, meas_f[0]-55), fontsize=8, color="red")
ax.annotate(f"Full lift  {meas_f[-1]:.0f} N", xy=(VALVE_LIFT, meas_f[-1]),
            xytext=(7.0, meas_f[-1]-55), fontsize=8, color="red")

ax.set_ylabel("Spring Force [N]", fontsize=11)
ax.set_title(f"Valve Spring FEA vs Measurement\n"
             f"Free length {L0} mm  |  Installed {L_INSTALLED} mm  |  Valve lift {VALVE_LIFT:.0f} mm",
             fontsize=11)
ax.legend(fontsize=9, loc="upper left")
ax.grid(True, alpha=0.3)
ax.set_ylim(bottom=0)

# Secondary x-axis: spring installed length
ax2 = ax.secondary_xaxis('top',
    functions=(lambda lift: L_INSTALLED - lift, lambda L: L_INSTALLED - L))
ax2.set_xlabel("Spring Installed Length [mm]", fontsize=10)

# ── Panel 2: Local spring rate dF/ds  ─────────────────────────────────────────
if len(meas_lift) > 4:
    k_meas = np.diff(meas_f) / np.diff(meas_lift)
    s_mid_meas = 0.5 * (meas_lift[:-1] + meas_lift[1:])
    win = 15
    k_sm = np.convolve(k_meas, np.ones(win)/win, mode='valid')
    s_sm = s_mid_meas[win//2: win//2 + len(k_sm)]
    ax_rate.plot(s_sm, k_sm, "m-", lw=1.5, label="Measurement (smoothed)")

if len(fea_lift) >= 3:
    k_fea = np.diff(fea_f) / np.diff(fea_lift)
    s_mid_fea = 0.5 * (fea_lift[:-1] + fea_lift[1:])
    ax_rate.plot(s_mid_fea, k_fea, "b-o", ms=6, lw=1.5, label="FEA")

ax_rate.axvspan(0, VALVE_LIFT, alpha=0.07, color="steelblue")
ax_rate.axvline(0, color="gray", lw=0.8, ls=":")
ax_rate.axvline(VALVE_LIFT, color="gray", lw=0.8, ls=":")
ax_rate.set_ylabel("dF/dx  [N/mm]", fontsize=11)
ax_rate.legend(fontsize=9, loc="upper left")
ax_rate.grid(True, alpha=0.3)
ax_rate.set_ylim(bottom=0)

# ── Panel 3: Absolute error FEA - measurement  ────────────────────────────────
lifts_op  = fea_lift[in_range]
f_meas_at = np.array([float(meas_interp(l)) for l in lifts_op])
err_abs   = fea_f[in_range] - f_meas_at
err_pct   = 100.0 * err_abs / f_meas_at

ax_err.axhline(0, color="black", lw=0.8)
ax_err.bar(lifts_op, err_abs, width=0.35, color="steelblue", alpha=0.7, label="Abs error [N]")
ax_err.axvspan(0, VALVE_LIFT, alpha=0.07, color="steelblue")
ax_err.axvline(0, color="gray", lw=0.8, ls=":")
ax_err.axvline(VALVE_LIFT, color="gray", lw=0.8, ls=":")

ax_err2 = ax_err.twinx()
ax_err2.plot(lifts_op, err_pct, "rs--", ms=6, lw=1.4, label="Rel error [%]")
ax_err2.set_ylabel("Error [%]", fontsize=10, color="red")
ax_err2.tick_params(axis='y', colors='red')
ax_err2.axhline(5, color="red", lw=0.6, ls=":", alpha=0.5)
ax_err2.axhline(-5, color="red", lw=0.6, ls=":", alpha=0.5)

ax_err.set_xlabel("Valve Lift [mm]", fontsize=11)
ax_err.set_ylabel("FEA − Meas  [N]", fontsize=10)
ax_err.legend(fontsize=9, loc="upper left")
ax_err2.legend(fontsize=9, loc="upper right")
ax_err.grid(True, alpha=0.3)
ax_err.set_xlim(fea_lift.min() - 0.5, VALVE_LIFT + 0.5)

plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=150)
print(f"\nPlot saved: {PLOT_FILE}")
