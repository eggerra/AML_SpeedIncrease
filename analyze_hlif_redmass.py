"""
analyze_hlif_redmass.py
=======================
HLA pump-up analysis for AML_AE26_ChainDrive__04_spring_update_redMass.
Identical logic to analyze_hlif_pumpup.py but targets the redMass model
(7 speed cases: 7000–7800 rpm, 5400° / 15 cam cycles).
Appends a new section to AML_Valvetrain_Model_Analysis.pdf.

Usage
-----
    python analyze_hlif_redmass.py
"""

import os, re, io, tempfile
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

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
MODEL   = "AML_AE26_ChainDrive__04_spring_update_redMass"
CASESET = f"{MODEL}.EngineSpeed"

MAIN_PDF   = os.path.join(BASE, "AML_Valvetrain_Model_Analysis.pdf")
HLIF_PDF   = os.path.join(BASE, "_hlif_redmass_section.pdf")
OUTPUT_PDF = os.path.join(BASE, "AML_Valvetrain_Model_Analysis.pdf")

# ── Channel mapping ────────────────────────────────────────────────────────────
INTAKE_HLIF = {
    "INTL_HLIF1": "HLIF_282", "INTL_HLIF2": "HLIF_290",
    "INTL_HLIF3": "HLIF_302", "INTL_HLIF4": "HLIF_310",
    "INTL_HLIF5": "HLIF_318", "INTL_HLIF6": "HLIF_326",
    "INTL_HLIF7": "HLIF_334", "INTL_HLIF8": "HLIF_342",
    "INTr_HLIF1": "HLIF_63",  "INTr_HLIF2": "HLIF_71",
    "INTr_HLIF3": "HLIF_83",  "INTr_HLIF4": "HLIF_91",
    "INTr_HLIF5": "HLIF_99",  "INTr_HLIF6": "HLIF_107",
    "INTr_HLIF7": "HLIF_115", "INTr_HLIF8": "HLIF_123",
}

COL_CAM   = 1
COL_CRANK = 2
COL_LIFT  = 4
COL_FORCE = 7
COL_WKPR  = 13

CYCLE_DEG = 360.0
PUMP_UP_THRESHOLD_MM = 0.10

# ── Colours ────────────────────────────────────────────────────────────────────
DARK_BLUE  = "#0D2B55"
MID_BLUE   = "#1A4B8C"
LIGHT_BLUE = "#D6E4F7"
ACCENT_RED = "#C0392B"
ACCENT_GRN = "#1E8449"
ORANGE     = "#E67E22"
STRIPE     = "#EBF2FB"

RPM_COLORS = {
    7000: "#2980B9",
    7300: "#16A085",
    7400: "#D35400",
    7500: "#27AE60",
    7600: "#F39C12",
    7700: "#E74C3C",
    7800: "#8E44AD",
}


# ── GID reader ─────────────────────────────────────────────────────────────────
def read_gid_time(filepath):
    with open(filepath, "r", errors="replace") as f:
        raw = f.read()
    end_idx = raw.find("\nEND")
    if end_idx < 0:
        end_idx = raw.find("END")
    header = raw[:end_idx] if end_idx > 0 else raw[:2000]
    body   = raw[end_idx + 4:] if end_idx > 0 else ""
    ch_block_m = re.search(r"CHANNEL\s*=\s*\[([^\]]+)\]", header, re.DOTALL)
    channels = re.findall(r"'([^']+)'", ch_block_m.group(1)) if ch_block_m else []
    un_block_m = re.search(r"UNIT\s*=\s*\[([^\]]+)\]", header, re.DOTALL)
    units = re.findall(r"'([^']+)'", un_block_m.group(1)) if un_block_m else []
    ncols = len(channels)
    if ncols == 0:
        return channels, units, np.zeros((0, 0))
    rows = []
    for line in body.splitlines():
        parts = line.split()
        if len(parts) >= ncols:
            try:
                rows.append([float(v) for v in parts[:ncols]])
            except ValueError:
                continue
    if not rows:
        return channels, units, np.zeros((0, ncols))
    return channels, units, np.array(rows)


