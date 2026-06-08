#!/usr/bin/env python3
"""
Generate PDF documentation for valvetrain_viewer.py
Run once:  python generate_viewer_doc.py
"""

import os
import sys
import numpy as np
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── Paths ─────────────────────────────────────────────────────────────────────
HERE     = Path(__file__).parent
OUT_PDF  = HERE / "valvetrain_viewer_documentation.pdf"
IMG_DIR  = HERE / "_doc_imgs"
IMG_DIR.mkdir(exist_ok=True)

BASE_DIR = Path(
    r"D:\AW82001\5005\ref_Tamas\AW82001_5004_20-Loop1-ModelStatus"
    r"\Status20260608\excite_td"
)
MODEL = "vtRBint01.Ref_C10"
RPMS  = [7000, 7100, 7200, 7300, 7400, 7500]
RPM_COLORS = ["#1E88E5", "#43A047", "#FB8C00", "#8E24AA", "#E53935", "#00ACC1"]

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_gid_data(filepath):
    import re
    text = Path(filepath).read_text(encoding="latin-1")
    end_pos = text.find("END\r\n")
    if end_pos < 0:
        end_pos = text.find("END\n")
    header = text[:end_pos]
    m = re.search(r"CHANNEL\s*=\s*\[(.*?)\]", header, re.DOTALL)
    raw = re.sub(r"[\r\n\t&]", " ", m.group(1))
    channels = [v.strip().strip("'") for v in re.split(r",\s*", raw) if v.strip().strip("'")]
    skip = 5 if text[end_pos:end_pos+5] == "END\r\n" else 4
    vals = np.fromstring(text[end_pos + skip:], sep=" ")
    n = len(channels)
    data = vals.reshape(-1, n) if len(vals) % n == 0 else None
    return channels, data


def last_cycle(x_raw, y_raw):
    """Fold last complete 720° cycle to [0, 720)."""
    mask  = x_raw >= (x_raw[-1] - 720.0)
    x_cyc = x_raw[mask] % 720.0
    y_cyc = y_raw[mask]
    order = np.argsort(x_cyc)
    return x_cyc[order], y_cyc[order]


# ── Figure 1 – sample lift curves all RPMs ────────────────────────────────────
def make_fig_lift():
    fig, ax = plt.subplots(figsize=(13, 4.5))
    ax.set_facecolor("#F9F9F9")
    ax.grid(True, color="#E0E0E0", linewidth=0.7, linestyle="--")

    comp = "VAFA_10"
    for rpm, col in zip(RPMS, RPM_COLORS):
        f = BASE_DIR / f"{MODEL}.{rpm}rpm" / "results" / f"{comp}.GID"
        if not f.exists():
            continue
        chs, data = parse_gid_data(f)
        xi = chs.index("equiv. crank angle")
        yi = chs.index("lift")
        x, y = last_cycle(data[:, xi], data[:, yi] * 1000)
        ax.plot(x, y, color=col, linewidth=1.5, label=f"{rpm} rpm")

    ax.set_xlabel("Crank Angle  [°]", fontsize=11)
    ax.set_ylabel("Valve Lift  [mm]", fontsize=11)
    ax.set_title("INTr_VAFA1 — Valve Lift vs. Crank Angle  (7000 – 7500 rpm)", fontsize=12)
    ax.set_xlim(0, 720)
    ax.set_xticks(range(0, 721, 90))
    ax.legend(fontsize=9, loc="upper right", framealpha=0.85)
    fig.tight_layout()
    p = IMG_DIR / "fig_lift.png"
    fig.savefig(p, dpi=120)
    plt.close(fig)
    return p


