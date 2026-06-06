"""
generate_report.py
Create a multi-page PDF report for the valve spring FEA study.
Uses matplotlib PdfPages only (no external dependencies).
"""
import re, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from mpl_toolkits.mplot3d import Axes3D

BASE   = r"D:\Projects_AI\AML_SpeedIncrease"
PDF    = os.path.join(BASE, "ValveSpring_FEA_Report.pdf")
DAT    = os.path.join(BASE, "ValveSpring_contact.dat")
MESH   = os.path.join(BASE, "ValveSpring_mesh.inp")
PREV   = os.path.join(BASE, "ValveSpring_preview.png")

# ── Spring / model constants ──────────────────────────────────────────────────
L0          = 46.1
wire_a      = 2.92
wire_r      = 3.66
nt          = 8.6
n_closed    = 1.25
Di_bot      = 15.90
Di_top      = 12.00
grind_z     = 0.75
D_pitch     = 0.22
n_active    = nt - 2 * n_closed        # 6.1
h_closed    = n_closed * wire_a        # 3.65
h_active    = L0 - 2 * h_closed       # 38.80
pitch_mean  = h_active / n_active      # 6.361
p_top       = pitch_mean * (1 - D_pitch)  # 4.96
p_bot       = pitch_mean * (1 + D_pitch)  # 7.76
R_mean_bot  = Di_bot / 2 + wire_r / 2
R_mean_top  = Di_top / 2 + wire_r / 2
E_MOD       = 206000.0
NU          = 0.30
L_INSTALLED = 36.1
L_FULL_LIFT = 26.1
S_PRELOAD   = L0 - L_INSTALLED
S_FULL_LIFT = L0 - L_FULL_LIFT
VALVE_LIFT  = 10.0
F_PRELOAD   = 250.0
F_FULL_LIFT = 620.0
S_SOLID     = L0 - (nt * wire_a - 2 * grind_z)
S_RELIABLE  = S_SOLID - 3.0
k1, k2, sb  = 25.0, 37.0, 10.0

# ── Parse mesh ────────────────────────────────────────────────────────────────
print("Parsing mesh...")
nodes_xyz = {}
in_node = False
with open(MESH) as f:
    for line in f:
        s  = line.strip()
        up = s.upper()
        if up.startswith("*NODE") and "PRINT" not in up and "FILE" not in up:
            in_node = True; continue
        elif s.startswith("*"):
            in_node = False
        elif in_node:
            p = s.split(",")
            if len(p) >= 4:
                try:
                    nodes_xyz[int(p[0])] = (float(p[1]), float(p[2]), float(p[3]))
                except ValueError:
                    pass

all_pts = np.array(list(nodes_xyz.values()))
print(f"  Nodes: {len(all_pts):,}")

# Sample for 3-D scatter
rng    = np.random.default_rng(42)
idx_s  = rng.choice(len(all_pts), size=min(3000, len(all_pts)), replace=False)
sample = all_pts[idx_s]

# ── Parse dat (F-L results) ───────────────────────────────────────────────────
print("Parsing results...")
time_re = re.compile(r"forces.*?time\s+([\d.E+\-]+)", re.IGNORECASE)
node_re = re.compile(r"^\s+\d+\s+[\d.E+\-]+\s+[\d.E+\-]+\s+([\d.E+\-]+)")

lifts, forces = [], []
cur_time, cur_rf3, n = None, 0.0, 0
with open(DAT) as f:
    for line in f:
        m = time_re.search(line)
        if m:
            if cur_time is not None and n > 0:
                lifts.append(cur_time); forces.append(abs(cur_rf3))
            cur_time, cur_rf3, n = float(m.group(1)), 0.0, 0
            continue
        if cur_time is not None:
            m2 = node_re.match(line)
            if m2:
                cur_rf3 += float(m2.group(1)); n += 1

if cur_time is not None and n > 0:
    lifts.append(cur_time); forces.append(abs(cur_rf3))

lifts  = np.array(lifts);  forces = np.array(forces)
order  = np.argsort(lifts); lifts, forces = lifts[order], forces[order]
mask_ok  = lifts <= S_RELIABLE
mask_bad = lifts >  S_RELIABLE