def load_hlif_speed(rpm, element_name, gid_name):
    run_dir  = os.path.join(ETD_DIR, f"{CASESET}.{rpm}rpm", "results")
    gid_path = os.path.join(run_dir, f"{gid_name}.GID")
    if not os.path.isfile(gid_path):
        return None
    ch, un, data = read_gid_time(gid_path)
    if data.shape[0] < 10:
        return None
    return data


def get_cycle_stats(cam_angles_deg, lift_m, cycle_deg=CYCLE_DEG):
    total_range = cam_angles_deg[-1] - cam_angles_deg[0]
    n_cycles = int(total_range / cycle_deg)
    if n_cycles < 1:
        return np.array([]), np.array([]), np.array([]), np.array([])
    cycle_start = cam_angles_deg[0]
    idxs, mins, maxs, means = [], [], [], []
    for c in range(n_cycles):
        c0 = cycle_start + c * cycle_deg
        c1 = c0 + cycle_deg
        mask = (cam_angles_deg >= c0) & (cam_angles_deg < c1)
        if mask.sum() < 5:
            continue
        seg = lift_m[mask] * 1e3
        idxs.append(c + 1)
        mins.append(float(np.min(seg)))
        maxs.append(float(np.max(seg)))
        means.append(float(np.mean(seg)))
    return (np.array(idxs, dtype=int),
            np.array(mins), np.array(maxs), np.array(means))


def collect_all_data():
    speeds = sorted([
        int(re.search(r"\.(\d+)rpm$", d).group(1))
        for d in os.listdir(ETD_DIR)
        if os.path.isdir(os.path.join(ETD_DIR, d))
        and d.startswith(CASESET + ".")
        and re.search(r"\.\d+rpm$", d)
    ])
    print(f"Found speed cases: {speeds}")
    data = {}
    for rpm in speeds:
        data[rpm] = {}
        for elem, gid in INTAKE_HLIF.items():
            d = load_hlif_speed(rpm, elem, gid)
            status = f"{d.shape[0]} steps" if d is not None else "missing"
            print(f"  {rpm}rpm  {elem}: {status}")
            data[rpm][elem] = d
    return speeds, data


