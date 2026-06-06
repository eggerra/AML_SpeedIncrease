"""
plot_results.py - Parse existing ValveSpring_fea.dat and plot Force vs Lift
"""
import re, os
import numpy as np
import matplotlib.pyplot as plt

BASE     = r"D:\Projects_AI\AML_SpeedIncrease"
DAT_FILE = os.path.join(BASE, "ValveSpring_fea.dat")
PLOT     = os.path.join(BASE, "spring_FvL.png")

REF = [(10.0, 250.0, "F1 = 250 N @ L1"), (20.0, 620.0, "F2 = 620 N @ L2")]

# ── Parse .dat: sum RF3 over all bottom nodes per time increment ──────────────
time_re   = re.compile(r"forces.*?time\s+([\d.E+\-]+)", re.IGNORECASE)
node_rf_re = re.compile(
    r"^\s+(\d+)\s+([\d.,E+\-]+)\s+([\d.,E+\-]+)\s+([\d.,E+\-]+)"
)

lifts, forces = [], []
cur_time, cur_rf3, cnt = None, 0.0, 0

with open(DAT_FILE) as f:
    for line in f:
        m = time_re.search(line)
        if m:
            if cur_time is not None and cnt > 0:
                lifts.append(cur_time)
                forces.append(abs(cur_rf3))
            cur_time, cur_rf3, cnt = float(m.group(1)), 0.0, 0
            continue
        if cur_time is not None:
            m2 = node_rf_re.match(line)
            if m2:
                # Handle both . and , as decimal separator (locale issue)
                val = float(m2.group(4).replace(",", "."))
                cur_rf3 += val
                cnt += 1

if cur_time is not None and cnt > 0:
    lifts.append(cur_time)
    forces.append(abs(cur_rf3))

lifts  = np.array(lifts)
forces = np.array(forces)
idx    = np.argsort(lifts)
lifts, forces = lifts[idx], forces[idx]

print(f"Data points: {len(lifts)}")
for l, f in zip(lifts, forces):
    print(f"  Lift = {l:5.1f} mm   Force = {f:7.1f} N")

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(lifts, forces, "b-o", ms=5, linewidth=2, label="CalculiX FEA (NLGEOM, Tet10)")

for lift_r, force_r, lbl in REF:
    ax.axvline(lift_r, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.plot(lift_r, force_r, "r^", ms=10, zorder=5)
    ax.annotate(lbl, xy=(lift_r, force_r), xytext=(lift_r+0.3, force_r-40),
                fontsize=9, color="red")

k_dwg = (REF[1][1] - REF[0][1]) / (REF[1][0] - REF[0][0])
ax.text(0.04, 0.94, f"Drawing rate (F1->F2): {k_dwg:.0f} N/mm",
        transform=ax.transAxes, fontsize=9, color="red")

if len(lifts) >= 4:
    k_coeff = np.polyfit(lifts, forces, 1)
    k_fea   = k_coeff[0]
    ax.plot(lifts, np.polyval(k_coeff, lifts), "b--",
            alpha=0.5, linewidth=1.2, label=f"Linear fit  k = {k_fea:.1f} N/mm")
    ax.text(0.04, 0.87, f"FEA rate (linear fit): {k_fea:.0f} N/mm",
            transform=ax.transAxes, fontsize=9, color="blue")

ax.set_xlabel("Spring Lift / Compression [mm]", fontsize=11)
ax.set_ylabel("Spring Force [N]", fontsize=11)
ax.set_title("Valve Spring A177 053 05 00 - Force vs Lift (FEA)", fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig(PLOT, dpi=150)
print(f"\nPlot saved: {PLOT}")
plt.show()
