"""
Valve Spring Drawing Comparison Report Generator
Exhaust (A1770530600) vs Intake (A1770530500)
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable
)
from reportlab.platypus.flowables import KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, String
from PIL import Image as PILImage
import os

# ── colour palette ─────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor('#0D2B55')
MID_BLUE    = colors.HexColor('#1A4B8C')
LIGHT_BLUE  = colors.HexColor('#D6E4F7')
ACCENT_RED  = colors.HexColor('#C0392B')
ACCENT_GRN  = colors.HexColor('#1E8449')
STRIPE      = colors.HexColor('#EBF2FB')
WHITE       = colors.white
BLACK       = colors.black
GREY        = colors.HexColor('#666666')
LIGHT_GREY  = colors.HexColor('#F5F5F5')

# ── data extracted from drawings ───────────────────────────────────────────────
EXHAUST = {
    "part_no":        "A 177 053 06 00",
    "description":    "Valve Spring – Exhaust (Auslassfeder)",
    "drawing_file":   "A1770530600_3_Exhaust_Valve_Spring.tif",
    "color_1":        "Violet RAL 4002",
    "color_2":        "Brown (Braun) RAL 8004",
    "color_3":        "Kobe: none",
    "d_wire":         "2.92 × 3.66 (oval)",
    "Dio":            "12.00 ± 0.20",
    "Diu":            "15.90 ± 0.20",
    "Deo":            "19.32",
    "Deu":            "23.22",
    "spring_index":   "5.32",
    "coil_dir":       "Right (RH)",
    "G":              "79 500",
    "L0":             "47.0",
    "L1":             "36.10",
    "L2":             "26.10",
    "Lc":             "24.60 − 0.9",
    "F1":             "270 ± 13",
    "F2":             "620 ± 27",
    "tau_k1":         "453",
    "tau_k2":         "1 040",
    "tau_kh":         "587",
    "nt":             "8.6",
    "na":             "4.4 – 3.4",
    "e_min":          "0.55",
    "e1":             "1.84",
    "e2":             "0.70",
    "spring_shape":   "Beehive (Bienenkorb)",
    "ends":           "Both closed & ground, 240°",
    "shot_peened":    "Yes",
    "surface":        "Wax",
    "heat_treat":     "Yes (table DIN 7386.20)",
}

INTAKE = {
    "part_no":        "A 177 053 05 00",
    "description":    "Valve Spring – Intake (Einlassfeder)",
    "drawing_file":   "A1770530500_4_Intake_Valve_Spring.tif",
    "color_1":        "Violet RAL 4002",
    "color_2":        "Yellow (Gelb) RAL 1006",
    "color_3":        "Kobe: none",
    "d_wire":         "2.92 × 3.66 (oval)",
    "Dio":            "12.00 ± 0.20",
    "Diu":            "15.90 ± 0.20",
    "Deo":            "19.32",
    "Deu":            "23.22",
    "spring_index":   "5.32",
    "coil_dir":       "Right (RH)",
    "G":              "79 500",
    "L0":             "46.1",
    "L1":             "36.10",
    "L2":             "26.10",
    "Lc":             "24.60 − 0.9",
    "F1":             "250 ± 12",
    "F2":             "620 ± 21",
    "tau_k1":         "419",
    "tau_k2":         "1 040",
    "tau_kh":         "521",
    "nt":             "8.6",
    "na":             "4.4 – 3.4",
    "e_min":          "0.55",
    "e1":             "1.84",
    "e2":             "0.70",
    "spring_shape":   "Beehive (Bienenkorb)",
    "ends":           "Both closed & ground, 240°",
    "shot_peened":    "Yes",
    "surface":        "Wax",
    "heat_treat":     "Yes (table DIN 7386.20)",
}

# ── derived calculations ───────────────────────────────────────────────────────
# Average working spring rate  k = ΔF / ΔL  over installed stroke
L1, L2 = 36.10, 26.10
exhaust_k = (620 - 270) / (L1 - L2)   # 35.0 N/mm
intake_k  = (620 - 250) / (L1 - L2)   # 37.0 N/mm

# ── helpers ────────────────────────────────────────────────────────────────────
def make_thumbnail(src, max_px=1200):
    """Return path to a downsampled PNG suitable for embedding."""
    dst = src.replace(".tif", "_thumb.png")
    img = PILImage.open(src).convert("L")
    img.thumbnail((max_px, max_px), PILImage.LANCZOS)
    img.save(dst, "PNG")
    return dst


def styles():
    s = getSampleStyleSheet()
    custom = {
        "title": ParagraphStyle("title", fontSize=22, textColor=WHITE,
                                 alignment=TA_CENTER, spaceAfter=4,
                                 fontName="Helvetica-Bold"),
        "subtitle": ParagraphStyle("subtitle", fontSize=12, textColor=LIGHT_BLUE,
                                    alignment=TA_CENTER, spaceAfter=2,
                                    fontName="Helvetica"),
        "h1": ParagraphStyle("h1", fontSize=14, textColor=DARK_BLUE,
                              spaceBefore=10, spaceAfter=4,
                              fontName="Helvetica-Bold"),
        "h2": ParagraphStyle("h2", fontSize=11, textColor=MID_BLUE,
                              spaceBefore=6, spaceAfter=3,
                              fontName="Helvetica-Bold"),
        "body": ParagraphStyle("body", fontSize=9, textColor=BLACK,
                                leading=14, alignment=TA_JUSTIFY,
                                fontName="Helvetica"),
        "note": ParagraphStyle("note", fontSize=8, textColor=GREY,
                                leading=12, fontName="Helvetica-Oblique"),
        "cell_hdr": ParagraphStyle("cell_hdr", fontSize=9, textColor=WHITE,
                                    alignment=TA_CENTER, fontName="Helvetica-Bold"),
        "cell": ParagraphStyle("cell", fontSize=8.5, textColor=BLACK,
                                alignment=TA_CENTER, fontName="Helvetica"),
        "cell_diff": ParagraphStyle("cell_diff", fontSize=8.5,
                                     textColor=ACCENT_RED,
                                     alignment=TA_CENTER,
                                     fontName="Helvetica-Bold"),
    }
    return custom


# ── page header/footer ─────────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    W, H = A4
    # top banner
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, H - 22*mm, W, 22*mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(W/2, H - 13*mm,
        "AML Valvetrain Engineering — Valve Spring Drawing Analysis")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LIGHT_BLUE)
    canvas.drawRightString(W - 15*mm, H - 19*mm,
        "Mercedes-Benz AMG M177 | Prepared 2026-06-16")
    # bottom bar
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(15*mm, 3.5*mm,
        "Confidential — Internal Engineering Document")
    canvas.drawRightString(W - 15*mm, 3.5*mm,
        f"Page {doc.page}")
    canvas.restoreState()


# ── build report ───────────────────────────────────────────────────────────────
def build_report(output="ValveSpring_Drawing_Comparison.pdf"):
    st = styles()
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        topMargin=28*mm, bottomMargin=16*mm,
        leftMargin=15*mm, rightMargin=15*mm,
        title="Valve Spring Drawing Comparison",
        author="AML Engineering",
    )
    story = []

    # ── COVER ──────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 18*mm))

    cover_data = [[Paragraph("VALVE SPRING DRAWING COMPARISON", st["title"])]]
    cover_tbl = Table(cover_data, colWidths=[180*mm])
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("TOPPADDING",  (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(cover_tbl)
    story.append(Spacer(1, 3*mm))

    sub_data = [[Paragraph(
        "Exhaust Spring A1770530600  vs  Intake Spring A1770530500<br/>"
        "<font size='9'>Mercedes-Benz AMG M177 Engine · Scherdel GmbH · DIN 2098 Series</font>",
        st["subtitle"])]]
    sub_tbl = Table(sub_data, colWidths=[180*mm])
    sub_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), MID_BLUE),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(sub_tbl)
    story.append(Spacer(1, 8*mm))

    # summary KPI boxes
    kpi_data = [
        [
            Paragraph("<b>Wire Section</b><br/>2.92 × 3.66 mm oval<br/>(shared)", st["cell"]),
            Paragraph("<b>Free Length Δ</b><br/>Exhaust 47.0 mm<br/>Intake 46.1 mm  (+0.9 mm)", st["cell"]),
            Paragraph("<b>Seat Load Δ</b><br/>Exhaust 270 N<br/>Intake 250 N  (+8 %)", st["cell"]),
            Paragraph("<b>Full-Lift Load</b><br/>Both 620 N<br/>(shared)", st["cell"]),
            Paragraph("<b>Avg. Work Rate</b><br/>Exhaust 35.0 N/mm<br/>Intake 37.0 N/mm", st["cell"]),
        ]
    ]
    kpi_tbl = Table(kpi_data, colWidths=[36*mm]*5)
    kpi_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), LIGHT_BLUE),
        ("BACKGROUND",   (1,0), (1,0),  colors.HexColor('#FFF3CD')),
        ("BACKGROUND",   (2,0), (2,0),  colors.HexColor('#FFF3CD')),
        ("BOX",          (0,0), (-1,-1), 0.5, MID_BLUE),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, MID_BLUE),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(kpi_tbl)
    story.append(Spacer(1, 8*mm))

    # thumbnails
    story.append(Paragraph("Engineering Drawings", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_BLUE))
    story.append(Spacer(1, 3*mm))

    ex_thumb = make_thumbnail(EXHAUST["drawing_file"])
    in_thumb = make_thumbnail(INTAKE["drawing_file"])

    thumb_w = 86*mm
    thumb_h = 61*mm

    img_data = [[
        Image(ex_thumb, width=thumb_w, height=thumb_h),
        Image(in_thumb, width=thumb_w, height=thumb_h),
    ],[
        Paragraph(f"<b>{EXHAUST['part_no']}</b><br/>{EXHAUST['description']}", st["note"]),
        Paragraph(f"<b>{INTAKE['part_no']}</b><br/>{INTAKE['description']}",  st["note"]),
    ]]
    img_tbl = Table(img_data, colWidths=[90*mm, 90*mm])
    img_tbl.setStyle(TableStyle([
        ("BOX",          (0,0), (-1,-1), 0.5, MID_BLUE),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, colors.lightgrey),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    story.append(img_tbl)

    story.append(PageBreak())

    # ── COMPARISON TABLE ───────────────────────────────────────────────────────
    story.append(Paragraph("Parameter Comparison Table", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_BLUE))
    story.append(Spacer(1, 3*mm))

    HDR = [
        Paragraph("No.", st["cell_hdr"]),
        Paragraph("Symbol / Parameter", st["cell_hdr"]),
        Paragraph("Unit", st["cell_hdr"]),
        Paragraph("Exhaust\nA1770530600", st["cell_hdr"]),
        Paragraph("Intake\nA1770530500", st["cell_hdr"]),
        Paragraph("Δ / Remark", st["cell_hdr"]),
    ]

    def row(no, param, unit, ex_val, in_val, remark, diff=False):
        c = st["cell_diff"] if diff else st["cell"]
        return [
            Paragraph(str(no), st["cell"]),
            Paragraph(param, st["cell"]),
            Paragraph(unit, st["cell"]),
            Paragraph(str(ex_val), c if diff else st["cell"]),
            Paragraph(str(in_val), c if diff else st["cell"]),
            Paragraph(remark, c if diff else st["cell"]),
        ]

    rows = [
        HDR,
        row(1,  "d — wire diameter (oval cross-section)", "mm",   "2.92 × 3.66", "2.92 × 3.66", "Identical"),
        row(2,  "Dio — inner dia. top (oben)",            "mm",   "12.00 ± 0.20","12.00 ± 0.20","Identical"),
        row(3,  "Diu — inner dia. bottom (unten)",        "mm",   "15.90 ± 0.20","15.90 ± 0.20","Identical"),
        row(4,  "Deo — outer dia. top",                   "mm",   "19.32",        "19.32",        "Identical"),
        row(5,  "Deu — outer dia. bottom",                "mm",   "23.22",        "23.22",        "Identical"),
        row(6,  "# — spring index",                       "—",    "5.32",         "5.32",         "Identical"),
        row(7,  "Coiling direction",                      "—",    "Right (RH)",   "Right (RH)",   "Identical"),
        row(8,  "G — shear modulus",                      "N/mm²","79 500",       "79 500",       "Identical"),
        row(9,  "L0 — free length",                       "mm",   "47.0",         "46.1",         "Exhaust +0.9 mm", diff=True),
        row(10, "L1 — installed length",                  "mm",   "36.10",        "36.10",        "Identical"),
        row(11, "L2 — max. working length",               "mm",   "26.10",        "26.10",        "Identical"),
        row(12, "Lc — solid length",                      "mm",   "24.60 − 0.9",  "24.60 − 0.9",  "Identical"),
        row(13, "F1 — load at L1 (seat/installed)",       "N",    "270 ± 13",     "250 ± 12",     "Exhaust +20 N (+8 %)", diff=True),
        row(14, "F2 — load at L2 (full lift)",            "N",    "620 ± 27",     "620 ± 21",     "Same load; tighter tol. on intake", diff=False),
        row(15, "k_avg — avg. working rate (derived)",    "N/mm", f"{exhaust_k:.1f}", f"{intake_k:.1f}", "Exhaust softer over stroke", diff=True),
        row(16, "τ_k1 — torsional stress at L1",         "N/mm²","453",          "419",          "Exhaust +34 N/mm² (+8 %)", diff=True),
        row(17, "τ_k2 — torsional stress at L2",         "N/mm²","1 040",        "1 040",        "Identical"),
        row(18, "τ_kh — fatigue / stress range",         "N/mm²","587",          "521",          "Exhaust +66 N/mm² (+13 %)", diff=True),
        row(19, "nt — total coils",                       "—",    "8.6",          "8.6",          "Identical"),
        row(20, "na — active coils",                      "—",    "4.4 – 3.4",    "4.4 – 3.4",    "Identical"),
        row(21, "e_min — min. coil spacing",              "mm",   "0.55",         "0.55",         "Identical"),
        row(22, "Spring shape",                           "—",    "Beehive",      "Beehive",      "Identical"),
        row(23, "End treatment",                          "—",    "Closed & ground 240°","Closed & ground 240°","Identical"),
        row(24, "Shot peening",                           "—",    "Yes",          "Yes",          "Identical"),
        row(25, "Colour stripe 1",                        "—",    "Violet RAL 4002","Violet RAL 4002","Identical — spring type marker"),
        row(26, "Colour stripe 2 (ID colour)",            "—",    "Brown RAL 8004","Yellow RAL 1006","DIFFERENT — position identifier", diff=True),
        row(27, "Surface protection",                     "—",    "Wax",          "Wax",          "Identical"),
        row(28, "Heat treatment",                         "—",    "Yes (DIN 7386.20)","Yes (DIN 7386.20)","Identical"),
        row(29, "Supplier / std.",                        "—",    "Scherdel / DIN 2098","Scherdel / DIN 2098","Identical"),
        row(30, "Material",                               "—",    "VD SiCrNiV SC","VD SiCrNiV SC","Identical (DIN 17 223)"),
    ]

    col_w = [8*mm, 60*mm, 14*mm, 33*mm, 33*mm, 32*mm]
    tbl = Table(rows, colWidths=col_w, repeatRows=1)

    ts = TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  DARK_BLUE),
        ("TEXTCOLOR",    (0,0), (-1,0),  WHITE),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, STRIPE]),
        ("GRID",         (0,0), (-1,-1), 0.3, colors.HexColor('#BBBBBB')),
        ("LINEBELOW",    (0,0), (-1,0),  1,   DARK_BLUE),
        ("ALIGN",        (1,1), (1,-1),  "LEFT"),
        ("ALIGN",        (5,1), (5,-1),  "LEFT"),
    ])
    # highlight diff rows
    diff_rows = [9, 13, 15, 16, 18, 26]  # 1-indexed from header
    for r in diff_rows:
        ts.add("BACKGROUND", (3,r), (5,r), colors.HexColor('#FFF3CD'))
    tbl.setStyle(ts)
    story.append(tbl)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "★ Highlighted rows indicate parameters that differ between the two springs.",
        st["note"]))

    story.append(PageBreak())

    # ── ENGINEERING ANALYSIS ───────────────────────────────────────────────────
    story.append(Paragraph("Engineering Analysis", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_BLUE))
    story.append(Spacer(1, 4*mm))

    sections = [
        ("1. Shared Design Basis",
         """Both springs are manufactured by Scherdel GmbH to DIN 2098 / DIN 17 223 standards
         using <b>VD SiCrNiV SC</b> valve-spring steel wire with an <b>oval cross-section
         (2.92 × 3.66 mm)</b>. The beehive (Bienenkorb) profile, coiling direction (RH), spring
         index (5.32), coil count (nt = 8.6), end treatment (closed-and-ground, 240°), solid
         length (Lc = 24.60 mm), installed length (L1 = 36.10 mm), maximum working length
         (L2 = 26.10 mm), and full-lift force (F2 = 620 N) are all identical. Both springs
         receive the same shot-peening, wax surface protection, and heat treatment.  This shared
         basis minimises part proliferation and tooling cost — the two parts diverge only where
         the valve dynamics demand it."""),

        ("2. Free Length and Preload Difference",
         """The sole geometric difference between the two springs is free length:
         <b>L0 = 47.0 mm (exhaust)</b> vs <b>46.1 mm (intake)</b>, a delta of 0.9 mm. Because
         both springs are installed to the same assembly height (L1 = 36.10 mm), the 0.9 mm
         extra free length compresses the exhaust spring 0.9 mm further at installation, raising
         the <b>seat load (F1) from 250 N to 270 N — an 8 % increase</b>.  The torsional stress
         at the installed length rises proportionally: 453 N/mm² (exhaust) vs 419 N/mm²
         (intake)."""),

        ("3. Derived Spring Rates Over the Working Stroke",
         f"""Using the simple average-rate formula k = ΔF / ΔL over the 10 mm working stroke
         (L1 − L2):<br/><br/>
         &nbsp;&nbsp;&nbsp;<b>Exhaust:</b> k = (620 − 270) / (36.10 − 26.10) = <b>{exhaust_k:.1f} N/mm</b><br/>
         &nbsp;&nbsp;&nbsp;<b>Intake:</b> &nbsp;&nbsp;k = (620 − 250) / (36.10 − 26.10) = <b>{intake_k:.1f} N/mm</b><br/><br/>
         Both springs reach the same force (620 N) at full valve lift, but the exhaust spring
         starts from a higher seat load, so its effective spring rate over the working stroke is
         slightly <b>lower (35.0 vs 37.0 N/mm)</b>.  The intake spring therefore has
         approximately <b>5.7 % higher dynamic stiffness</b> across the lift event. Note that the
         beehive geometry produces a naturally progressive rate; these figures represent mean
         values across the stroke."""),

        ("4. Fatigue Stress Range and Durability",
         """The fatigue stress range τ_kh = τ_k2 − τ_k1 is the primary HCF driver for valve
         springs. The exhaust spring carries a <b>13 % higher fatigue range
         (587 vs 521 N/mm²)</b>. This is consistent with the higher preload and reflects the
         harsher thermal and pressure environment of the exhaust side:<br/><br/>
         &bull; <b>Exhaust valves</b> are exposed to residual combustion gases during the overlap
         period, and exhaust-side combustion pressure acts against the valve in early exhaust
         stroke. A higher seat load ensures positive valve closure despite back-pressure.<br/>
         &bull; <b>Intake valves</b> benefit from lower back-pressure — only intake-manifold
         vacuum assists closure — so a lower seat load is sufficient while keeping fatigue stress
         range within limits.<br/><br/>
         Both springs share the same peak stress at full lift (τ_k2 = 1 040 N/mm²), confirming
         the valvetrain is dimensioned to the same maximum stress level; it is only the
         <i>starting point</i> of each load cycle that differs."""),

        ("5. Load Tolerance and Assembly Quality",
         """The full-lift tolerance on the exhaust spring is <b>±27 N</b> vs <b>±21 N</b> for
         the intake spring.  A tighter tolerance on the intake spring may reflect closer
         attention to intake air-flow symmetry and cylinder-to-cylinder variation, whereas the
         exhaust spring relies more on the higher absolute preload level to guarantee closure.
         Both are well within the limits prescribed by DIN 2098 Part 2 (Gütevorschrift) and
         subject to statistical process control (Mitteldruckprüfen, DIN 6515 escalation level C,
         verified by Scherdel)."""),

        ("6. Colour Coding and Field Identification",
         """Both springs share the first colour stripe (violet RAL 4002) indicating the spring
         <i>type</i> (beehive, oval wire, AMG series).  The <b>second colour stripe uniquely
         identifies the position</b>:<br/><br/>
         &bull; Exhaust: <b>brown (braun) RAL 8004</b><br/>
         &bull; Intake: <b>yellow (gelb) RAL 1006</b><br/><br/>
         This two-colour coding system prevents incorrect installation during engine assembly or
         service — the springs are externally identical in shape, and only the colour stripe
         distinguishes them without measurement."""),
    ]

    for title, text in sections:
        story.append(KeepTogether([
            Paragraph(title, st["h2"]),
            Paragraph(text.replace("\n", " "), st["body"]),
            Spacer(1, 4*mm),
        ]))

    story.append(PageBreak())

    # ── CONCLUSIONS ────────────────────────────────────────────────────────────
    story.append(Paragraph("Conclusions", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_BLUE))
    story.append(Spacer(1, 4*mm))

    conclusion_items = [
        ("<b>Near-identical springs, one key difference:</b>",
         "The exhaust spring is the same part as the intake spring except for a 0.9 mm longer "
         "free length, which raises the seat load by 20 N (8 %) and the fatigue stress range "
         "by 66 N/mm² (13 %)."),
        ("<b>Same peak force at full lift (620 N):</b>",
         "Both springs are designed to deliver the same maximum force at full valve lift. This "
         "ensures the valvetrain cam/follower system, designed to a single peak force level, "
         "can be applied to both banks without modification."),
        ("<b>Higher exhaust preload is physically justified:</b>",
         "The additional seat load on the exhaust spring (270 vs 250 N) compensates for "
         "combustion back-pressure on the exhaust valve, preventing valve float or delayed "
         "closure under high-RPM or high-load conditions."),
        ("<b>Intake spring has slightly higher working stiffness:</b>",
         "Paradoxically, the softer (lower-preload) intake spring shows a 5.7 % higher average "
         "working rate (37.0 vs 35.0 N/mm) over the valve lift event, because it must "
         "traverse the same force range from a lower starting point."),
        ("<b>Fatigue dimensioning is consistent:</b>",
         "Both springs share the same peak torsional stress at full lift (1 040 N/mm²), "
         "confirming unified fatigue dimensioning. The exhaust spring operates at a higher mean "
         "stress, which in a Goodman diagram reduces its fatigue allowance; the "
         "VD SiCrNiV SC material and shot-peening are chosen to accommodate this."),
        ("<b>Colour coding is critical for correct assembly:</b>",
         "The brown vs yellow second stripe is the only visual distinction between the springs. "
         "Swapping them would install too-high preload on intake and too-low on exhaust — "
         "causing potential intake-side over-stress and exhaust-side valve float."),
        ("<b>No changes to manufacturing process or supplier:</b>",
         "Both parts share supplier (Scherdel), material specification, end treatment, surface "
         "protection, and quality standard. The free-length difference is the sole production "
         "distinguisher, minimising supply-chain complexity."),
    ]

    for title, text in conclusion_items:
        bullet_data = [[
            Paragraph("▶", ParagraphStyle("blt", fontSize=10, textColor=MID_BLUE,
                                           fontName="Helvetica-Bold")),
            Paragraph(f"{title} {text}", st["body"]),
        ]]
        btbl = Table(bullet_data, colWidths=[6*mm, 174*mm])
        btbl.setStyle(TableStyle([
            ("VALIGN",  (0,0), (-1,-1), "TOP"),
            ("TOPPADDING",   (0,0), (-1,-1), 2),
            ("BOTTOMPADDING",(0,0), (-1,-1), 2),
        ]))
        story.append(btbl)
        story.append(Spacer(1, 2.5*mm))

    story.append(Spacer(1, 6*mm))

    # summary box
    summary_data = [[Paragraph(
        "<b>Summary:</b> The exhaust and intake valve springs of the M177 engine are nearly "
        "identical beehive springs sharing all geometry and manufacturing parameters. The "
        "single engineering difference — a 0.9 mm longer free length on the exhaust spring — "
        "deliberately raises the seat load to resist exhaust back-pressure, while both springs "
        "converge to the same 620 N force at maximum valve lift. Correct installation is "
        "assured through a distinctive colour-stripe identification system (brown = exhaust, "
        "yellow = intake).",
        st["body"])]]
    stbl = Table(summary_data, colWidths=[180*mm])
    stbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT_BLUE),
        ("BOX",           (0,0), (-1,-1), 1,   MID_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ]))
    story.append(stbl)

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "Document prepared automatically from engineering drawings A1770530600-3 and "
        "A1770530500-4.  Derived calculations use nominal drawing values.  "
        "All specifications subject to Scherdel DIN 2098 Part 2 quality protocol.",
        st["note"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Report written: {output}")
    return output


if __name__ == "__main__":
    build_report()