# ── Figures ────────────────────────────────────────────────────────────────────
def fig_lift_timehist(speeds, data, savepath):
    elem_L, elem_R = "INTL_HLIF1", "INTr_HLIF1"
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    fig.suptitle(
        f"Intake HLA Lift — Last 2 Cam Cycles\n{MODEL}",
        fontsize=11, fontweight="bold", color=DARK_BLUE, y=1.01)
    for ax, elem in zip(axes, [elem_L, elem_R]):
        for rpm in speeds:
            d = data[rpm].get(elem)
            if d is None or d.shape[0] < 10:
                continue
            cam = d[:, COL_CAM]
            lift_mm = d[:, COL_LIFT] * 1e3
            cam_end = cam[-1]
            mask = cam >= (cam_end - 720.0)
            cam_seg  = cam[mask] - cam[mask][0]
            lift_seg = lift_mm[mask]
            ax.plot(cam_seg, lift_seg, color=RPM_COLORS.get(rpm, "grey"),
                    lw=1.2, alpha=0.85, label=f"{rpm} rpm")
        bank = "Left bank" if elem.startswith("INTL") else "Right bank"
        ax.set_title(f"{elem}  ({bank})", fontsize=10, color=MID_BLUE)
        ax.set_xlabel("Cam angle in last 2 cycles [°]", fontsize=9)
        ax.set_ylabel("HLA lift [mm]", fontsize=9)
        ax.axhline(PUMP_UP_THRESHOLD_MM, color=ACCENT_RED, lw=0.8,
                   ls="--", alpha=0.7, label=f"Pump-up limit ({PUMP_UP_THRESHOLD_MM} mm)")
        ax.xaxis.set_major_locator(ticker.MultipleLocator(90))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(45))
        ax.grid(True, which="major", ls="--", alpha=0.35)
        ax.grid(True, which="minor", ls=":", alpha=0.15)
        ax.legend(fontsize=8, loc="upper right")
    plt.tight_layout()
    fig.savefig(savepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {savepath}")


def fig_pumpup_envelope(speeds, data, savepath):
    elem_L, elem_R = "INTL_HLIF1", "INTr_HLIF1"
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(
        f"HLA Pump-Up Envelope — Max / Min Lift per Cycle\n{MODEL}",
        fontsize=11, fontweight="bold", color=DARK_BLUE, y=1.01)
    for ax, elem in zip(axes, [elem_L, elem_R]):
        for rpm in speeds:
            d = data[rpm].get(elem)
            if d is None or d.shape[0] < 10:
                continue
            cam  = d[:, COL_CAM]
            lift = d[:, COL_LIFT]
            cyc_idx, mins, maxs, means = get_cycle_stats(cam, lift)
            if len(cyc_idx) == 0:
                continue
            col = RPM_COLORS.get(rpm, "grey")
            ax.fill_between(cyc_idx, mins, maxs, alpha=0.18, color=col)
            ax.plot(cyc_idx, maxs, "-o", color=col, ms=4, lw=1.4, label=f"{rpm} rpm")
            ax.plot(cyc_idx, mins, "--", color=col, ms=3, lw=0.8)
        bank = "Left bank" if elem.startswith("INTL") else "Right bank"
        ax.set_title(f"{elem}  ({bank})", fontsize=10, color=MID_BLUE)
        ax.set_xlabel("Cam cycle number [—]", fontsize=9)
        ax.set_ylabel("HLA lift [mm]", fontsize=9)
        ax.axhline(PUMP_UP_THRESHOLD_MM, color=ACCENT_RED, lw=0.9,
                   ls="--", alpha=0.8, label="Pump-up limit")
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.grid(True, ls="--", alpha=0.35)
        ax.legend(fontsize=8, loc="upper left")
    plt.tight_layout()
    fig.savefig(savepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {savepath}")


def fig_speed_sweep(speeds, data, savepath):
    left_elems  = [f"INTL_HLIF{i}" for i in range(1, 9)]
    right_elems = [f"INTr_HLIF{i}"  for i in range(1, 9)]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    fig.suptitle(
        f"HLA Max Lift (Last Cycle) vs. Engine Speed — All Intake Elements\n{MODEL}",
        fontsize=11, fontweight="bold", color=DARK_BLUE, y=1.01)
    cmap = plt.colormaps["tab10"]
    marker_list = ["o", "s", "^", "v", "D", "P", "X", "*"]
    for ax, elem_list, bank_label in zip(
            axes, [left_elems, right_elems], ["Left bank (INTL)", "Right bank (INTr)"]):
        for i, elem in enumerate(elem_list):
            xs, ys = [], []
            for rpm in speeds:
                d = data[rpm].get(elem)
                if d is None or d.shape[0] < 10:
                    continue
                cam  = d[:, COL_CAM]
                lift = d[:, COL_LIFT]
                cam_end = cam[-1]
                mask = cam >= (cam_end - CYCLE_DEG)
                if mask.sum() < 3:
                    continue
                xs.append(rpm)
                ys.append(float(np.max(lift[mask])) * 1e3)
            if xs:
                ax.plot(xs, ys, "-" + marker_list[i % len(marker_list)],
                        color=cmap(i / 8), ms=6, lw=1.4, label=f"CYL{i+1}")
        ax.axhline(PUMP_UP_THRESHOLD_MM, color=ACCENT_RED, lw=1.0,
                   ls="--", alpha=0.8, label=f"Limit {PUMP_UP_THRESHOLD_MM} mm")
        ax.set_title(bank_label, fontsize=10, color=MID_BLUE)
        ax.set_xlabel("Engine speed [rpm]", fontsize=9)
        ax.set_ylabel("Max HLA lift [mm]", fontsize=9)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
        ax.grid(True, ls="--", alpha=0.35)
        ax.legend(fontsize=7.5, ncol=2, loc="upper left")
    plt.tight_layout()
    fig.savefig(savepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {savepath}")


def fig_working_pressure(speeds, data, savepath):
    elem_L, elem_R = "INTL_HLIF1", "INTr_HLIF1"
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    fig.suptitle(
        f"HLA Working Pressure — Last 2 Cam Cycles\n{MODEL}",
        fontsize=11, fontweight="bold", color=DARK_BLUE, y=1.01)
    for ax, elem in zip(axes, [elem_L, elem_R]):
        for rpm in speeds:
            d = data[rpm].get(elem)
            if d is None or d.shape[0] < 10:
                continue
            cam = d[:, COL_CAM]
            wkpr_bar = d[:, COL_WKPR] / 1e5
            cam_end = cam[-1]
            mask = cam >= (cam_end - 720.0)
            cam_seg  = cam[mask] - cam[mask][0]
            wkpr_seg = wkpr_bar[mask]
            ax.plot(cam_seg, wkpr_seg, color=RPM_COLORS.get(rpm, "grey"),
                    lw=1.2, alpha=0.85, label=f"{rpm} rpm")
        bank = "Left bank" if elem.startswith("INTL") else "Right bank"
        ax.set_title(f"{elem}  ({bank})", fontsize=10, color=MID_BLUE)
        ax.set_xlabel("Cam angle in last 2 cycles [°]", fontsize=9)
        ax.set_ylabel("HLA working pressure [bar]", fontsize=9)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(90))
        ax.grid(True, ls="--", alpha=0.35)
        ax.legend(fontsize=8, loc="upper right")
    plt.tight_layout()
    fig.savefig(savepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {savepath}")


def build_summary_table(speeds, data):
    rows = []
    for rpm in speeds:
        for elem in sorted(INTAKE_HLIF):
            d = data[rpm].get(elem)
            if d is None or d.shape[0] < 10:
                continue
            cam  = d[:, COL_CAM]
            lift = d[:, COL_LIFT]
            wkpr = d[:, COL_WKPR]
            cam_end = cam[-1]
            mask = cam >= (cam_end - CYCLE_DEG)
            if mask.sum() < 3:
                continue
            max_l   = float(np.max(lift[mask])) * 1e3
            min_l   = float(np.min(lift[mask])) * 1e3
            max_p   = float(np.max(wkpr[mask])) / 1e5
            pump_up = min_l > PUMP_UP_THRESHOLD_MM
            rows.append((elem, rpm, max_l, min_l, pump_up, max_p))
    return rows


# ── PDF ────────────────────────────────────────────────────────────────────────
DARK_BLUE_CL  = colors.HexColor(DARK_BLUE)
MID_BLUE_CL   = colors.HexColor(MID_BLUE)
LIGHT_BLUE_CL = colors.HexColor(LIGHT_BLUE)
ACCENT_RED_CL = colors.HexColor(ACCENT_RED)
STRIPE_CL     = colors.HexColor(STRIPE)
ORANGE_CL     = colors.HexColor(ORANGE)


def _styles():
    return {
        "h1":        ParagraphStyle("h1",   fontSize=14, textColor=DARK_BLUE_CL,
                                    spaceBefore=12, spaceAfter=5, fontName="Helvetica-Bold"),
        "h2":        ParagraphStyle("h2",   fontSize=11, textColor=MID_BLUE_CL,
                                    spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold"),
        "body":      ParagraphStyle("body", fontSize=9,  textColor=colors.black,
                                    leading=14, alignment=TA_JUSTIFY, fontName="Helvetica"),
        "note":      ParagraphStyle("note", fontSize=8,  textColor=colors.HexColor("#555555"),
                                    leading=12, fontName="Helvetica-Oblique"),
        "cell_hdr":  ParagraphStyle("cell_hdr", fontSize=8.5, textColor=colors.white,
                                    alignment=TA_CENTER, fontName="Helvetica-Bold"),
        "cell":      ParagraphStyle("cell",  fontSize=8, textColor=colors.black,
                                    alignment=TA_CENTER, fontName="Helvetica"),
        "cell_warn": ParagraphStyle("cell_warn", fontSize=8, textColor=ACCENT_RED_CL,
                                    alignment=TA_CENTER, fontName="Helvetica-Bold"),
    }


def header_footer(canvas, doc):
    W, H = A4
    canvas.saveState()
    canvas.setFillColor(DARK_BLUE_CL)
    canvas.rect(0, H - 22*mm, W, 22*mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(W/2, H - 13*mm,
        "AML Valvetrain Engineering — EXCITE TD Dynamics Analysis")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LIGHT_BLUE_CL)
    canvas.drawRightString(W - 15*mm, H - 19*mm,
        f"AML AE26 ChainDrive 04 spring_update_redMass | 2026-06-19")
    canvas.setFillColor(DARK_BLUE_CL)
    canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(15*mm, 3.5*mm, "Confidential — Internal Engineering Document")
    canvas.drawRightString(W - 15*mm, 3.5*mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf_section(fig_paths, summary_rows, out_path, speeds):
    st = _styles()
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        topMargin=28*mm, bottomMargin=16*mm,
        leftMargin=15*mm, rightMargin=15*mm,
        title="HLIF Pump-Up Analysis — redMass", author="AML Engineering",
    )
    story = []

    title_data = [[Paragraph(
        "5. EXCITE TD Dynamic Analysis — Intake HLA Pump-Up (Reduced Mass Variant)",
        st["h1"])]]
    title_tbl = Table(title_data, colWidths=[180*mm])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE_CL),
        ("TEXTCOLOR",  (0,0), (-1,-1), colors.white),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))
    story.append(title_tbl)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("5.1  Simulation Setup", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    model_info = [
        ["Parameter", "Value"],
        ["Model", f"{MODEL}.etd"],
        ["Variant", "Reduced mass (redMass) — follower mass reduction vs. 04_spring_update"],
        ["Speed cases", ", ".join(f"{s} rpm" for s in speeds)],
        ["Simulation duration", "15 cam cycles (5400° cam angle)"],
        ["Intake elements analysed", "16  (INTL_HLIF1–8, INTr_HLIF1–8)"],
        ["Pump-up detection threshold", f"{PUMP_UP_THRESHOLD_MM} mm min. lift on base circle"],
        ["Result channel", "HLIF_xxx.GID — 'lift' column (col. 5)"],
        ["Software", "AVL EXCITE Timing Drive R2024.1"],
    ]
    col_w = [70*mm, 110*mm]
    info_tbl = Table(model_info, colWidths=col_w)
    info_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE_CL),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 8.5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, STRIPE_CL]),
        ("GRID",       (0,0), (-1,-1), 0.3, colors.HexColor("#BBBBBB")),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("ALIGN",      (0,0), (-1,-1), "LEFT"),
        ("LEFTPADDING",(0,0), (-1,-1), 5),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("5.2  Results", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    fig_captions = [
        ("Fig. 5-1: HLA Lift — Last 2 Cam Cycles",
         "HLA plunger lift for INTL_HLIF1 (left bank) and INTr_HLIF1 (right bank) "
         "over the last two cam cycles. Non-zero base-circle lift indicates pump-up. "
         "Dashed red line = 0.10 mm threshold."),
        ("Fig. 5-2: Pump-Up Envelope — Max/Min Lift per Cycle",
         "Cycle-by-cycle max (solid) and min (dashed) HLA lift. Rising maxima or "
         "non-converging minima indicate continuing pump-up growth across 15 cycles."),
        ("Fig. 5-3: Speed Sweep — Max Lift at Last Cycle",
         "Max HLA lift in the last cam cycle vs. engine speed for all 16 intake elements. "
         "7 speed points: 7000, 7300, 7400, 7500, 7600, 7700, 7800 rpm."),
        ("Fig. 5-4: HLA Working Pressure — Last 2 Cam Cycles",
         "HLA working pressure over last 2 cycles. Elevated base-circle pressure "
         "corroborates pump-up detected via the lift signal."),
    ]

    img_w = 175*mm
    img_h = img_w * 5.0 / 14.0

    for fig_path, (cap_title, cap_text) in zip(fig_paths, fig_captions):
        if not os.path.isfile(fig_path):
            continue
        story.append(KeepTogether([
            Image(fig_path, width=img_w, height=img_h),
            Spacer(1, 1.5*mm),
            Paragraph(f"<b>{cap_title}</b>  {cap_text}", st["note"]),
            Spacer(1, 5*mm),
        ]))

    story.append(PageBreak())

    story.append(Paragraph("5.3  Pump-Up Summary — All Intake Elements", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    hdr = [
        Paragraph("Element",          st["cell_hdr"]),
        Paragraph("Speed\n[rpm]",     st["cell_hdr"]),
        Paragraph("Max lift\n[mm]",   st["cell_hdr"]),
        Paragraph("Min lift\n[mm]",   st["cell_hdr"]),
        Paragraph("Pump-up?",         st["cell_hdr"]),
        Paragraph("Max wk. press.\n[bar]", st["cell_hdr"]),
    ]
    tbl_rows = [hdr]
    flag_rows = []
    for i, (elem, rpm, max_l, min_l, pump_up, max_p) in enumerate(summary_rows):
        flag = "YES !" if pump_up else "no"
        cell_style = st["cell_warn"] if pump_up else st["cell"]
        tbl_rows.append([
            Paragraph(elem, st["cell"]),
            Paragraph(str(rpm), st["cell"]),
            Paragraph(f"{max_l:.4f}", st["cell"]),
            Paragraph(f"{min_l:.4f}", st["cell"]),
            Paragraph(flag, cell_style),
            Paragraph(f"{max_p:.1f}", st["cell"]),
        ])
        if pump_up:
            flag_rows.append(i + 1)

    col_w2 = [35*mm, 20*mm, 22*mm, 22*mm, 20*mm, 30*mm]
    sum_tbl = Table(tbl_rows, colWidths=col_w2, repeatRows=1)
    ts2 = TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK_BLUE_CL),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, STRIPE_CL]),
        ("GRID",         (0,0), (-1,-1), 0.3, colors.HexColor("#BBBBBB")),
    ])
    for r in flag_rows:
        ts2.add("BACKGROUND", (4,r), (4,r), colors.HexColor("#FDECEA"))
    sum_tbl.setStyle(ts2)
    story.append(sum_tbl)
    story.append(Spacer(1, 3*mm))

    n_pumpup = sum(1 for _, _, _, _, pu, _ in summary_rows if pu)
    story.append(Paragraph(
        f"★  {n_pumpup} of {len(summary_rows)} element-speed combinations exceed the "
        f"{PUMP_UP_THRESHOLD_MM} mm pump-up threshold (last cam cycle).",
        st["note"]))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("5.4  Interpretation and Engineering Assessment", st["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=MID_BLUE_CL))
    story.append(Spacer(1, 2*mm))

    max_speed_pu = max((rpm for _, rpm, _, _, pu, _ in summary_rows if pu), default=None)
    min_speed_pu = min((rpm for _, rpm, _, _, pu, _ in summary_rows if pu), default=None)

    interp_text = (
        f"The EXCITE TD dynamic simulation of the <b>{MODEL}</b> model covers "
        f"seven speed points ({', '.join(str(s) for s in speeds)} rpm) over "
        "15 cam cycles (5400°) each — an extended run providing better convergence "
        "than the predecessor model.  Results are evaluated at the last complete "
        "cam cycle.<br/><br/>"
    )
    if n_pumpup == 0:
        interp_text += (
            "<b>No pump-up detected</b> in any intake HLA element across the full "
            "speed range (7000–7800 rpm). The reduced-mass variant maintains HLA "
            f"plunger lift below the {PUMP_UP_THRESHOLD_MM} mm threshold at all "
            "conditions, confirming that the follower mass reduction is beneficial "
            "for HLA stability at high engine speeds."
        )
    else:
        interp_text += (
            f"<b>Pump-up detected</b> in {n_pumpup} element-speed combination(s). "
            f"First onset at <b>{min_speed_pu} rpm</b>, persisting to "
            f"<b>{max_speed_pu} rpm</b>. "
            "Compare directly with Section 4 (04_spring_update baseline) to assess "
            "whether the mass reduction shifted the pump-up onset speed upward. "
            "If onset speed increased, the reduced-mass design is an improvement; "
            "if unchanged or lower, spring seat load is the limiting factor.<br/><br/>"
            "Recommended actions: (1) Plot pump-up onset speed vs. follower mass for "
            "both variants. (2) Check HLA bleed orifice sizing against peak working "
            "pressures at affected speeds."
        )

    story.append(Paragraph(interp_text, st["body"]))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        f"Analysis performed on AVL EXCITE TD R2024.1 results — {MODEL}.etd. "
        f"Results auto-generated by analyze_hlif_redmass.py — 2026-06-19.",
        st["note"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF section written: {out_path}")


def merge_pdfs(base_pdf, section_pdf, out_pdf):
    writer = PdfWriter()
    for src in [base_pdf, section_pdf]:
        if os.path.isfile(src):
            reader = PdfReader(src)
            for page in reader.pages:
                writer.add_page(page)
    with open(out_pdf, "wb") as f:
        writer.write(f)
    print(f"Merged PDF written: {out_pdf}")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    tmp_dir = tempfile.mkdtemp(prefix="hlif_redmass_")
    fig1 = os.path.join(tmp_dir, "fig1_lift_history.png")
    fig2 = os.path.join(tmp_dir, "fig2_pumpup_envelope.png")
    fig3 = os.path.join(tmp_dir, "fig3_speed_sweep.png")
    fig4 = os.path.join(tmp_dir, "fig4_working_pressure.png")

    print("=== HLIF Pump-Up Analysis — redMass ===")
    print(f"Model  : {MODEL}")
    print(f"ETD dir: {ETD_DIR}")

    print("\n[1/5] Loading HLIF data ...")
    speeds, data = collect_all_data()
    if not speeds:
        print("ERROR: No speed cases found.")
        return

    print("\n[2/5] Generating figures ...")
    fig_lift_timehist(speeds, data, fig1)
    fig_pumpup_envelope(speeds, data, fig2)
    fig_speed_sweep(speeds, data, fig3)
    fig_working_pressure(speeds, data, fig4)

    print("\n[3/5] Building summary table ...")
    summary = build_summary_table(speeds, data)
    n_pu = sum(1 for r in summary if r[4])
    print(f"  Total entries: {len(summary)},  pump-up flags: {n_pu}")

    print("\n[4/5] Building PDF section ...")
    build_pdf_section([fig1, fig2, fig3, fig4], summary, HLIF_PDF, speeds)

    print("\n[5/5] Merging into main PDF ...")
    merge_pdfs(MAIN_PDF, HLIF_PDF, OUTPUT_PDF)

    for p in [fig1, fig2, fig3, fig4]:
        try: os.remove(p)
        except: pass
    try: os.rmdir(tmp_dir)
    except: pass
    try: os.remove(HLIF_PDF)
    except: pass

    print(f"\nDone.  Updated PDF: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
