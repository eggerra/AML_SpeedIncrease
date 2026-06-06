"""
plot_contact_results.py
Parse ValveSpring_contact.dat and plot Force vs Lift from self-contact FEA.
The 20 mm point is marked as unreliable (near solid height).
"""
import re, os
import numpy as np
import matplotlib.pyplot as plt

BASE    = r"D:\Projects_AI\AML_SpeedIncrease"
DAT     = os.path.join(BASE, "ValveSpring_contact.dat")
PLOT    = os.path.join(BASE, "spring_FvL_contact.png")

L0          = 46.1
L_INSTALLED = 36.1
L_FULL_LIFT = 26.1
S_PRELOAD   = L0 - L_INSTALLED   # 10 mm
S_FULL_LIFT = L0 - L_FULL_LIFT   # 20 mm
VALVE_LIFT  = 10.0

# Solid height: nt*wire_a - 2*grind = 8.6*2.92 - 1.5 = 23.6 mm  ->  s_solid = 46.1-23.6 = 22.5 mm
# Near-solid threshold: flag points within 3 mm of solid height
S_SOLID         = L0 - (8.6 * 2.92 - 1.5)   # ~22.5 mm
S_RELIABLE_MAX  = S_SOLID - 3.0              # ~19.5 mm — last trustworthy region

REF = [(S_PRELOAD,   250.0, f"Preload: 250 N  (L={L_INSTALLED} mm)"),
       (S_FULL_LIFT, 620.0, f"Full lift: 620 N  (L={L_FULL_LIFT} mm)")]

# Analytical progressive spring rate (2-phase, calibrated to drawing)
k1, k2, sb = 25.0, 37.0, 10.0
def analytical_force(s):
    if s <= 0: return 0.0
    if s <= sb: return k1 * s
    return 250.0 + k2 * (s - sb)

# --- parse dat file ---
time_re = re.compile(r"forces.*?time\s+([\d.E+\-]+)", re.IGNORECASE)
node_re = re.compile(r"^\s+\d+\s+[\d.E+\-]+\s+[\d.E+\-]+\s+([\d.E+\-]+)")

lifts, forces = [], []
cur_time, cur_rf3, n = None, 0.0, 0

with open(DAT) as f:
    for line in f:
        m = time_re.search(line)
        if m:
            if cur_time is not None and n > 0:
                lifts.append(cur_time)
                forces.append(abs(cur_rf3))
            cur_time, cur_rf3, n = float(m.group(1)), 0.0, 0
            continue
        if cur_time is not None:
            m2 = node_re.match(line)
            if m2:
                cur_rf3 += float(m2.group(1))
                n += 1

if cur_time is not None and n > 0:
    lifts.append(cur_time)
    forces.append(abs(cur_rf3))

lifts  = np.array(lifts)
forces = np.array(forces)
idx    = np.argsort(lifts)
lifts, forces = lifts[idx], forces[idx]

# Split into reliable and near-solid-height points
mask_ok  = lifts <= S_RELIABLE_MAX
mask_bad = lifts >  S_RELIABLE_MAX

print(f"Data points: {len(lifts)}  (reliable: {mask_ok.sum()}, near solid-height: {mask_bad.sum()})")
for l, f_ in zip(lifts, forces):
    flag = "  << near solid height — unreliable" if l > S_RELIABLE_MAX else ""
    print(f"  lift={l:.3f} mm   F={f_:.1f} N{flag}")

# --- plot ---
fig, ax = plt.subplots(figsize=(11, 6.5))

# Shade valve operating range
ax.axvspan(S_PRELOAD, S_FULL_LIFT, alpha=0.07, color="blue",
           label=f"Valve operating range ({VALVE_LIFT:.0f} mm lift)")

# Near-solid-height warning band
ax.axvspan(S_RELIABLE_MAX, S_FULL_LIFT + 0.5, alpha=0.10, color="red")
ax.axvline(S_RELIABLE_MAX, color="red", linestyle="--", linewidth=1.0, alpha=0.6)
ax.text(S_RELIABLE_MAX + 0.15, 50, "Near solid\nheight", fontsize=7.5,
        color="red", alpha=0.8, va="bottom")

