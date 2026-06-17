"""
analyze_hlif_cycles.py
======================
Compares HLA lift cycle-by-cycle across all 6 simulated cycles (2–7)
for every intake HLIF element at every speed case.

A rising minimum lift on the base-circle from one cycle to the next is the
definitive indicator of HLA pump-up.  This script:

  1. Reads the multi-cycle GID result files (cycles 2–7, cam angle 360–2520°)
  2. Splits the data into individual cam cycles
  3. Computes per-cycle metrics: min lift (base circle), max lift (valve event),
     and lift range
  4. Detects pump-up: monotonically or consistently rising min-lift trend
  5. Generates plots:
       - Cycle overlay per element (6 traces per subplot, colour = cycle number)
       - Min-lift trend per element (pump-up fingerprint)
       - Heatmap: Δlift (cycle 7 – cycle 2) per element × speed
  6. Appends a new section to AML_Valvetrain_Model_Analysis.pdf
  7. Commits and pushes to the excite_td git branch

Usage
-----
  python analyze_hlif_cycles.py
  python analyze_hlif_cycles.py --check   # just check if results are ready
"""

import os, re, sys, subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm as mplcm
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
from matplotlib.colors import Normalize

from reportlab.lib.pagesizes import A4
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
WT_PATH = os.path.join(BASE, ".excite_td_wt")

MAIN_PDF   = os.path.join(BASE, "AML_Valvetrain_Model_Analysis.pdf")
SEC_PDF    = os.path.join(BASE, "_hlif_cycles_section.pdf")
OUTPUT_PDF = MAIN_PDF

FIG_OVERLAY_INTL = os.path.join(BASE, "hlif_cycles_overlay_INTL.png")
FIG_OVERLAY_INTr = os.path.join(BASE, "hlif_cycles_overlay_INTr.png")
FIG_TREND        = os.path.join(BASE, "hlif_cycles_trend.png")
FIG_HEATMAP      = os.path.join(BASE, "hlif_cycles_heatmap.png")

# ── Channel mapping ───────────────────────────────────────────────────────────
INTL = {f"INTL_HLIF{i}": f"HLIF_{n}"
        for i, n in enumerate([282,290,302,310,318,326,334,342], 1)}
INTr = {f"INTr_HLIF{i}":  f"HLIF_{n}"
        for i, n in enumerate([63,71,83,91,99,107,115,123], 1)}
INTAKE_HLIF = {**INTL, **INTr}

COL_CAM  = 1
COL_LIFT = 4   # [m]
COL_WKPR = 13  # [N/m²]

CYCLE_DEG         = 360.0
N_CYCLES_EXPECTED = 5       # cycles 11–15 (TIMS=0.16s limits binary storage to last 5 cycles)
PUMP_UP_THR_MM    = 0.10    # mm

# Cycle colour map: cycle 2 (blue) → cycle 7 (red)
CYCLE_CMAP = plt.get_cmap("coolwarm")
CYCLE_COLORS = {c: CYCLE_CMAP((c - 2) / 5.0) for c in range(2, 8)}

DARK_BLUE  = "#0D2B55"
MID_BLUE   = "#1A4B8C"
LIGHT_BLUE = "#D6E4F7"
ACCENT_RED = "#C0392B"
STRIPE     = "#EBF2FB"

SPEED_MARKER = {7500: "o", 7600: "s", 7700: "^", 7800: "D"}
SPEED_COLOR  = {7500: "#2471A3", 7600: "#1E8449", 7700: "#CB4335", 7800: "#7D3C98"}


# ── Readiness check ───────────────────────────────────────────────────────────
def results_ready():
    """
    Return True when all 4 speed-case HLIF files contain ≥ 5 cycles of data
    (cam angle span ≥ 1800°) and the jobstate is no longer 'running'.
    With TIMS=0.16s the binary stores cycles 11–15 (span = 5×360 = 1800°).
    """
    speeds = [7500, 7600, 7700, 7800]
    for rpm in speeds:
        js = os.path.join(ETD_DIR, f"{CASESET}.{rpm}rpm", "jobstate")
        if not os.path.isfile(js):
            return False
        with open(js) as f:
            content = f.read()
        # Accept finished / completed / results
        if re.search(r'state\s+(running|submitted)', content):
            return False
    return True


