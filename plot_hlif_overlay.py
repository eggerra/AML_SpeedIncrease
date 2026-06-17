"""
plot_hlif_overlay.py
====================
Overlays the steady-state HLA lift profile for ALL 16 intake HLIF elements
across ALL simulated speed cases on a single set of panels.

Each GID file holds the last (steady-state) cam cycle (0-360°) for that
speed. Overlaying all speed traces per element immediately shows:
  - Pump-up onset: elevated lift baseline on the base-circle at higher speeds
  - Amplitude differences: valve-lift peak reduction due to HLA extension
  - Cylinder-to-cylinder spread within each bank

Outputs
-------
  hlif_overlay_INTL.png   — 2×4 grid, left-bank elements INTL_HLIF1–8
  hlif_overlay_INTr.png   — 2×4 grid, right-bank elements INTr_HLIF1–8
  hlif_overlay_summary.png — 1 combined panel showing all elements both banks

All figures are embedded in a new PDF section and merged into
AML_Valvetrain_Model_Analysis.pdf, then pushed to the excite_td git branch.

Usage
-----
  python plot_hlif_overlay.py
"""

import os, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether, PageBreak,
)

from pypdf import PdfWriter, PdfReader

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE    = r"D:\Projects_AI\AML_SpeedIncrease"
ETD_DIR = r"D:\AW82001\5005\excite_td"
MODEL   = "AML_AE26_ChainDrive__04_spring_update"
CASESET = f"{MODEL}.EngineSpeed"

MAIN_PDF   = os.path.join(BASE, "AML_Valvetrain_Model_Analysis.pdf")
SEC_PDF    = os.path.join(BASE, "_hlif_overlay_section.pdf")
OUTPUT_PDF = os.path.join(BASE, "AML_Valvetrain_Model_Analysis.pdf")

FIG_INTL   = os.path.join(BASE, "hlif_overlay_INTL.png")
FIG_INTr   = os.path.join(BASE, "hlif_overlay_INTr.png")
FIG_SUM    = os.path.join(BASE, "hlif_overlay_summary.png")

# ── Channel mapping ───────────────────────────────────────────────────────────
INTL = {f"INTL_HLIF{i}": f"HLIF_{n}"
        for i, n in enumerate([282,290,302,310,318,326,334,342], 1)}
INTr = {f"INTr_HLIF{i}":  f"HLIF_{n}"
        for i, n in enumerate([63,71,83,91,99,107,115,123], 1)}
INTAKE_HLIF = {**INTL, **INTr}

COL_CAM  = 1   # equiv. cam angle [deg]
COL_LIFT = 4   # HLA plunger lift  [m]
COL_FORCE= 7   # contact force [N]

PUMP_UP_THRESHOLD_MM = 0.10   # mm: min-lift above this → pump-up flag

# ── Colour palette ────────────────────────────────────────────────────────────
DARK_BLUE  = "#0D2B55"
MID_BLUE   = "#1A4B8C"
LIGHT_BLUE = "#D6E4F7"
ACCENT_RED = "#C0392B"
STRIPE     = "#EBF2FB"

# Speed → colour  (consistent across all plots)
SPEED_COLOR = {
    7000: "#2471A3",   # blue
    7500: "#1E8449",   # green
    7600: "#D4AC0D",   # yellow-gold
    7700: "#CB4335",   # red
    7800: "#7D3C98",   # purple
}
SPEED_LW = {7000: 1.5, 7500: 1.5, 7600: 1.8, 7700: 2.0, 7800: 2.2}
SPEED_LS = {7000: ":", 7500: "--", 7600: "-.", 7700: "-", 7800: "-"}


# ── GID reader ────────────────────────────────────────────────────────────────
def read_gid(filepath):
    with open(filepath, "r", errors="replace") as f:
        raw = f.read()
    end_idx = raw.find("\nEND")
    header  = raw[:end_idx] if end_idx > 0 else raw[:3000]
    body    = raw[end_idx+4:] if end_idx > 0 else ""
    ch_m = re.search(r"CHANNEL\s*=\s*\[([^\]]+)\]", header, re.DOTALL)
    channels = re.findall(r"'([^']+)'", ch_m.group(1)) if ch_m else []
    ncols = len(channels)
    if ncols == 0:
        return np.zeros((0, 0))
    rows = []
    for line in body.splitlines():
        parts = line.split()
        if len(parts) >= ncols:
            try:
                rows.append([float(v) for v in parts[:ncols]])
            except ValueError:
                continue
    return np.array(rows) if rows else np.zeros((0, ncols))