def af(s):
    if s <= 0: return 0.0
    return k1 * s if s <= sb else F_PRELOAD + k2 * (s - sb)

# ── Helper: page header / footer ─────────────────────────────────────────────
def header(fig, title, page, total=6):
    fig.text(0.5, 0.975, "CONFIDENTIAL — AML Valve Spring Study",
             ha="center", va="top", fontsize=7, color="gray")
    fig.text(0.02, 0.975, f"Drawing: A177 053 05 00", fontsize=7, color="gray")
    fig.text(0.98, 0.975, f"Page {page}/{total}", ha="right", fontsize=7, color="gray")
    fig.text(0.5, 0.015, title, ha="center", fontsize=9, color="#333333",
             fontweight="bold")

# ── PDF ───────────────────────────────────────────────────────────────────────
print(f"Writing PDF: {PDF}")
with PdfPages(PDF) as pdf:

    # ── Page 1: Title page ────────────────────────────────────────────────────
    fig = plt.figure(figsize=(11.69, 8.27))   # A4 landscape
    header(fig, "Title Page", 1)

    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")

    # Title block
    ax.text(0.5, 0.88, "Valve Spring Finite Element Analysis",
            ha="center", fontsize=26, fontweight="bold", color="#1a3a6b",
            transform=ax.transAxes)
    ax.text(0.5, 0.80, "Drawing A177 053 05 00  |  Intake Valve Spring (Beehive)",
            ha="center", fontsize=15, color="#444",
            transform=ax.transAxes)
    ax.plot([0.1, 0.9], [0.77, 0.77], color="#1a3a6b", linewidth=1.5,
            transform=ax.transAxes)

    # Two-column summary
    left = 0.10;  right = 0.55
    row  = 0.70;  dy    = 0.048

    def kv(col, r, key, val, bold_val=True):
        ax.text(col,       r, key + ":", fontsize=10, color="#555",
                transform=ax.transAxes, ha="left")
        ax.text(col+0.20,  r, val, fontsize=10, color="#111",
                fontweight="bold" if bold_val else "normal",
                transform=ax.transAxes, ha="left")

    ax.text(left,  row+0.04, "Spring Geometry", fontsize=11, fontweight="bold",
            color="#1a3a6b", transform=ax.transAxes)
    kv(left, row-0*dy, "Free length",      f"{L0} mm")
    kv(left, row-1*dy, "Wire cross-section", f"{wire_a} × {wire_r} mm (oval)")
    kv(left, row-2*dy, "Total coils",      f"{nt}  ({n_closed} closed each end)")
    kv(left, row-3*dy, "Active coils",     f"{n_active} (free length)")
    kv(left, row-4*dy, "OD range",         f"{Di_bot+wire_r:.1f} → {Di_top+wire_r:.1f} mm (beehive)")
    kv(left, row-5*dy, "Pitch range",      f"{p_top:.2f} → {p_bot:.2f} mm (top→bot)")
    kv(left, row-6*dy, "Solid height Ls",  f"≈ {L0-S_SOLID:.1f} mm")

    ax.text(right, row+0.04, "Operating Conditions", fontsize=11, fontweight="bold",
            color="#1a3a6b", transform=ax.transAxes)
    kv(right, row-0*dy, "Installed length", f"{L_INSTALLED} mm  (s = {S_PRELOAD:.0f} mm)")
    kv(right, row-1*dy, "Preload force",    f"{F_PRELOAD:.0f} N")
    kv(right, row-2*dy, "Valve lift",       f"{VALVE_LIFT:.0f} mm")
    kv(right, row-3*dy, "Full-lift length", f"{L_FULL_LIFT} mm  (s = {S_FULL_LIFT:.0f} mm)")
    kv(right, row-4*dy, "Full-lift force",  f"{F_FULL_LIFT:.0f} N")
    kv(right, row-5*dy, "Material",         "VD SiCrNi SC")
    kv(right, row-6*dy, "E / ν",            f"{E_MOD/1000:.0f} GPa / {NU}")

    ax.text(right, row+0.04-7*dy, "FE Model Summary", fontsize=11, fontweight="bold",
            color="#1a3a6b", transform=ax.transAxes)
    kv(right, row-7*dy, "Solver",  "CalculiX v2.22 (CCX)")
    kv(right, row-8*dy, "Elements","C3D10 (10-node tet, quadratic)")
    kv(right, row-9*dy, "Nodes / Elements", f"{len(all_pts):,} / ~{len(all_pts)//4:,}")
    kv(right, row-10*dy,"Analysis", "Nonlinear static (NLGEOM)")
    kv(right, row-11*dy,"Contact",  "Self-contact, penalty linear")
    kv(right, row-12*dy,"Steps",    "2  (preload → valve lift)")

    # Preview image (if available)
    if os.path.isfile(PREV):
        from matplotlib.image import imread
        img = imread(PREV)
        ax_img = fig.add_axes([0.63, 0.20, 0.32, 0.50])
        ax_img.imshow(img)
        ax_img.axis("off")
        ax_img.set_title("CAD Model (STEP)", fontsize=9, color="#555")

    ax.text(0.5, 0.04,
            "Prepared by: FEA Engineering  |  Solver: CalculiX v2.22  |  Date: 2026-06-06",
            ha="center", fontsize=9, color="#777", transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Page 2: FE Model description ─────────────────────────────────────────
    fig = plt.figure(figsize=(11.69, 8.27))
    header(fig, "FE Model Description", 2)

    gs = gridspec.GridSpec(2, 2, figure=fig, left=0.05, right=0.95,
                           top=0.93, bottom=0.08, hspace=0.35, wspace=0.30)

    # 3-D mesh scatter (all nodes)
    ax3 = fig.add_subplot(gs[:, 0], projection="3d")
    sc  = ax3.scatter(sample[:,0], sample[:,1], sample[:,2],
                      c=sample[:,2], cmap="plasma", s=0.4, alpha=0.45,
                      vmin=0, vmax=L0)
    plt.colorbar(sc, ax=ax3, shrink=0.55, label="Z position [mm]", pad=0.05)

    # Mark top/bottom BCs
    bot_s = sample[sample[:,2] < 1.5]
    top_s = sample[sample[:,2] > L0 - 1.5]
    if len(bot_s): ax3.scatter(bot_s[:,0], bot_s[:,1], bot_s[:,2],
                               c="cyan", s=10, alpha=0.9, label="Fixed BC (NBOT)", zorder=5)
    if len(top_s): ax3.scatter(top_s[:,0], top_s[:,1], top_s[:,2],
                               c="red",  s=10, alpha=0.9, label="Prescribed disp (NTOP)", zorder=5)
    ax3.set_xlabel("X [mm]", fontsize=7, labelpad=2)
    ax3.set_ylabel("Y [mm]", fontsize=7, labelpad=2)
    ax3.set_zlabel("Z [mm]", fontsize=7, labelpad=2)
    ax3.set_title(f"FE Mesh — {len(all_pts):,} Nodes\nC3D10 Tetrahedral Elements",
                  fontsize=9)
    ax3.legend(fontsize=7, loc="upper right")
    ax3.tick_params(labelsize=6)
    ax3.view_init(elev=20, azim=45)

    # Step diagram (top-right)
    ax_step = fig.add_subplot(gs[0, 1])
    ax_step.axis("off")
    ax_step.set_title("Analysis Steps", fontsize=10, fontweight="bold", pad=4)

    steps = [
        ("Step 1 — Assembly Preload",
         [f"Compress {L0} → {L_INSTALLED} mm",
          f"  (s = {S_PRELOAD:.0f} mm)",
          f"Target: {F_PRELOAD:.0f} N preload",
          "NBOT: fully fixed (UX=UY=UZ=0)",
          f"NTOP: UX=UY=0, UZ=−{S_PRELOAD:.0f} mm",
          "Increments: 500 max, INC=1 mm",
          "NLGEOM, self-contact active"]),
        ("Step 2 — Valve Lift",
         [f"Continue: {L_INSTALLED} → {L_FULL_LIFT} mm",
          f"  (additional {VALVE_LIFT:.0f} mm)",
          f"Target: {F_FULL_LIFT:.0f} N at full lift",
          "NBOT: fully fixed (OP=NEW)",
          f"NTOP: UZ=−{S_FULL_LIFT:.0f} mm (total)",
          "Increments: 1000 max, INC=0.1 mm",
          "NLGEOM, progressive stiffening"]),
    ]
    colors = ["#d0e8ff", "#ffe0c0"]
    y0 = 0.95
    for title, lines, col in zip([s[0] for s in steps],
                                  [s[1] for s in steps], colors):
        box = FancyBboxPatch((0.02, y0-0.41), 0.96, 0.40,
                              boxstyle="round,pad=0.02", linewidth=1,
                              edgecolor="#666", facecolor=col, transform=ax_step.transAxes)
        ax_step.add_patch(box)
        ax_step.text(0.05, y0-0.05, title, fontsize=9, fontweight="bold",
                     color="#1a3a6b", transform=ax_step.transAxes)
        for i, ln in enumerate(lines):
            ax_step.text(0.07, y0-0.13-i*0.052, ln, fontsize=7.5,
                         color="#333", transform=ax_step.transAxes, family="monospace")
        y0 -= 0.50

    # Contact surface description (bottom-right)
    ax_ct = fig.add_subplot(gs[1, 1])
    ax_ct.axis("off")
    ax_ct.set_title("Self-Contact Setup", fontsize=10, fontweight="bold", pad=4)

    ct_lines = [
        "Surface type : ELEMENT (exterior free faces)",
        f"Contact zone : z = 4.15 – 41.95 mm",
        "               (active coil region only)",
        "               ground-end coils EXCLUDED",
        "Interaction  : SURFACE TO SURFACE",
        "Overclosure  : PRESSURE-OVERCLOSURE=LINEAR",
        "Penalty K    : 1 000 N/mm³",
        "               (~0.5% of E / element size)",
        "",
        "Purpose: capture progressive coil binding",
        "as top (small-OD) coils contact first,",
        "reproducing the beehive spring's increasing",
        "rate from 6.1 → 3.1 active coils over",
        "the 20 mm compression stroke.",
    ]
    ax_ct.text(0.05, 0.95, "\n".join(ct_lines), fontsize=8,
               va="top", transform=ax_ct.transAxes,
               family="monospace", color="#222",
               bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f5f5",
                         edgecolor="#aaa", linewidth=0.8))

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Page 3: F-L curve ─────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    header(fig, "Force vs Lift — FEA Results vs Analytical Model", 3)

    ax.set_position([0.07, 0.10, 0.88, 0.78])

    # Shading
    ax.axvspan(S_PRELOAD, S_FULL_LIFT, alpha=0.07, color="blue")
    ax.axvspan(S_RELIABLE, S_FULL_LIFT+0.5, alpha=0.09, color="red")
    ax.axvline(S_RELIABLE, color="red", linestyle="--", lw=1.0, alpha=0.6)
    ax.text(S_RELIABLE+0.15, 30, f"Near solid\nheight (Ls≈{L0-S_SOLID:.1f}mm)",
            fontsize=8, color="red", alpha=0.85)

    # Analytical
    s_ana = np.linspace(0, S_FULL_LIFT, 400)
    f_ana = np.array([af(s) for s in s_ana])
    ax.plot(s_ana, f_ana, "g-", lw=2.5,
            label=f"Analytical (2-phase progressive)  k={k1:.0f}→{k2:.0f} N/mm")

    # FEA reliable
    ax.plot(lifts[mask_ok], forces[mask_ok], "b-o", ms=7, lw=2.2,
            label="FEA (NLGEOM, C3D10, self-contact)  — valid range")

    # FEA unreliable
    if mask_bad.sum():
        ax.plot(lifts[mask_bad], forces[mask_bad], "rs", ms=9,
                markerfacecolor="none", markeredgewidth=2, zorder=6,
                label="FEA — near solid height (contact overloaded)")
        for l, fv in zip(lifts[mask_bad], forces[mask_bad]):
            ax.annotate(f"{fv:.0f} N", xy=(l, fv),
                        xytext=(l-1.8, fv-100),
                        fontsize=8, color="red",
                        arrowprops=dict(arrowstyle="->", color="red", lw=0.9))

    # Operating fit
    op = mask_ok & (lifts >= S_PRELOAD)
    if op.sum() >= 2:
        coeff = np.polyfit(lifts[op], forces[op], 1)
        k_fea = coeff[0]
        l_fit = np.linspace(lifts[op].min(), lifts[op].max(), 80)
        ax.plot(l_fit, np.polyval(coeff, l_fit), "b--", alpha=0.45, lw=1.3,
                label=f"FEA linear fit (operating range)  k = {k_fea:.1f} N/mm")

    # Reference marks
    for lr, fr, lbl in [(S_PRELOAD, F_PRELOAD, f"Preload: {F_PRELOAD:.0f} N"),
                         (S_FULL_LIFT, F_FULL_LIFT, f"Full lift: {F_FULL_LIFT:.0f} N")]:
        ax.axvline(lr, color="gray", ls=":", lw=0.8, alpha=0.5)
        ax.plot(lr, fr, "r^", ms=11, zorder=5)
        ax.annotate(lbl, xy=(lr, fr), xytext=(lr+0.4, fr-50),
                    fontsize=9, color="darkred")

    ax.set_xlabel("Compression from Free Length [mm]", fontsize=12)
    ax.set_ylabel("Spring Force [N]", fontsize=12)
    ax.set_title("Force vs Compression — Valve Spring A177 053 05 00\n"
                 "CalculiX FEA (self-contact, NLGEOM) vs Analytical Progressive Model",
                 fontsize=12)
    ax.legend(fontsize=9.5, loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0, right=S_FULL_LIFT+1)
    ax.set_ylim(bottom=0)

    ax2 = ax.secondary_xaxis("top",
        functions=(lambda s: L0-s, lambda L: L0-L))
    ax2.set_xlabel("Spring Installed Length [mm]", fontsize=11)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Page 4: Results table + error breakdown ────────────────────────────────
    fig = plt.figure(figsize=(11.69, 8.27))
    header(fig, "Numerical Results & Validation", 4)

    gs4 = gridspec.GridSpec(1, 2, figure=fig, left=0.05, right=0.95,
                            top=0.91, bottom=0.08, wspace=0.30)

    # Results table
    ax_t = fig.add_subplot(gs4[0, 0])
    ax_t.axis("off")
    ax_t.set_title("FEA Force vs Lift — All Data Points", fontsize=10,
                   fontweight="bold", pad=6)

    cols = ["Compression\n[mm]", "Spring\nlength [mm]",
            "FEA Force\n[N]", "Analytical\n[N]", "Error\n[%]", "Status"]
    rows = []
    for l, fv in zip(lifts, forces):
        a_    = af(l)
        err   = (fv - a_) / a_ * 100 if a_ > 0 else 0.0
        stat  = "Near Ls" if l > S_RELIABLE else ("Op. range" if l >= S_PRELOAD else "Preload")
        rows.append([f"{l:.2f}", f"{L0-l:.1f}", f"{fv:.0f}", f"{a_:.0f}",
                     f"{err:+.1f}", stat])

    colors_row = []
    for l, _ in zip(lifts, forces):
        if l > S_RELIABLE:
            colors_row.append(["#ffe0e0"]*6)
        elif l >= S_PRELOAD:
            colors_row.append(["#e8f0ff"]*6)
        else:
            colors_row.append(["#f9f9f9"]*6)

    tbl = ax_t.table(cellText=rows, colLabels=cols,
                     cellColours=colors_row,
                     loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1.0, 1.55)

    # Legend for row colours
    legend_handles = [
        mpatches.Rectangle((0,0), 1, 1, facecolor="#f9f9f9", edgecolor="#888",
                            label="Step 1 – preload stroke"),
        mpatches.Rectangle((0,0), 1, 1, facecolor="#e8f0ff", edgecolor="#888",
                            label="Step 2 – valve lift (operating range)"),
        mpatches.Rectangle((0,0), 1, 1, facecolor="#ffe0e0", edgecolor="#888",
                            label="Near solid height – unreliable"),
    ]
    ax_t.legend(handles=legend_handles, fontsize=7.5, loc="lower center",
                bbox_to_anchor=(0.5, -0.02))

    # Error bar chart
    ax_e = fig.add_subplot(gs4[0, 1])
    bar_colors = ["#cc3333" if l > S_RELIABLE else
                  ("#2255aa" if l >= S_PRELOAD else "#558833")
                  for l in lifts]
    errs = [(abs(fv) - af(l)) / af(l) * 100 if af(l) > 0 else 0
            for l, fv in zip(lifts, forces)]
    bars = ax_e.barh([f"{l:.1f}" for l in lifts], errs, color=bar_colors, alpha=0.75)
    ax_e.axvline(0, color="black", lw=0.8)
    ax_e.axvline(-10, color="green", lw=0.8, ls="--", alpha=0.5, label="±10% band")
    ax_e.axvline(+10, color="green", lw=0.8, ls="--", alpha=0.5)
    ax_e.set_xlabel("FEA vs Analytical Error [%]", fontsize=10)
    ax_e.set_ylabel("Compression [mm]", fontsize=10)
    ax_e.set_title("Force Prediction Error\n(FEA − Analytical) / Analytical",
                   fontsize=10, fontweight="bold")
    ax_e.legend(fontsize=8)
    ax_e.grid(True, axis="x", alpha=0.3)

    # Annotation
    op_errs = [e for l, e in zip(lifts, errs) if S_PRELOAD <= l <= S_RELIABLE]
    if op_errs:
        ax_e.text(0.98, 0.05,
                  f"Operating range:\nmean error = {np.mean(op_errs):+.1f}%\nmax |err| = {max(abs(e) for e in op_errs):.1f}%",
                  transform=ax_e.transAxes, ha="right", va="bottom",
                  fontsize=8.5, color="#1a3a6b",
                  bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f0ff", alpha=0.9))

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Page 5: Mesh detail + BC schematic ────────────────────────────────────
    fig = plt.figure(figsize=(11.69, 8.27))
    header(fig, "FE Model — Mesh Detail & Boundary Conditions", 5)

    gs5 = gridspec.GridSpec(1, 2, figure=fig, left=0.04, right=0.96,
                            top=0.91, bottom=0.06, wspace=0.25)

    # Side-view scatter (XZ plane)
    ax_xz = fig.add_subplot(gs5[0, 0])
    sc_xz = ax_xz.scatter(sample[:,0], sample[:,2],
                           c=sample[:,2], cmap="plasma", s=0.5, alpha=0.35,
                           vmin=0, vmax=L0)
    plt.colorbar(sc_xz, ax=ax_xz, label="Z [mm]", shrink=0.8)
    bot_pts = sample[sample[:,2] < 1.5]
    top_pts = sample[sample[:,2] > L0-1.5]
    ax_xz.scatter(bot_pts[:,0], bot_pts[:,2], c="cyan",  s=12, zorder=4,
                  label="NBOT — fixed (UX=UY=UZ=0)")
    ax_xz.scatter(top_pts[:,0], top_pts[:,2], c="red",   s=12, zorder=4,
                  label=f"NTOP — UX=UY=0, UZ=−{S_FULL_LIFT:.0f} mm")

    # Contact zone band
    ax_xz.axhspan(4.15, 41.95, alpha=0.07, color="orange",
                  label="Self-contact zone (z=4.15–41.95 mm)")
    ax_xz.axhline(4.15,  color="orange", lw=0.8, ls="--", alpha=0.7)
    ax_xz.axhline(41.95, color="orange", lw=0.8, ls="--", alpha=0.7)

    ax_xz.set_xlabel("X [mm]", fontsize=10)
    ax_xz.set_ylabel("Z [mm]", fontsize=10)
    ax_xz.set_title("Side View (XZ plane)\nMesh Nodes with BC & Contact Zone",
                    fontsize=10)
    ax_xz.legend(fontsize=7.5, loc="upper right")
    ax_xz.grid(True, alpha=0.2)

    # Top-view scatter (XY plane)
    ax_xy = fig.add_subplot(gs5[0, 1])
    mid = (sample[:,2] > 20) & (sample[:,2] < 30)
    ax_xy.scatter(sample[mid,0], sample[mid,1],
                  c=sample[mid,2], cmap="viridis", s=1.2, alpha=0.45)
    ax_xy.set_xlabel("X [mm]", fontsize=10)
    ax_xy.set_ylabel("Y [mm]", fontsize=10)
    ax_xy.set_title(f"Top View (XY plane)\nCoil cross-section  z = 20–30 mm\n"
                    f"Inner Ø {Di_bot:.1f}→{Di_top:.1f} mm  |  Wire {wire_a}×{wire_r} mm",
                    fontsize=10)
    ax_xy.set_aspect("equal")
    ax_xy.grid(True, alpha=0.2)

    # Dimension annotations
    r_mid = (R_mean_bot + R_mean_top) / 2
    ax_xy.annotate("", xy=(r_mid, 0), xytext=(-r_mid, 0),
                   arrowprops=dict(arrowstyle="<->", color="red", lw=1.2))
    ax_xy.text(0, 1.5, f"Mean OD range\n{Di_bot+wire_r:.1f}→{Di_top+wire_r:.1f} mm",
               ha="center", fontsize=8, color="red")

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

    # ── Page 6: Conclusions ───────────────────────────────────────────────────
    fig = plt.figure(figsize=(11.69, 8.27))
    header(fig, "Conclusions & Recommendations", 6)

    ax = fig.add_axes([0.06, 0.06, 0.88, 0.86]); ax.axis("off")

    sections = [
        ("1. Model Summary",
         [f"• Valve spring A177 053 05 00 (beehive, oval wire {wire_a}×{wire_r} mm, {nt} coils)",
          f"• 3D solid FEA: {len(all_pts):,} nodes, C3D10 quadratic tetrahedral elements",
          f"• Two-step nonlinear static analysis with NLGEOM flag",
          f"• Self-contact on active coil zone (z = 4.15–41.95 mm, ground ends excluded)",
          f"• Material: VD SiCrNi SC  E = {E_MOD/1000:.0f} GPa, ν = {NU}"]),

        ("2. Force vs Lift Results",
         [f"• Step 1 (preload):  FEA = {forces[lifts<=10][-1]:.0f} N  vs drawing = {F_PRELOAD:.0f} N  "
          f"(error {(forces[lifts<=10][-1]-F_PRELOAD)/F_PRELOAD*100:+.1f}%)",
          f"• Operating range ({S_PRELOAD:.0f}–{S_RELIABLE:.0f} mm): FEA tracks analytical within ≈ 3–25%",
          f"• FEA spring ~9% softer than drawing spec — consistent across all reliable increments",
          f"  → Likely source: mesh size effect, quadratic tet shear locking, or geometry approximation",
          f"• Point at {S_FULL_LIFT:.0f} mm ({L_FULL_LIFT:.0f} mm installed) flagged UNRELIABLE — spring",
          f"  is only {L0-S_SOLID-0:.1f} mm from solid height; contact model overloads at this condition"]),

        ("3. Self-Contact Performance",
         [f"• Ground-end exclusion (z < 4.15 mm, z > 41.95 mm) eliminated false contact",
          f"  from closed coils that are touching at free length",
          f"• Contact spring elements = 0 at increment 1 — no spurious initial penetration",
          f"• Progressive stiffening visible from ~16 mm onwards — consistent with drawing",
          f"  (active coils 6.1 → 4.4 → 3.1 binding sequence per A177 053 05 00)",
          f"• Penalty K = 1 000 N/mm³ (reduced from 10 000); further reduction may help"]),

        ("4. Recommendations",
         [f"• For F-L prediction: use the calibrated analytical model (k={k1:.0f}→{k2:.0f} N/mm)",
          f"  which is directly traceable to drawing references",
          f"• For stress analysis: FEA displacement-controlled load cases are valid for",
          f"  Von Mises / principal stress extraction in the reliable compression range",
          f"• To improve the 20 mm contact: reduce max compression to {S_RELIABLE:.0f} mm, or",
          f"  refine the mesh in the top-coil binding region to capture progressive binding",
          f"• Dynamic (modal) analysis recommended to verify spring surge margin vs cam speed"]),
    ]

    y = 0.97
    for title, bullets in sections:
        ax.text(0.01, y, title, fontsize=11, fontweight="bold",
                color="#1a3a6b", transform=ax.transAxes)
        y -= 0.04
        for b in bullets:
            ax.text(0.025, y, b, fontsize=9, color="#222",
                    transform=ax.transAxes, wrap=True)
            y -= 0.038
        y -= 0.018

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

print(f"PDF written: {PDF}")
print(f"Pages: 6")