# Analytical progressive curve (full range)
s_ana = np.linspace(0, S_FULL_LIFT, 300)
f_ana = np.array([analytical_force(s) for s in s_ana])
ax.plot(s_ana, f_ana, "g-", linewidth=2.2,
        label=f"Analytical progressive  k={k1:.0f}→{k2:.0f} N/mm  (calibrated to drawing)")

# FEA — reliable points
if mask_ok.sum() >= 2:
    ax.plot(lifts[mask_ok], forces[mask_ok], "b-o", ms=6, linewidth=2.0,
            label="CalculiX FEA (NLGEOM, C3D10, self-contact)  — reliable")
    # Linear fit over reliable operating range only
    op = mask_ok & (lifts >= S_PRELOAD)
    if op.sum() >= 2:
        coeff  = np.polyfit(lifts[op], forces[op], 1)
        k_fea  = coeff[0]
        l_fit  = np.linspace(lifts[op].min(), lifts[op].max(), 50)
        ax.plot(l_fit, np.polyval(coeff, l_fit), "b--", alpha=0.45, linewidth=1.2,
                label=f"FEA linear fit (operating range)  k={k_fea:.1f} N/mm")

# FEA — unreliable (near solid height)
if mask_bad.sum() > 0:
    ax.plot(lifts[mask_bad], forces[mask_bad], "rs", ms=8, markerfacecolor="none",
            markeredgewidth=1.8, zorder=6,
            label="FEA — near solid height (unreliable)")
    for l, f_ in zip(lifts[mask_bad], forces[mask_bad]):
        ax.annotate(f"{f_:.0f} N\n(near Ls)", xy=(l, f_),
                    xytext=(l - 2.2, f_ - 120), fontsize=7.5, color="red",
                    arrowprops=dict(arrowstyle="->", color="red", lw=0.8))

# Drawing reference marks
for lr, fr, lbl in REF:
    ax.axvline(lr, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.plot(lr, fr, "r^", ms=10, zorder=5)
    ax.annotate(lbl, xy=(lr, fr), xytext=(lr + 0.35, fr - 45),
                fontsize=8.5, color="darkred")

# Info box
info = (f"Drawing A177 053 05 00  |  Material: VD SiCrNi SC\n"
        f"Free length {L0} mm  →  Installed {L_INSTALLED} mm ({250:.0f} N)\n"
        f"Valve lift {VALVE_LIFT:.0f} mm  →  Full lift {L_FULL_LIFT} mm ({620:.0f} N)\n"
        f"Solid height Ls ≈ {L0 - S_SOLID:.1f} mm  (s_solid ≈ {S_SOLID:.1f} mm)")
ax.text(0.02, 0.97, info, transform=ax.transAxes, fontsize=8,
        va="top", color="navy",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="lightyellow", alpha=0.85))

ax.set_xlabel("Compression from Free Length [mm]", fontsize=11)
ax.set_ylabel("Spring Force [N]", fontsize=11)
ax.set_title("Valve Spring A177 053 05 00  –  Force vs Lift\n"
             "CalculiX Self-Contact FEA vs Analytical Progressive Model",
             fontsize=12)
ax.legend(fontsize=9, loc="upper left", bbox_to_anchor=(0.02, 0.72))
ax.grid(True, alpha=0.3)
ax.set_xlim(left=0, right=S_FULL_LIFT + 0.8)
ax.set_ylim(bottom=0)

ax2 = ax.secondary_xaxis("top",
    functions=(lambda s: L0 - s, lambda L: L0 - L))
ax2.set_xlabel("Spring Installed Length [mm]", fontsize=10)

plt.tight_layout()
plt.savefig(PLOT, dpi=150)
print(f"\nPlot saved: {PLOT}")