def load_all():
    """Return dict: all_data[rpm][elem] = ndarray or None."""
    speeds = sorted([
        int(re.search(r"\.(\d+)rpm$", d).group(1))
        for d in os.listdir(ETD_DIR)
        if os.path.isdir(os.path.join(ETD_DIR, d))
        and d.startswith(CASESET + ".")
        and re.search(r"\.\d+rpm$", d)
    ])
    print(f"Speed cases: {speeds}")
    all_data = {}
    for rpm in speeds:
        all_data[rpm] = {}
        res_dir = os.path.join(ETD_DIR, f"{CASESET}.{rpm}rpm", "results")
        for elem, gid in INTAKE_HLIF.items():
            path = os.path.join(res_dir, f"{gid}.GID")
            if os.path.isfile(path):
                d = read_gid(path)
                all_data[rpm][elem] = d if d.shape[0] > 5 and d.shape[1] > COL_LIFT else None
            else:
                all_data[rpm][elem] = None
    return speeds, all_data


# ── Style helpers ─────────────────────────────────────────────────────────────
def _apply_subplot_style(ax, elem_name, ylabel=True):
    bank = "LB" if elem_name.startswith("INTL") else "RB"
    cyl  = re.search(r"HLIF(\d+)", elem_name).group(1)
    ax.set_title(f"Cyl {cyl} ({bank})", fontsize=9, color=MID_BLUE,
                 fontweight="bold", pad=3)
    ax.set_xlabel("Cam angle [°]", fontsize=7.5, labelpad=2)
    if ylabel:
        ax.set_ylabel("HLA lift [mm]", fontsize=7.5, labelpad=2)
    ax.tick_params(labelsize=7)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(90))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(45))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
    ax.grid(True, which="major", ls="--", alpha=0.30, lw=0.6)
    ax.grid(True, which="minor", ls=":", alpha=0.12, lw=0.4)
    # pump-up threshold line
    ax.axhline(PUMP_UP_THRESHOLD_MM, color=ACCENT_RED, lw=0.7,
               ls="--", alpha=0.55, zorder=1)
    ax.set_xlim(0, 360)


def _speed_legend_handles(speeds):
    return [
        Line2D([0], [0],
               color=SPEED_COLOR.get(s, "grey"),
               lw=SPEED_LW.get(s, 1.5),
               ls=SPEED_LS.get(s, "-"),
               label=f"{s} rpm")
        for s in speeds if s in SPEED_COLOR
    ]