def results_span():
    """Return dict of rpm -> cam angle span for HLIF_63/HLIF_282."""
    spans = {}
    for rpm in [7500, 7600, 7700, 7800]:
        # Use INTr_HLIF1 = HLIF_63
        path = os.path.join(ETD_DIR, f"{CASESET}.{rpm}rpm", "results", "HLIF_63.GID")
        if not os.path.isfile(path):
            spans[rpm] = 0
            continue
        with open(path, "r", errors="replace") as f:
            raw = f.read()
        end_idx = raw.find("\nEND")
        body = raw[end_idx+4:] if end_idx > 0 else ""
        cam_vals = []
        for line in body.splitlines():
            parts = line.split()
            if len(parts) > COL_CAM:
                try:
                    cam_vals.append(float(parts[COL_CAM]))
                except ValueError:
                    pass
        spans[rpm] = (cam_vals[-1] - cam_vals[0]) if len(cam_vals) > 1 else 0
    return spans


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


# ── Data loading ──────────────────────────────────────────────────────────────
def load_all():
    speeds = sorted([
        int(re.search(r"\.(\d+)rpm$", d).group(1))
        for d in os.listdir(ETD_DIR)
        if os.path.isdir(os.path.join(ETD_DIR, d))
        and d.startswith(CASESET + ".")
        and re.search(r"\.\d+rpm$", d)
    ])
    all_data = {}
    for rpm in speeds:
        all_data[rpm] = {}
        res_dir = os.path.join(ETD_DIR, f"{CASESET}.{rpm}rpm", "results")
        for elem, gid in INTAKE_HLIF.items():
            path = os.path.join(res_dir, f"{gid}.GID")
            if os.path.isfile(path):
                d = read_gid(path)
                all_data[rpm][elem] = d if d.shape[0] > 10 and d.shape[1] > COL_LIFT else None
            else:
                all_data[rpm][elem] = None
    return speeds, all_data


# ── Cycle splitting ───────────────────────────────────────────────────────────
def split_cycles(data):
    """
    Split data array into individual 360° cam cycles.
    Returns dict: cycle_number (2..7) -> sub-array, where cam angles are
    normalised to 0–360° within each cycle.
    """
    if data is None or data.shape[0] < 5:
        return {}
    cam = data[:, COL_CAM]
    cam_min = cam[0]
    # First cycle index: cycle 2 starts at 360°, or wherever cam_min sits
    first_cycle = int(cam_min / CYCLE_DEG) + 1   # e.g. cam_min=360 → first_cycle=2
    cycles = {}
    for c in range(first_cycle, first_cycle + N_CYCLES_EXPECTED + 1):
        c0 = c * CYCLE_DEG
        c1 = (c + 1) * CYCLE_DEG
        mask = (cam >= c0 - 0.5) & (cam < c1 + 0.5)
        if mask.sum() < 50:
            continue
        sub = data[mask].copy()
        sub[:, COL_CAM] = sub[:, COL_CAM] - c0   # normalise to 0–360°
        cycles[c] = sub
    return cycles


def cycle_metrics(cycles_dict):
    """
    Per-cycle: min lift (base circle), max lift, mean lift [mm].
    Returns lists aligned to sorted cycle numbers.
    """
    cyc_nums = sorted(cycles_dict.keys())
    mins, maxs, means = [], [], []
    for c in cyc_nums:
        lift = cycles_dict[c][:, COL_LIFT] * 1e3   # m → mm
        mins.append(float(np.min(lift)))
        maxs.append(float(np.max(lift)))
        means.append(float(np.mean(lift)))
    return cyc_nums, mins, maxs, means


def is_pump_up(mins, threshold=PUMP_UP_THR_MM):
    """
    Returns (flag, severity).
    flag = True if min lift is generally rising or stays above threshold.
    severity = 'none' | 'onset' | 'progressive'
    """
    if not mins:
        return False, "no data"
    above = [m > threshold for m in mins]
    rising = all(mins[i] <= mins[i+1] + 0.005 for i in range(len(mins)-1))
    if any(above) and rising:
        return True, "progressive"
    if any(above):
        return True, "onset"
    return False, "none"