# ── Figure 2 – contact pressure all RPMs ─────────────────────────────────────
def make_fig_contact():
    fig, ax = plt.subplots(figsize=(13, 4.5))
    ax.set_facecolor("#F9F9F9")
    ax.grid(True, color="#E0E0E0", linewidth=0.7, linestyle="--")

    comp = "CLUB_7"
    for rpm, col in zip(RPMS, RPM_COLORS):
        f = BASE_DIR / f"{MODEL}.{rpm}rpm" / "results" / f"{comp}.GID"
        if not f.exists():
            continue
        chs, data = parse_gid_data(f)
        xi = chs.index("equiv. crank angle")
        yi = chs.index("contact stress")
        x, y = last_cycle(data[:, xi], data[:, yi] / 1e6)
        ax.plot(x, y, color=col, linewidth=1.5, label=f"{rpm} rpm")

    ax.set_xlabel("Crank Angle  [°]", fontsize=11)
    ax.set_ylabel("Contact Pressure  [MPa]", fontsize=11)
    ax.set_title("INTr_CLUB1 — Hertzian Contact Pressure vs. Crank Angle  (7000 – 7500 rpm)", fontsize=12)
    ax.set_xlim(0, 720)
    ax.set_xticks(range(0, 721, 90))
    ax.legend(fontsize=9, loc="upper right", framealpha=0.85)
    fig.tight_layout()
    p = IMG_DIR / "fig_contact.png"
    fig.savefig(p, dpi=120)
    plt.close(fig)
    return p