# ── Figure 1 & 2: per-bank 2×4 grids ─────────────────────────────────────────
def plot_bank(bank_dict, bank_label, speeds, all_data, savepath, figsize=(16, 9)):
    """
    2-row × 4-col grid showing one subplot per element.
    Each subplot overlays all available speed traces.
    """
    elem_list = sorted(bank_dict.keys(),
                       key=lambda e: int(re.search(r"HLIF(\d+)", e).group(1)))

    fig, axes = plt.subplots(2, 4, figsize=figsize,
                             sharex=True, sharey=False)
    fig.patch.set_facecolor("#F8FAFD")

    # Super-title
    fig.suptitle(
        f"Intake HLA Lift — Steady-State Cam Cycle Overlay\n"
        f"{bank_label}  ·  Model: {MODEL}",
        fontsize=12, fontweight="bold", color=DARK_BLUE, y=1.01
    )

    # Shared y-range across all subplots for easy comparison
    global_min, global_max = np.inf, -np.inf

    for ax, elem in zip(axes.flat, elem_list):
        plotted_any = False
        for rpm in speeds:
            d = all_data[rpm].get(elem)
            if d is None or d.shape[0] < 5:
                continue
            cam  = d[:, COL_CAM]
            lift = d[:, COL_LIFT] * 1e3   # m → mm
            ax.plot(cam, lift,
                    color=SPEED_COLOR.get(rpm, "grey"),
                    lw=SPEED_LW.get(rpm, 1.5),
                    ls=SPEED_LS.get(rpm, "-"),
                    alpha=0.88, zorder=2 + speeds.index(rpm))
            global_min = min(global_min, lift.min())
            global_max = max(global_max, lift.max())
            plotted_any = True

        col_idx = list(axes.flat).index(ax) % 4
        _apply_subplot_style(ax, elem, ylabel=(col_idx == 0))

        if not plotted_any:
            ax.text(180, 0.05, "No data", ha="center", va="center",
                    color="grey", fontsize=8)

    # Shared y-axis with margin
    if global_max > global_min:
        margin = (global_max - global_min) * 0.10
        y0 = max(0, global_min - margin)
        y1 = global_max + margin + 0.02
        for ax in axes.flat:
            ax.set_ylim(y0, y1)

    # Shared legend
    handles = _speed_legend_handles(speeds)
    handles.append(Line2D([0], [0], color=ACCENT_RED, lw=0.9, ls="--",
                           alpha=0.7, label=f"Pump-up limit {PUMP_UP_THRESHOLD_MM} mm"))
    fig.legend(handles=handles, loc="lower center",
               ncol=len(handles), fontsize=8.5,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.04))

    fig.tight_layout(rect=[0, 0.04, 1, 0.99])
    fig.savefig(savepath, dpi=160, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved: {savepath}")


# ── Figure 3: summary — all 16 elements in one figure ────────────────────────
def plot_summary(speeds, all_data, savepath, figsize=(22, 12)):
    """
    4-row × 8-col grid: row 0-1 = INTL_HLIF1-8, row 2-3 = INTr_HLIF1-8.
    All speed traces overlaid, colour-coded by speed.
    """
    intl_list = [f"INTL_HLIF{i}" for i in range(1, 9)]
    intr_list = [f"INTr_HLIF{i}"  for i in range(1, 9)]
    all_elems = intl_list + intr_list   # 16 total

    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor("#F4F6F9")

    # Title + bank labels via text
    fig.suptitle(
        f"Intake HLA Lift — All 16 Elements · All Speed Cases  |  {MODEL}",
        fontsize=13, fontweight="bold", color=DARK_BLUE, y=0.995
    )

    gs = GridSpec(2, 8, figure=fig, hspace=0.55, wspace=0.30,
                  left=0.05, right=0.99, top=0.94, bottom=0.10)

    # track global y range per bank row for shared scaling
    bank_ranges = {0: [np.inf, -np.inf], 1: [np.inf, -np.inf]}
    ax_list = []

    for row, elem_group in enumerate([intl_list, intr_list]):
        bank_label = "Left bank (INTL)" if row == 0 else "Right bank (INTr)"
        fig.text(0.005, 0.725 - row * 0.47, bank_label,
                 ha="left", va="center", fontsize=9.5,
                 fontweight="bold", color=MID_BLUE, rotation=90)

        for col, elem in enumerate(elem_group):
            ax = fig.add_subplot(gs[row, col])
            ax_list.append((ax, row))
            cyl = int(re.search(r"HLIF(\d+)", elem).group(1))

            for rpm in speeds:
                d = all_data[rpm].get(elem)
                if d is None or d.shape[0] < 5:
                    continue
                cam  = d[:, COL_CAM]
                lift = d[:, COL_LIFT] * 1e3
                ax.plot(cam, lift,
                        color=SPEED_COLOR.get(rpm, "grey"),
                        lw=SPEED_LW.get(rpm, 1.4),
                        ls=SPEED_LS.get(rpm, "-"),
                        alpha=0.88)
                bank_ranges[row][0] = min(bank_ranges[row][0], lift.min())
                bank_ranges[row][1] = max(bank_ranges[row][1], lift.max())

            # pump-up limit
            ax.axhline(PUMP_UP_THRESHOLD_MM, color=ACCENT_RED, lw=0.55,
                       ls="--", alpha=0.5)

            # Title and axes labels
            ax.set_title(f"CYL {cyl}", fontsize=8, color=MID_BLUE,
                         fontweight="bold", pad=2)
            ax.tick_params(labelsize=6.5)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(120))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(60))
            ax.grid(True, which="major", ls="--", alpha=0.25, lw=0.5)
            ax.set_xlim(0, 360)

            if col == 0:
                ax.set_ylabel("Lift [mm]", fontsize=7, labelpad=2)
            else:
                ax.yaxis.set_tick_params(labelleft=False)
            if row == 1:
                ax.set_xlabel("Cam [°]", fontsize=7, labelpad=1)

    # Apply shared y-range per bank row
    for ax, row in ax_list:
        lo, hi = bank_ranges[row]
        if hi > lo:
            m = (hi - lo) * 0.08
            ax.set_ylim(max(0, lo - m), hi + m + 0.015)

    # Legend
    handles = _speed_legend_handles(speeds)
    handles.append(Line2D([0], [0], color=ACCENT_RED, lw=0.9, ls="--",
                           alpha=0.65, label=f"Limit {PUMP_UP_THRESHOLD_MM} mm"))
    fig.legend(handles=handles, loc="lower center", ncol=len(handles),
               fontsize=8.5, framealpha=0.92, bbox_to_anchor=(0.5, 0.005))

    fig.savefig(savepath, dpi=160, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved: {savepath}")


# ── Figure 4: min-lift per element per speed (pump-up bar chart) ──────────────
def plot_pumpup_bars(speeds, all_data, savepath, figsize=(14, 5)):
    """
    Bar chart: min lift in steady-state cycle per element per speed.
    Bars above threshold = pump-up condition.
    """
    intl_list = [f"INTL_HLIF{i}" for i in range(1, 9)]
    intr_list = [f"INTr_HLIF{i}"  for i in range(1, 9)]

    fig, axes = plt.subplots(1, 2, figsize=figsize, sharey=True)
    fig.patch.set_facecolor("#F8FAFD")
    fig.suptitle(
        "Min HLA Lift on Base Circle — Pump-Up Indicator\n"
        f"(Steady-state cam cycle per speed  |  {MODEL})",
        fontsize=11, fontweight="bold", color=DARK_BLUE, y=1.01
    )

    valid_speeds = [s for s in speeds if any(
        all_data[s].get(e) is not None for e in intl_list)]

    n_spd = len(valid_speeds)
    bar_w = 0.7 / max(n_spd, 1)
    offsets = np.linspace(-0.35 + bar_w/2, 0.35 - bar_w/2, n_spd) if n_spd > 1 else [0.0]

    for ax, elem_list, bank_label in zip(
            axes, [intl_list, intr_list], ["Left bank (INTL)", "Right bank (INTr)"]):
        x = np.arange(len(elem_list))
        for si, (rpm, off) in enumerate(zip(valid_speeds, offsets)):
            mins = []
            for elem in elem_list:
                d = all_data[rpm].get(elem)
                if d is not None and d.shape[0] > 5:
                    mins.append(float(np.min(d[:, COL_LIFT])) * 1e3)
                else:
                    mins.append(0.0)

            bars = ax.bar(x + off, mins, width=bar_w * 0.90,
                          color=SPEED_COLOR.get(rpm, "grey"),
                          alpha=0.80, label=f"{rpm} rpm",
                          edgecolor="white", linewidth=0.5)

            # Outline bars that exceed pump-up threshold in red
            for bar, val in zip(bars, mins):
                if val > PUMP_UP_THRESHOLD_MM:
                    bar.set_edgecolor(ACCENT_RED)
                    bar.set_linewidth(1.5)

        ax.axhline(PUMP_UP_THRESHOLD_MM, color=ACCENT_RED, lw=1.2,
                   ls="--", alpha=0.8, zorder=5,
                   label=f"Limit {PUMP_UP_THRESHOLD_MM} mm")
        ax.axhspan(0, PUMP_UP_THRESHOLD_MM, color="#EAF5EA", alpha=0.4, zorder=0)
        ax.axhspan(PUMP_UP_THRESHOLD_MM, 1.0, color="#FDECEA", alpha=0.25, zorder=0)

        ax.set_title(bank_label, fontsize=10, color=MID_BLUE, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([f"CYL{i+1}" for i in range(len(elem_list))], fontsize=8)
        ax.set_ylabel("Min HLA lift [mm]", fontsize=9)
        ax.set_ylim(0, None)
        ax.grid(True, axis="y", ls="--", alpha=0.30)
        ax.legend(fontsize=8, loc="upper left", ncol=2)

    fig.tight_layout()
    fig.savefig(savepath, dpi=160, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved: {savepath}")


FIG_BARS = os.path.join(BASE, "hlif_pumpup_bars.png")


# ── PDF section ───────────────────────────────────────────────────────────────
DARK_BLUE_CL  = colors.HexColor(DARK_BLUE)
MID_BLUE_CL   = colors.HexColor(MID_BLUE)
LIGHT_BLUE_CL = colors.HexColor(LIGHT_BLUE)
ACCENT_RED_CL = colors.HexColor(ACCENT_RED)
STRIPE_CL     = colors.HexColor(STRIPE)


def _st():
    return {
        "h1": ParagraphStyle("h1", fontSize=14, textColor=DARK_BLUE_CL,
                              spaceBefore=12, spaceAfter=5,
                              fontName="Helvetica-Bold"),
        "h2": ParagraphStyle("h2", fontSize=11, textColor=MID_BLUE_CL,
                              spaceBefore=8, spaceAfter=3,
                              fontName="Helvetica-Bold"),
        "body": ParagraphStyle("body", fontSize=9, textColor=colors.black,
                                leading=14, alignment=TA_JUSTIFY,
                                fontName="Helvetica"),
        "note": ParagraphStyle("note", fontSize=7.5, textColor=colors.HexColor("#555"),
                                leading=12, fontName="Helvetica-Oblique"),
    }


def hdr_ftr(canvas, doc):
    W, H = A4
    canvas.saveState()
    canvas.setFillColor(DARK_BLUE_CL)
    canvas.rect(0, H - 22*mm, W, 22*mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(W/2, H - 13*mm,
        "AML Valvetrain Engineering — EXCITE TD HLA Lift Overlay")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LIGHT_BLUE_CL)
    canvas.drawRightString(W - 15*mm, H - 19*mm,
        f"{MODEL} | 2026-06-17")
    canvas.setFillColor(DARK_BLUE_CL)
    canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(15*mm, 3.5*mm, "Confidential — Internal Engineering Document")
    canvas.drawRightString(W - 15*mm, 3.5*mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf_section(speeds, all_data, out_path):
    st = _st()
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        topMargin=28*mm, bottomMargin=16*mm,
        leftMargin=15*mm, rightMargin=15*mm,
    )
    story = []

    # Section title banner
    ttbl = Table([[Paragraph(
        "5. HLA Lift Overlay — All Elements · All Speed Cases", st["h1"])]],
        colWidths=[180*mm])
    ttbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE_CL),
        ("TEXTCOLOR",  (0,0), (-1,-1), colors.white),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))
    story.append(ttbl)
    story.append(Spacer(1, 5*mm))

    # Intro
    story.append(Paragraph("5.1  Methodology", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    valid_speeds = [s for s in speeds
                    if any(all_data[s].get(f"INTL_HLIF{i}") is not None
                           for i in range(1, 9))]

    story.append(Paragraph(
        "AVL EXCITE TD stores the last (steady-state) cam cycle of each simulation "
        "run as a GID time-domain file.  For the <i>pump-up overlay</i>, the lift signal "
        "(HLA plunger displacement in mm) of each element is plotted against the "
        "cam angle (0–360°) for all available speed cases: "
        f"<b>{', '.join(str(s) + ' rpm' for s in valid_speeds)}</b>.  "
        "Each speed trace is colour-coded and line-style-coded.  "
        "Curves that do not return to the zero-line on the base circle (cam angle "
        "outside the valve-open window) indicate <b>pump-up</b> — the HLA has "
        "extended and cannot release all of the pumped-in oil volume within the "
        f"available base-circle dwell time.  The dashed red line marks the "
        f"{PUMP_UP_THRESHOLD_MM} mm detection threshold.",
        st["body"]))
    story.append(Spacer(1, 4*mm))

    # Figures
    story.append(Paragraph("5.2  Overlay Plots", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    W_full = 178*mm
    aspect_bank = 9.0 / 16.0   # figsize (16,9)
    aspect_sum  = 12.0 / 22.0  # figsize (22,12)
    aspect_bar  = 5.0 / 14.0   # figsize (14,5)

    figs = [
        (FIG_INTL, aspect_bank,
         "Fig. 5-1: Left bank — INTL_HLIF1–8.",
         "Each subplot shows the HLA lift over one full cam revolution (0–360°) "
         "for the left-bank intake elements.  Speed traces are overlaid; the "
         "dashed red line is the pump-up threshold.  Rising lift baselines at "
         "higher speeds indicate pump-up onset."),
        (FIG_INTr, aspect_bank,
         "Fig. 5-2: Right bank — INTr_HLIF1–8.",
         "Equivalent view for the right-bank intake elements.  Comparing "
         "left vs. right bank reveals any cam-phasing or supply-pressure "
         "asymmetry."),
        (FIG_SUM, aspect_sum,
         "Fig. 5-3: All 16 intake elements — combined overview.",
         "Full overview: 2 rows × 8 columns, top row = left bank, bottom row = "
         "right bank.  Shared colour coding allows direct cross-cylinder and "
         "cross-bank comparison at a glance."),
        (FIG_BARS, aspect_bar,
         "Fig. 5-4: Minimum HLA lift per element and speed (pump-up bar chart).",
         "The minimum lift value in the steady-state cycle is a direct measure "
         "of how much the HLA plunger has extended relative to its nominal zero "
         "position.  Bars exceeding the red dashed line are in pump-up condition."),
    ]

    for fig_path, asp, cap_title, cap_text in figs:
        if not os.path.isfile(fig_path):
            continue
        h = W_full * asp
        story.append(KeepTogether([
            Image(fig_path, width=W_full, height=h),
            Spacer(1, 1.5*mm),
            Paragraph(f"<b>{cap_title}</b>  {cap_text}", st["note"]),
            Spacer(1, 5*mm),
        ]))

    story.append(PageBreak())

    # Engineering notes
    story.append(Paragraph("5.3  Engineering Observations", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    # Count pump-up cases
    n_pu = 0
    pu_elems = []
    for elem in sorted(INTAKE_HLIF.keys()):
        for rpm in valid_speeds:
            d = all_data[rpm].get(elem)
            if d is not None and d.shape[0] > 5:
                min_lift = float(np.min(d[:, COL_LIFT])) * 1e3
                if min_lift > PUMP_UP_THRESHOLD_MM:
                    n_pu += 1
                    pu_elems.append(f"{elem}@{rpm}")

    obs_text = (
        f"Across {len(valid_speeds)} evaluated speed cases and 16 intake HLA elements "
        f"({len(valid_speeds) * 16} combinations total), "
        f"<b>{n_pu} element-speed combinations</b> exceed the "
        f"{PUMP_UP_THRESHOLD_MM} mm pump-up threshold.  "
    )
    if n_pu > 0:
        obs_text += (
            "Affected combinations: "
            + ", ".join(pu_elems[:10])
            + (f" … and {len(pu_elems)-10} more" if len(pu_elems) > 10 else "") + ".  "
            "The lift baseline elevation increases with engine speed, consistent with "
            "the shorter base-circle dwell time at higher RPM leaving insufficient "
            "time for the HLA to bleed down the pumped-up oil volume.  "
            "Cylinder-to-cylinder variation in pump-up magnitude may reflect "
            "differences in oil supply pressure or HLA bleed-down rates between "
            "cylinder positions."
        )
    else:
        obs_text += (
            "No pump-up is detected in any element across the full speed range. "
            "The updated spring (04_spring_update) seat load is sufficient to keep "
            "the HLA plunger in its nominal position throughout the base-circle dwell "
            "at all evaluated speeds."
        )
    story.append(Paragraph(obs_text, st["body"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        f"Source data: {MODEL}.etd — GID time-domain files (last steady-state cycle "
        f"per speed, post-processed by AVL Workspace R2024.1).  "
        f"Figures generated by plot_hlif_overlay.py — 2026-06-17.",
        st["note"]))

    doc.build(story, onFirstPage=hdr_ftr, onLaterPages=hdr_ftr)
    print(f"  PDF section: {out_path}")


# ── Merge PDFs ────────────────────────────────────────────────────────────────
def merge_pdfs(base_pdf, section_pdf, out_pdf):
    writer = PdfWriter()
    for src in [base_pdf, section_pdf]:
        if os.path.isfile(src):
            for page in PdfReader(src).pages:
                writer.add_page(page)
    with open(out_pdf, "wb") as f:
        writer.write(f)
    print(f"  Merged PDF: {out_pdf}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=== HLIF Lift Overlay ===")

    print("\n[1/4] Loading data ...")
    speeds, all_data = load_all()
    valid_speeds = [s for s in speeds
                    if any(all_data[s].get(f"INTL_HLIF{i}") is not None
                           for i in range(1, 9))]
    print(f"  Speeds with data: {valid_speeds}")

    print("\n[2/4] Generating figures ...")
    plot_bank(INTL, "Left bank (INTL_HLIF1–8)", valid_speeds, all_data, FIG_INTL)
    plot_bank(INTr, "Right bank (INTr_HLIF1–8)", valid_speeds, all_data, FIG_INTr)
    plot_summary(valid_speeds, all_data, FIG_SUM)
    plot_pumpup_bars(valid_speeds, all_data, FIG_BARS)

    print("\n[3/4] Building PDF section ...")
    build_pdf_section(speeds, all_data, SEC_PDF)

    print("\n[4/4] Merging PDFs ...")
    merge_pdfs(MAIN_PDF, SEC_PDF, OUTPUT_PDF)
    try:
        os.remove(SEC_PDF)
    except Exception:
        pass

    print("\nDone.")
    print(f"  Overlay figures: {os.path.basename(FIG_INTL)}, "
          f"{os.path.basename(FIG_INTr)}, {os.path.basename(FIG_SUM)}, "
          f"{os.path.basename(FIG_BARS)}")
    print(f"  Updated PDF: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