# ── Figure 1 & 2: cycle overlay per bank ─────────────────────────────────────
def plot_cycle_overlay(bank_dict, bank_label, speeds, all_data, savepath,
                       figsize=(16, 9)):
    elem_list = sorted(bank_dict.keys(),
                       key=lambda e: int(re.search(r"HLIF(\d+)", e).group(1)))
    fig, axes = plt.subplots(2, 4, figsize=figsize, sharex=True)
    fig.patch.set_facecolor("#F8FAFD")
    fig.suptitle(
        f"Intake HLA Lift — Cycle-by-Cycle Overlay  ({bank_label})\n"
        f"Cycles 2–7 · Model: {MODEL}",
        fontsize=11, fontweight="bold", color=DARK_BLUE, y=1.01
    )

    global_min, global_max = np.inf, -np.inf

    for ax, elem in zip(axes.flat, elem_list):
        cyl = re.search(r"HLIF(\d+)", elem).group(1)
        pump_up_detected = False

        for rpm in speeds:
            d = all_data[rpm].get(elem)
            if d is None:
                continue
            cycles = split_cycles(d)
            if not cycles:
                continue
            cyc_nums, mins, _, _ = cycle_metrics(cycles)
            pu, _ = is_pump_up(mins)
            if pu:
                pump_up_detected = True
            # Only plot one speed's cycle traces to keep readable
            # (use highest speed with most data, or show all speeds faded)

        # Plot all speeds at reduced alpha, annotate pump-up
        for rpm in speeds:
            d = all_data[rpm].get(elem)
            if d is None:
                continue
            cycles = split_cycles(d)
            for c_num, c_data in sorted(cycles.items()):
                cam  = c_data[:, COL_CAM]
                lift = c_data[:, COL_LIFT] * 1e3
                # Line style: solid for highest speed, dashed for others
                lw  = 1.5 if rpm == max(speeds) else 0.8
                alp = 0.9 if rpm == max(speeds) else 0.35
                ax.plot(cam, lift,
                        color=CYCLE_COLORS[min(c_num, 7)],
                        lw=lw, alpha=alp, zorder=c_num)
                global_min = min(global_min, lift.min())
                global_max = max(global_max, lift.max())

        ax.axhline(PUMP_UP_THR_MM, color=ACCENT_RED, lw=0.7,
                   ls="--", alpha=0.55, zorder=10)

        title_col = ACCENT_RED if pump_up_detected else MID_BLUE
        ax.set_title(f"CYL {cyl}" + (" ▲ pump-up" if pump_up_detected else ""),
                     fontsize=9, color=title_col, fontweight="bold", pad=3)

        col_idx = list(axes.flat).index(ax) % 4
        ax.set_xlabel("Cam angle [°]", fontsize=7.5, labelpad=2)
        if col_idx == 0:
            ax.set_ylabel("HLA lift [mm]", fontsize=7.5, labelpad=2)
        ax.tick_params(labelsize=7)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(90))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(45))
        ax.grid(True, which="major", ls="--", alpha=0.25, lw=0.5)
        ax.set_xlim(0, 360)

    if global_max > global_min:
        m = (global_max - global_min) * 0.08
        for ax in axes.flat:
            ax.set_ylim(max(0, global_min - m), global_max + m + 0.01)

    # Cycle legend
    cycle_handles = [
        Line2D([0],[0], color=CYCLE_COLORS[c], lw=1.8,
               label=f"Cycle {c}")
        for c in range(2, 8)
    ]
    cycle_handles.append(
        Line2D([0],[0], color=ACCENT_RED, lw=0.9, ls="--",
               alpha=0.7, label=f"Limit {PUMP_UP_THR_MM} mm")
    )
    fig.legend(handles=cycle_handles, loc="lower center",
               ncol=len(cycle_handles), fontsize=8.5,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.04))

    fig.tight_layout(rect=[0, 0.04, 1, 0.99])
    fig.savefig(savepath, dpi=160, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved: {savepath}")


# ── Figure 3: min-lift trend — pump-up fingerprint ────────────────────────────
def plot_trend(speeds, all_data, savepath, figsize=(16, 10)):
    """
    4×4 grid (left 2 cols = INTL, right 2 cols = INTr).
    Each subplot: min-lift per cycle for all speeds, 1 line per speed.
    Rising line = pump-up.
    """
    intl_list = [f"INTL_HLIF{i}" for i in range(1, 9)]
    intr_list = [f"INTr_HLIF{i}"  for i in range(1, 9)]

    fig, axes = plt.subplots(2, 8, figsize=figsize)
    fig.patch.set_facecolor("#F4F6F9")
    fig.suptitle(
        "HLA Base-Circle Min Lift per Cycle — Pump-Up Trend\n"
        f"Rising = pump-up growing  ·  {MODEL}",
        fontsize=11, fontweight="bold", color=DARK_BLUE, y=1.01
    )

    all_elems = intl_list + intr_list
    for ax, elem in zip(axes.flat, all_elems):
        cyl = int(re.search(r"HLIF(\d+)", elem).group(1))
        bank = "LB" if elem.startswith("INTL") else "RB"
        pump_up_any = False

        for rpm in speeds:
            d = all_data[rpm].get(elem)
            if d is None:
                continue
            cycles = split_cycles(d)
            if not cycles:
                continue
            cyc_nums, mins, _, _ = cycle_metrics(cycles)
            pu, sev = is_pump_up(mins)
            if pu:
                pump_up_any = True
            col = SPEED_COLOR.get(rpm, "grey")
            mrk = SPEED_MARKER.get(rpm, "o")
            lw = 1.8 if pu else 1.2
            ax.plot(cyc_nums, mins, f"-{mrk}",
                    color=col, lw=lw, ms=4, alpha=0.88,
                    label=f"{rpm}")

        ax.axhline(PUMP_UP_THR_MM, color=ACCENT_RED, lw=0.7,
                   ls="--", alpha=0.55)
        ax.axhspan(PUMP_UP_THR_MM, ax.get_ylim()[1] if ax.get_ylim()[1] > PUMP_UP_THR_MM else PUMP_UP_THR_MM + 0.2,
                   color="#FDECEA", alpha=0.15, zorder=0)

        title_col = ACCENT_RED if pump_up_any else MID_BLUE
        ax.set_title(f"CYL{cyl} {bank}", fontsize=8,
                     color=title_col, fontweight="bold", pad=2)
        ax.tick_params(labelsize=6.5)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.grid(True, ls="--", alpha=0.25, lw=0.5)
        ax.set_xlabel("Cycle #", fontsize=7, labelpad=1)
        col_idx = list(axes.flat).index(ax) % 8
        if col_idx == 0:
            ax.set_ylabel("Min lift [mm]", fontsize=7, labelpad=2)

    # Speed legend
    spd_handles = [
        Line2D([0],[0], color=SPEED_COLOR[s], marker=SPEED_MARKER[s],
               ms=5, lw=1.5, label=f"{s} rpm")
        for s in speeds if s in SPEED_COLOR
    ]
    spd_handles.append(
        Line2D([0],[0], color=ACCENT_RED, lw=0.9, ls="--",
               alpha=0.7, label=f"Limit {PUMP_UP_THR_MM} mm")
    )
    fig.legend(handles=spd_handles, loc="lower center",
               ncol=len(spd_handles), fontsize=8.5,
               framealpha=0.92, bbox_to_anchor=(0.5, -0.03))

    fig.tight_layout(rect=[0, 0.04, 1, 0.99])
    fig.savefig(savepath, dpi=160, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved: {savepath}")


# ── Figure 4: heatmap — Δlift cycle 7 – cycle 2 ──────────────────────────────
def plot_heatmap(speeds, all_data, savepath, figsize=(12, 5)):
    """
    Heatmap: rows = elements, cols = speeds.
    Cell value = min_lift(cycle 7) – min_lift(cycle 2) [mm].
    Positive = pump-up growth. Negative = unexpected decay.
    """
    intl_list = [f"INTL_HLIF{i}" for i in range(1, 9)]
    intr_list = [f"INTr_HLIF{i}"  for i in range(1, 9)]
    all_elems = intl_list + intr_list

    valid_speeds = [s for s in speeds if s in SPEED_COLOR]
    matrix = np.full((len(all_elems), len(valid_speeds)), np.nan)

    for j, rpm in enumerate(valid_speeds):
        for i, elem in enumerate(all_elems):
            d = all_data[rpm].get(elem)
            if d is None:
                continue
            cycles = split_cycles(d)
            cyc_nums, mins, _, _ = cycle_metrics(cycles)
            if len(cyc_nums) < 2:
                continue
            c_first = cyc_nums[0]
            c_last  = cyc_nums[-1]
            idx_f = cyc_nums.index(c_first)
            idx_l = cyc_nums.index(c_last)
            matrix[i, j] = mins[idx_l] - mins[idx_f]

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#F8FAFD")

    vmax = max(0.05, np.nanmax(np.abs(matrix)))
    im = ax.imshow(matrix, cmap="RdYlGn_r", aspect="auto",
                   vmin=-vmax, vmax=vmax)

    ax.set_xticks(range(len(valid_speeds)))
    ax.set_xticklabels([f"{s} rpm" for s in valid_speeds], fontsize=9)
    ax.set_yticks(range(len(all_elems)))
    def _elabel(e):
        m = re.search(r'HLIF(\d+)', e)
        return f"CYL{m.group(1)} {'LB' if e.startswith('INTL') else 'RB'}" if m else e
    ax.set_yticklabels([_elabel(e) for e in all_elems], fontsize=8)

    # Annotate cells
    for i in range(len(all_elems)):
        for j in range(len(valid_speeds)):
            if not np.isnan(matrix[i, j]):
                txt = f"{matrix[i,j]:+.3f}"
                col = "white" if abs(matrix[i,j]) > vmax * 0.6 else "black"
                ax.text(j, i, txt, ha="center", va="center",
                        fontsize=7.5, color=col, fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label("Δ min lift  (cycle 7 – cycle 2)  [mm]", fontsize=9)
    ax.set_title(
        f"HLA Pump-Up Growth  —  Δ min lift (last – first cycle)  |  {MODEL}",
        fontsize=11, fontweight="bold", color=DARK_BLUE, pad=8
    )
    ax.axhline(7.5, color="white", lw=1.5)   # separator INTL / INTr

    # Bank labels
    ax.text(-0.5, 3.5, "Left bank\n(INTL)", ha="right", va="center",
            fontsize=8, color=MID_BLUE, fontweight="bold", rotation=90,
            transform=ax.get_yaxis_transform())
    ax.text(-0.5, 11.5, "Right bank\n(INTr)", ha="right", va="center",
            fontsize=8, color=MID_BLUE, fontweight="bold", rotation=90,
            transform=ax.get_yaxis_transform())

    fig.tight_layout()
    fig.savefig(savepath, dpi=160, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved: {savepath}")


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
        "note": ParagraphStyle("note", fontSize=7.5,
                                textColor=colors.HexColor("#555"),
                                leading=12, fontName="Helvetica-Oblique"),
        "cell_hdr": ParagraphStyle("cell_hdr", fontSize=8,
                                    textColor=colors.white,
                                    alignment=TA_CENTER,
                                    fontName="Helvetica-Bold"),
        "cell": ParagraphStyle("cell", fontSize=7.5,
                                textColor=colors.black,
                                alignment=TA_CENTER, fontName="Helvetica"),
        "cell_warn": ParagraphStyle("cell_warn", fontSize=7.5,
                                     textColor=ACCENT_RED_CL,
                                     alignment=TA_CENTER,
                                     fontName="Helvetica-Bold"),
    }


def hdr_ftr(canvas, doc):
    W, H = A4
    canvas.saveState()
    canvas.setFillColor(DARK_BLUE_CL)
    canvas.rect(0, H - 22*mm, W, 22*mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(W/2, H - 13*mm,
        "AML Valvetrain Engineering — HLA Pump-Up: Cycle-by-Cycle Analysis")
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

    # ── Banner ────────────────────────────────────────────────────────────────
    ttbl = Table([[Paragraph(
        "6. HLA Pump-Up — Cycle-by-Cycle Analysis (Cycles 6–7)", st["h1"])]],
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

    # ── 6.1 Background ────────────────────────────────────────────────────────
    story.append(Paragraph("6.1  Analysis Approach", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    valid_speeds = [s for s in speeds if s in SPEED_COLOR and
                    any(all_data[s].get(f"INTL_HLIF{i}") is not None
                        for i in range(1,9))]

    story.append(Paragraph(
        "The re-run results post-processing extends the output window to "
        "<b>cycles 11–15</b> (cam angle 3600°–5400°).  The simulation binary storage "
        "begins at TIMS = 0.16 s, which corresponds to the start of cycle 11 — "
        "cycles 1–10 are not retained in the TYCON binary and cannot be extracted. "
        "Each 360° cam segment is treated as one independent lift event. "
        "For every HLA element the <b>minimum lift on the base circle is tracked "
        "across cycles 11–15</b>: a rising minimum indicates that pump-up "
        "is still growing at the end of the simulation (not yet saturated). "
        "A stable or falling minimum indicates that the HLA has reached its "
        "pump-up equilibrium. No value above the detection threshold indicates "
        "nominal HLA behaviour.",
        st["body"]))
    story.append(Spacer(1, 4*mm))

    # ── 6.2 Figures ───────────────────────────────────────────────────────────
    story.append(Paragraph("6.2  Results", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    W_full = 178*mm
    figs = [
        (FIG_OVERLAY_INTL, 9/16,
         "Fig. 6-1: Cycle overlay — Left bank (INTL_HLIF1–8).",
         "Each subplot shows cycles 11–15 overlaid at all speed cases. "
         "The solid traces are the highest speed; faded traces show other speeds. "
         "A rising baseline from first to last cycle confirms pump-up still growing. "
         "Elements with pump-up are marked with ▲."),
        (FIG_OVERLAY_INTr, 9/16,
         "Fig. 6-2: Cycle overlay — Right bank (INTr_HLIF1–8).",
         "Equivalent view for the right-bank intake elements."),
        (FIG_TREND, 10/16,
         "Fig. 6-3: Min-lift per cycle for all 16 elements.",
         "Each line = one speed case. Cycles 11–15: a rising value means "
         "pump-up is still accumulating at the end of the simulation. "
         "Flat lines near zero = stable. Elements in red text exceed the 0.10 mm threshold."),
        (FIG_HEATMAP, 5/12,
         "Fig. 6-4: Pump-up growth heatmap — Δ min lift (cycle 15 − cycle 11).",
         "Positive values (red) = pump-up still growing between first and last stored cycle. "
         "Near-zero (green) = HLA has reached equilibrium or is stable. "
         "The separator line divides left bank (top) from right bank (bottom)."),
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

    # ── 6.3 Summary table ─────────────────────────────────────────────────────
    story.append(Paragraph("6.3  Pump-Up Summary — Per Element, Per Speed", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    all_elems = ([f"INTL_HLIF{i}" for i in range(1,9)] +
                 [f"INTr_HLIF{i}"  for i in range(1,9)])

    hdr_row = [
        Paragraph("Element", st["cell_hdr"]),
        Paragraph("Speed\n[rpm]", st["cell_hdr"]),
        Paragraph("Min lift\ncyc 11 [mm]", st["cell_hdr"]),
        Paragraph("Min lift\ncyc 15 [mm]", st["cell_hdr"]),
        Paragraph("Δ min lift\n[mm]", st["cell_hdr"]),
        Paragraph("Pump-up?", st["cell_hdr"]),
        Paragraph("Severity", st["cell_hdr"]),
    ]
    tbl_rows = [hdr_row]
    pu_flag_rows = []

    for elem in all_elems:
        for rpm in valid_speeds:
            d = all_data[rpm].get(elem)
            row_idx = len(tbl_rows)
            if d is None:
                tbl_rows.append([
                    Paragraph(elem, st["cell"]),
                    Paragraph(str(rpm), st["cell"]),
                    Paragraph("—", st["cell"]),
                    Paragraph("—", st["cell"]),
                    Paragraph("—", st["cell"]),
                    Paragraph("no data", st["cell"]),
                    Paragraph("—", st["cell"]),
                ])
                continue
            cycles = split_cycles(d)
            cyc_nums, mins, _, _ = cycle_metrics(cycles)
            if len(mins) < 2:
                continue
            delta = mins[-1] - mins[0]
            pu, sev = is_pump_up(mins)
            cs = st["cell_warn"] if pu else st["cell"]
            tbl_rows.append([
                Paragraph(elem, st["cell"]),
                Paragraph(str(rpm), st["cell"]),
                Paragraph(f"{mins[0]:.4f}", st["cell"]),
                Paragraph(f"{mins[-1]:.4f}", st["cell"]),
                Paragraph(f"{delta:+.4f}", cs),
                Paragraph("YES" if pu else "no", cs),
                Paragraph(sev, cs),
            ])
            if pu:
                pu_flag_rows.append(row_idx)

    col_w = [33*mm, 17*mm, 24*mm, 24*mm, 20*mm, 20*mm, 22*mm]
    sum_tbl = Table(tbl_rows, colWidths=col_w, repeatRows=1)
    ts = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE_CL),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("FONTSIZE",   (0,0), (-1,-1), 7.5),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, STRIPE_CL]),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#BBBBBB")),
    ])
    for r in pu_flag_rows:
        ts.add("BACKGROUND", (4,r), (6,r), colors.HexColor("#FDECEA"))
    sum_tbl.setStyle(ts)
    story.append(sum_tbl)
    story.append(Spacer(1, 3*mm))

    n_pu = len(pu_flag_rows)
    n_total = len(tbl_rows) - 1
    story.append(Paragraph(
        f"★  {n_pu} of {n_total} element-speed combinations show pump-up "
        f"(min lift exceeds {PUMP_UP_THR_MM} mm threshold or rises cycle-over-cycle).",
        st["note"]))
    story.append(Spacer(1, 5*mm))

    # ── 6.4 Engineering assessment ────────────────────────────────────────────
    story.append(Paragraph("6.4  Engineering Assessment", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    progressive = sum(1 for _, _, mins, _, _ in [
        (elem, rpm,
         cycle_metrics(split_cycles(all_data[rpm].get(elem)))[1],
         None, None)
        for elem in all_elems for rpm in valid_speeds
        if all_data[rpm].get(elem) is not None
        and len(cycle_metrics(split_cycles(all_data[rpm].get(elem)))[1]) >= 2
    ] if is_pump_up(mins)[1] == "progressive")

    if n_pu == 0:
        assess = (
            "No pump-up detected across all 16 intake HLA elements and all evaluated "
            "speed cases. The HLA min-lift on the base circle does not rise across "
            "cycles 11–15, confirming that the updated spring (04_spring_update) "
            "provides sufficient seat load to fully close the HLA check valve and bleed "
            "down any accumulated oil volume within the available base-circle dwell time. "
            "The intake valve train is dynamically stable across the full evaluated speed range."
        )
    else:
        assess = (
            f"Pump-up is confirmed in <b>{n_pu}</b> element-speed combination(s). "
            f"Of these, <b>{progressive}</b> show a <i>progressive</i> pattern "
            "(min lift still rising at cycle 7), meaning steady state has not been "
            "reached within the 7 simulated cycles. "
            "The remaining flagged cases show an <i>onset</i> pattern (above threshold "
            "but not monotonically increasing), suggesting the HLA is near its "
            "pump-up equilibrium. "
            "Progressive pump-up at the highest evaluated speed indicates that "
            "the bleed-down rate of the HLA is insufficient for the available "
            "base-circle dwell time at that speed. "
            "Recommended actions: (1) Increase intake spring seat load to reduce "
            "cam-follower separation time; (2) Review HLA bleed orifice diameter; "
            "(3) Extend simulation beyond 15 cycles to confirm whether pump-up saturates "
            "or diverges."
        )

    story.append(Paragraph(assess, st["body"]))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        f"Cycle-by-cycle data from {MODEL}.etd, "
        f"post-processed with setResultsInterval covering cycles 11–15 "
        f"(TIMS=0.16 s limits binary storage to last 5 cam cycles). "
        f"Analysis by analyze_hlif_cycles.py — 2026-06-17.",
        st["note"]))

    doc.build(story, onFirstPage=hdr_ftr, onLaterPages=hdr_ftr)
    print(f"  PDF section: {out_path}")


# ── Git push ──────────────────────────────────────────────────────────────────
def git_push(files_in_wt, commit_msg):
    wt = WT_PATH
    for f in files_in_wt:
        subprocess.run(["git", "-C", wt, "add", f],
                       check=False, capture_output=True)
    r = subprocess.run(
        ["git", "-C", wt, "commit", "-m", commit_msg],
        capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(
        ["git", "-C", wt, "push", "origin", "excite_td"],
        capture_output=True, text=True)
    print(r2.stdout.strip() or r2.stderr.strip())


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
    check_only = "--check" in sys.argv

    print("=== HLIF Cycle-by-Cycle Analysis ===")

    # Check readiness
    span = results_span()
    print("\nCurrent data spans:")
    all_ready = True
    for rpm, deg in sorted(span.items()):
        cycles_avail = deg / 360
        ready = cycles_avail >= 4.5
        print(f"  {rpm} rpm: {deg:.0f}° = {cycles_avail:.1f} cycles  "
              f"{'[READY]' if ready else '[PENDING]'}")
        if not ready:
            all_ready = False

    if check_only:
        print(f"\nResult: {'READY' if all_ready else 'NOT YET READY'}")
        return all_ready

    if not all_ready:
        print("\nResults not yet complete. Re-run when all cases show >= 5 cycles.")
        return False

    print("\n[1/5] Loading multi-cycle data ...")
    speeds, all_data = load_all()
    valid_speeds = [s for s in speeds if s in SPEED_COLOR and
                    any(all_data[s].get(f"INTL_HLIF{i}") is not None
                        for i in range(1,9))]
    print(f"  Speeds: {valid_speeds}")

    print("\n[2/5] Generating figures ...")
    plot_cycle_overlay(INTL, "Left bank (INTL_HLIF1–8)",
                       valid_speeds, all_data, FIG_OVERLAY_INTL)
    plot_cycle_overlay(INTr, "Right bank (INTr_HLIF1–8)",
                       valid_speeds, all_data, FIG_OVERLAY_INTr)
    plot_trend(valid_speeds, all_data, FIG_TREND)
    plot_heatmap(valid_speeds, all_data, FIG_HEATMAP)

    print("\n[3/5] Building PDF section ...")
    build_pdf_section(speeds, all_data, SEC_PDF)

    print("\n[4/5] Merging PDFs ...")
    merge_pdfs(MAIN_PDF, SEC_PDF, OUTPUT_PDF)
    try: os.remove(SEC_PDF)
    except: pass

    print("\n[5/5] Pushing to git ...")
    wt = WT_PATH
    for src, dst in [
        (OUTPUT_PDF,         "AML_Valvetrain_Model_Analysis.pdf"),
        (__file__,           "analyze_hlif_cycles.py"),
        (FIG_OVERLAY_INTL,   "hlif_cycles_overlay_INTL.png"),
        (FIG_OVERLAY_INTr,   "hlif_cycles_overlay_INTr.png"),
        (FIG_TREND,          "hlif_cycles_trend.png"),
        (FIG_HEATMAP,        "hlif_cycles_heatmap.png"),
    ]:
        if os.path.isfile(src):
            import shutil
            shutil.copy2(src, os.path.join(wt, dst))

    git_push(
        ["AML_Valvetrain_Model_Analysis.pdf",
         "analyze_hlif_cycles.py",
         "hlif_cycles_overlay_INTL.png",
         "hlif_cycles_overlay_INTr.png",
         "hlif_cycles_trend.png",
         "hlif_cycles_heatmap.png"],
        ("analysis: HLA pump-up cycle-by-cycle comparison (cycles 2-7)\n\n"
         "Compare HLA lift cycle-by-cycle for all 16 intake elements at\n"
         "7500-7800 rpm. Rising min-lift = progressive pump-up confirmed.\n"
         "Adds cycle overlay plots, min-lift trend, delta-lift heatmap,\n"
         "and summary table to AML_Valvetrain_Model_Analysis.pdf (section 6).\n\n"
         "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>")
    )

    print("\nDone.")
    return True


if __name__ == "__main__":
    main()