# ── Figure 3 – GUI layout diagram ─────────────────────────────────────────────
def make_fig_layout():
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 12); ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_facecolor("#ECEFF1")
    fig.patch.set_facecolor("#ECEFF1")

    def box(x, y, w, h, fc, ec, lw=1.5):
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.05",
            facecolor=fc, edgecolor=ec, linewidth=lw))

    # Window
    box(0.1, 0.1, 11.8, 4.8, "#FAFAFA", "#90A4AE", 2)
    ax.text(6, 4.6, "Valvetrain Result Viewer — AVL Excite Timing Drive  |  vtRBint01.Ref_C10",
            ha="center", va="center", fontsize=9, color="#263238", fontweight="bold")

    # Left panel
    box(0.2, 0.2, 2.8, 4.2, "#F5F5F5", "#607D8B")
    ax.text(1.6, 4.15, "Results Browser", ha="center", fontsize=8, fontweight="bold", color="#263238")

    # Category headers
    for i, (cat, col) in enumerate([("Valve Lift", "#1565C0"),
                                     ("Contact Pressure", "#B71C1C"),
                                     ("Spring Force", "#E65100")]):
        y0 = 3.6 - i * 1.1
        box(0.25, y0, 2.7, 0.28, col, col)
        ax.text(1.6, y0 + 0.14, cat, ha="center", va="center",
                fontsize=7, color="white", fontweight="bold")
        # RPM tiles
        rpm_cols = ["#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#FFEBEE", "#E0F7FA"]
        borders  = ["#1565C0", "#2E7D32", "#E65100", "#6A1B9A", "#B71C1C", "#006064"]
        for j, (bg, bd) in enumerate(zip(rpm_cols, borders)):
            tx = 0.27 + j * 0.44
            box(tx, y0 - 0.65, 0.40, 0.55, bg, bd, 1.0)
            ax.text(tx + 0.20, y0 - 0.38, f"{7000+j*100}", ha="center",
                    va="center", fontsize=5.5, color=bd)

    # Right panel
    box(3.2, 0.2, 8.7, 4.2, "#FAFAFA", "#607D8B")

    # Top subplot
    box(3.3, 2.3, 8.5, 1.9, "#F9F9F9", "#B0BEC5")
    ax.text(7.55, 3.35, "Valve Lift  [mm]  vs.  Crank Angle  [°]",
            ha="center", fontsize=8, color="#263238", style="italic")
    for j, col in enumerate(RPM_COLORS[:3]):
        xs = np.linspace(0, 8.3, 80)
        ys = 2.35 + 1.7 * np.clip(
            np.sin(np.pi * (xs / 8.3 - 0.3) * 1.5) ** 6 * (xs / 8.3 > 0.3), 0, 1
        ) * (0.9 - j * 0.05)
        ax.plot(xs + 3.35, ys, color=col, linewidth=1.2, alpha=0.85)

    # Bottom subplot
    box(3.3, 0.3, 8.5, 1.85, "#F9F9F9", "#B0BEC5")
    ax.text(7.55, 0.82, "Contact Pressure  [MPa]  vs.  Crank Angle  [°]",
            ha="center", fontsize=8, color="#263238", style="italic")
    for j, col in enumerate(RPM_COLORS[:3]):
        xs = np.linspace(0, 8.3, 80)
        noise = 0.3 * np.sin(xs * 12 + j)
        base  = 0.32 + 0.95 * np.clip(
            np.sin(np.pi * (xs / 8.3 - 0.3) * 1.5) ** 2 * (xs / 8.3 > 0.3), 0, 1
        ) * (0.9 - j * 0.05) + noise * np.clip(xs/8.3-0.3, 0, 1)
        ax.plot(xs + 3.35, np.clip(base + 0.3, 0.31, 2.05), color=col, linewidth=1.0, alpha=0.8)

    # Drag arrow
    ax.annotate("", xy=(3.25, 2.8), xytext=(3.05, 2.8),
                arrowprops=dict(arrowstyle="->", color="#E53935", lw=2))
    ax.text(3.15, 3.0, "drag\n& drop", ha="center", fontsize=6.5, color="#E53935")

    fig.tight_layout(pad=0)
    p = IMG_DIR / "fig_layout.png"
    fig.savefig(p, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return p


# ── PDF builder ───────────────────────────────────────────────────────────────
def build_pdf(fig_lift, fig_contact, fig_layout):
    doc = SimpleDocTemplate(
        str(OUT_PDF), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    W = A4[0] - 4*cm   # usable width

    # Custom styles
    h1 = ParagraphStyle("H1", parent=styles["Heading1"],
                         fontSize=18, spaceAfter=6, textColor=colors.HexColor("#1A237E"))
    h2 = ParagraphStyle("H2", parent=styles["Heading2"],
                         fontSize=13, spaceAfter=4, textColor=colors.HexColor("#283593"))
    h3 = ParagraphStyle("H3", parent=styles["Heading3"],
                         fontSize=10, spaceAfter=3, textColor=colors.HexColor("#37474F"))
    body = ParagraphStyle("Body", parent=styles["Normal"],
                           fontSize=9.5, leading=14, alignment=TA_JUSTIFY)
    code = ParagraphStyle("Code", parent=styles["Code"],
                           fontSize=8.5, leading=12, backColor=colors.HexColor("#F5F5F5"),
                           leftIndent=12, rightIndent=12)
    note = ParagraphStyle("Note", parent=styles["Normal"],
                           fontSize=8.5, leading=12, textColor=colors.HexColor("#546E7A"),
                           leftIndent=8)

    story = []

    # ── Title page ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Valvetrain Result Viewer", h1))
    story.append(Paragraph("AVL Excite Timing Drive — Technical Documentation", h2))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#3949AB")))
    story.append(Spacer(1, 0.3*cm))

    meta_data = [
        ["Project",  "AW82001 — V8 Engine Valvetrain Dynamic Analysis"],
        ["Model",    "vtRBint01.Ref_C10  (Intake Right Bank, Reference Config C10)"],
        ["Software", "AVL Excite Timing Drive"],
        ["Scope",    "Valvetrain functionality verification up to 7 500 rpm"],
        ["Tool",     "valvetrain_viewer.py  (PySide6 + Matplotlib interactive GUI)"],
        ["Date",     "2026-06-08"],
    ]
    tbl = Table(meta_data, colWidths=[3.5*cm, W - 3.5*cm])
    tbl.setStyle(TableStyle([
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("FONTNAME",    (0, 0), (0, -1),  "Helvetica-Bold"),
        ("TEXTCOLOR",   (0, 0), (0, -1),  colors.HexColor("#283593")),
        ("BACKGROUND",  (0, 0), (-1, -1), colors.HexColor("#F8F9FF")),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#C5CAE9")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#F8F9FF"),
                                               colors.HexColor("#FFFFFF")]),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.8*cm))

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story.append(Paragraph("1.  Overview", h2))
    story.append(Paragraph(
        "The Valvetrain Result Viewer is an interactive desktop application for post-processing "
        "AVL Excite Timing Drive simulation results. Its primary purpose is to verify valvetrain "
        "functionality — valve lift, Hertzian contact pressure, and spring behaviour — across the "
        "engine speed range 7 000 – 7 500 rpm for model <b>vtRBint01.Ref_C10</b>.",
        body))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "The tool uses a <b>drag-and-drop</b> workflow: result tiles in the left panel represent "
        "individual signal channels from the GID result files; dragging a tile onto the plot "
        "canvas instantly loads and displays the time-history curve against crank angle. "
        "Multiple tiles from different RPM points or engine components can be overlaid on the same "
        "subplot for direct comparison.",
        body))
    story.append(Spacer(1, 0.5*cm))

    # ── 2. GUI layout ─────────────────────────────────────────────────────────
    story.append(Paragraph("2.  GUI Layout", h2))
    story.append(Image(str(fig_layout), width=W, height=W * 5/12))
    story.append(Paragraph(
        "Figure 1 — Schematic of the application window. "
        "Left: Results Browser with colour-coded RPM tiles. "
        "Right: dual-subplot canvas (Valve Lift top, Contact Pressure bottom).",
        note))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("2.1  Results Browser (left panel)", h3))
    story.append(Paragraph(
        "The left panel lists all available signal channels for all six RPM operating points "
        "simultaneously. Tiles are organised hierarchically: <b>signal category</b> → "
        "<b>RPM sub-header</b> → <b>component tile</b>. "
        "Each tile is colour-coded by engine speed (see Table 1) to make it easy to identify "
        "at a glance which operating point is being added to the plot.",
        body))
    story.append(Spacer(1, 0.2*cm))

    rpm_table = [["Engine Speed", "Tile Colour"]] + [
        [f"{rpm} rpm", f"{'■ ' + bg}" ]
        for rpm, (bg, _) in {
            7000: ("#E3F2FD (light blue)",  ""), 7100: ("#E8F5E9 (light green)", ""),
            7200: ("#FFF3E0 (light orange)",""), 7300: ("#F3E5F5 (light purple)",""),
            7400: ("#FFEBEE (light red)",   ""), 7500: ("#E0F7FA (light teal)",  ""),
        }.items()
    ]
    rpm_table = [
        ["Engine Speed", "Background colour"],
        ["7 000 rpm", "#E3F2FD  (light blue)"],
        ["7 100 rpm", "#E8F5E9  (light green)"],
        ["7 200 rpm", "#FFF3E0  (light orange)"],
        ["7 300 rpm", "#F3E5F5  (light purple)"],
        ["7 400 rpm", "#FFEBEE  (light red)"],
        ["7 500 rpm", "#E0F7FA  (light teal)"],
    ]
    t = Table(rpm_table, colWidths=[4.5*cm, W - 4.5*cm])
    t.setStyle(TableStyle([
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3949AB")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#C5CAE9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [colors.HexColor(c) for c in
             ["#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#FFEBEE", "#E0F7FA"]]),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Paragraph("Table 1 — RPM colour coding of result tiles.", note))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("2.2  Plot Canvas (right panel)", h3))
    story.append(Paragraph(
        "The plot area contains two stacked subplots sharing the x-axis (crank angle 0 – 720°). "
        "Routing of dropped tiles is automatic: "
        "<b>Valve Lift</b> and <b>Valve Seat Force</b> tiles always appear on the <i>top</i> subplot; "
        "<b>Contact Pressure</b> and <b>Contact Force</b> tiles appear on the <i>bottom</i> subplot. "
        "Other signal categories (spring force, lash adjuster, …) default to the top subplot. "
        "Data is extracted from the last complete 720° crank-angle cycle recorded in the GID file "
        "and normalised to the range 0 – 720°.",
        body))
    story.append(Spacer(1, 0.5*cm))

    # ── 3. Signal categories ──────────────────────────────────────────────────
    story.append(Paragraph("3.  Available Signal Categories", h2))
    cat_table_data = [
        ["Category", "Source file prefix", "Channel", "Unit", "Subplot"],
        ["Valve Lift",          "VAFA_", "lift",               "mm",  "Top"],
        ["Valve Seat Force",    "VAFA_", "seat force",         "N",   "Top"],
        ["Contact Pressure",    "CLUB_", "contact stress",     "MPa", "Bottom"],
        ["Contact Force",       "CDAT_", "force",              "N",   "Bottom"],
        ["Spring Force",        "CTOR_", "force",              "N",   "Top"],
        ["Spring Coil Contact", "SPPR_", "force coil contact", "N",   "Top"],
        ["Lash Adjuster",       "HLIF_", "lift / force / pressure", "mm / N / Pa", "Top"],
        ["Finger Follower",     "FIFO_", "lift / force",       "mm / N", "Top"],
    ]
    ct = Table(cat_table_data, colWidths=[3.8*cm, 2.8*cm, 3.6*cm, 2.0*cm, 1.8*cm])
    ct.setStyle(TableStyle([
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#283593")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#C5CAE9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [colors.HexColor("#F8F9FF"), colors.white]),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ]))
    story.append(ct)
    story.append(Paragraph(
        "Table 2 — Result categories, source file prefixes, and default subplot assignment. "
        "Units are converted automatically: m→mm for lift, N/m²→MPa for contact stress.",
        note))
    story.append(Spacer(1, 0.6*cm))

    # ── 4. Results ────────────────────────────────────────────────────────────
    story.append(Paragraph("4.  Sample Results  (INTr_VAFA1 / INTr_CLUB1)", h2))

    story.append(Paragraph("4.1  Valve Lift", h3))
    story.append(Image(str(fig_lift), width=W, height=W * 4.5/13))
    story.append(Paragraph(
        "Figure 2 — Valve lift (INTr_VAFA1, intake valve 1, right bank) vs. crank angle "
        "for all six speed points 7 000 – 7 500 rpm.  The curves are nearly identical, "
        "indicating stable kinematic behaviour across the speed range.  "
        "Peak lift ≈ 9.95 mm.",
        note))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("4.2  Cam–Follower Contact Pressure", h3))
    story.append(Image(str(fig_contact), width=W, height=W * 4.5/13))
    story.append(Paragraph(
        "Figure 3 — Hertzian contact pressure (INTr_CLUB1, cam–follower contact, right bank) "
        "vs. crank angle.  Peak pressures reach approximately 1 170 MPa in the opening/closing "
        "flanks at 7 500 rpm.  Pressure oscillations during the lift event are caused by dynamic "
        "contact force variation (spring surge, follower inertia).",
        note))
    story.append(Spacer(1, 0.6*cm))

    # ── 5. Data structure ─────────────────────────────────────────────────────
    story.append(Paragraph("5.  Data Structure and File Format", h2))
    story.append(Paragraph(
        "Results are stored in <b>AVL GID</b> text files (ASCII, Latin-1 encoding). "
        "Each file contains a structured header block followed by columnar numeric data. "
        "The header is delimited by <code>BEGIN</code> / <code>END</code> keywords and "
        "defines the simulation speed, component name (<code>objectname</code>), channel names, "
        "and units. Continuation lines use the <code>&amp;</code> character.",
        body))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Example GID header (VAFA_10.GID):", h3))
    gid_sample = (
        "BEGIN\n"
        "  speed = '0.700000E+04'\n"
        "  objectname = 'INTr_VAFA1'\n"
        "  CHANNEL = ['time', &\n"
        "    'equiv. cam angle', &\n"
        "    'equiv. crank angle', &\n"
        "    'ref. angle', &\n"
        "    'lift', 'velocity', 'acceleration', 'force', 'seat force']\n"
        "  UNIT = ['s', 'deg', 'deg', 'deg', 'm', 'm/s', 'm/s^2', 'N', 'N']\n"
        "END\n"
        "  0.034309  720.499  1440.998  720.499  -1.576e-05  -0.00690  -80.95  -179.2  3947.8\n"
        "  ..."
    )
    story.append(Paragraph(gid_sample.replace("\n", "<br/>"), code))
    story.append(Spacer(1, 0.4*cm))

    dir_table = [
        ["Path element", "Description"],
        ["excite_td/",                      "Root result directory"],
        [f"  {MODEL}/",                     "AllCaseSet summary (speed-sweep statistics)"],
        [f"  {MODEL}.7000rpm/results/",     "Time-domain results at 7 000 rpm"],
        ["  …",                             "7 100 – 7 500 rpm (same structure)"],
        ["    VAFA_<id>.GID",               "Valve analysis: lift, velocity, force, seat force"],
        ["    CLUB_<id>.GID",               "Contact lubrication: Hertzian stress, OFT, friction"],
        ["    CDAT_<id>.GID",               "Cam data / contact force, friction moment"],
        ["    SPPR_<id>.GID",               "Spring coil: force, coil contact force"],
        ["    CTOR_<id>.GID",               "End-coil spring force"],
        ["    HLIF_<id>.GID",               "Hydraulic lash adjuster: lift, pressure, flow"],
        ["    FIFO_<id>.GID",               "Finger follower: lift, force"],
    ]
    dt = Table(dir_table, colWidths=[6.5*cm, W - 6.5*cm])
    dt.setStyle(TableStyle([
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#455A64")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#CFD8DC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [colors.HexColor("#ECEFF1"), colors.white]),
        ("FONTNAME",   (0, 1), (0, -1), "Courier"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ]))
    story.append(dt)
    story.append(Paragraph("Table 3 — Directory layout of the excite_td result tree.", note))
    story.append(Spacer(1, 0.6*cm))

    # ── 6. Usage ─────────────────────────────────────────────────────────────
    story.append(Paragraph("6.  Usage Instructions", h2))
    steps = [
        ("<b>Launch</b>",
         "Open a terminal in the project directory and run:<br/>"
         "<code>python valvetrain_viewer.py</code><br/>"
         "The application starts loading all six RPM catalogs in the background."),
        ("<b>Browse tiles</b>",
         "The Results Browser (left panel) lists signal tiles grouped by category and RPM. "
         "Scroll down to see all eight categories.  The tile colour indicates the engine speed."),
        ("<b>Drag a tile</b>",
         "Click and hold any tile, then drag it onto the plot canvas.  "
         "Release the mouse to drop.  The curve appears immediately on the appropriate subplot."),
        ("<b>Overlay multiple curves</b>",
         "Drag additional tiles from the same category but different RPM points to compare speeds.  "
         "Repeat for different valve components (INTr_VAFA1 – VAFA8) to compare cylinders."),
        ("<b>Navigate the plot</b>",
         "Use the matplotlib toolbar (zoom, pan, home, save) at the top right of the canvas."),
        ("<b>Remove curves</b>",
         "<i>Remove last</i> undoes the most recently added curve.  "
         "<i>Clear all</i> resets both subplots."),
    ]
    for num, (title, desc) in enumerate(steps, 1):
        story.append(Paragraph(f"{num}.  {title}", h3))
        story.append(Paragraph(desc, body))
        story.append(Spacer(1, 0.15*cm))
    story.append(Spacer(1, 0.4*cm))

    # ── 7. Dependencies ───────────────────────────────────────────────────────
    story.append(Paragraph("7.  Software Dependencies", h2))
    dep_table = [
        ["Package", "Version tested", "Purpose"],
        ["Python",      "3.13+",  "Runtime"],
        ["PySide6",     "6.11.0", "Qt6 GUI framework (window, drag & drop)"],
        ["matplotlib",  "3.10.9", "Embedded plot canvas, navigation toolbar"],
        ["numpy",       "2.4.4",  "Numeric array operations, data parsing"],
        ["reportlab",   "any",    "PDF documentation generation (this document)"],
    ]
    dep_t = Table(dep_table, colWidths=[3.5*cm, 3.0*cm, W - 6.5*cm])
    dep_t.setStyle(TableStyle([
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#37474F")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#CFD8DC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [colors.HexColor("#ECEFF1"), colors.white]),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]))
    story.append(dep_t)

    doc.build(story)
    print(f"PDF written -> {OUT_PDF}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating figures …")
    fig_lift    = make_fig_lift()
    fig_contact = make_fig_contact()
    fig_layout  = make_fig_layout()
    print("Building PDF …")
    build_pdf(fig_lift, fig_contact, fig_layout)
    import shutil
    shutil.rmtree(IMG_DIR, ignore_errors=True)
    print("Done.")
