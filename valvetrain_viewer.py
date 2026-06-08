"""
Valvetrain Result Viewer — AVL Excite Timing Drive
Drag result tiles from the left panel onto the plot canvas.
"""
import sys, os, re, json, itertools
import numpy as np

from PySide6.QtCore import Qt, QMimeData, QByteArray, QThread, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea, QLabel, QFrame, QComboBox, QPushButton, QSplitter,
    QSizePolicy, QProgressBar,
)
from PySide6.QtGui import QDrag, QFont, QCursor, QColor, QPalette

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('QtAgg')

# ── Config ────────────────────────────────────────────────────────────────────
BASE = r"D:\AW82001\5005\ref_Tamas\AW82001_5004_20-Loop1-ModelStatus\Status20260608\excite_td"
MODEL = "vtRBint01.Ref_C10"
RPM_LABELS = ["7000rpm", "7100rpm", "7200rpm", "7300rpm", "7400rpm", "7500rpm"]
RPM_FOLDERS = [f"{MODEL}.{r}" for r in RPM_LABELS]

COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
]

# Per-RPM tile colours: (background, border)
RPM_TILE_COLORS = {
    7000: ("#E3F2FD", "#1565C0"),
    7100: ("#E8F5E9", "#2E7D32"),
    7200: ("#FFF3E0", "#E65100"),
    7300: ("#F3E5F5", "#6A1B9A"),
    7400: ("#FFEBEE", "#B71C1C"),
    7500: ("#E0F7FA", "#006064"),
}

# category → (file_prefixes, channel_whitelist)
# "plot_axis" keys control which subplot receives the curve:
#   "top"  → Valve Lift subplot
#   "bot"  → Contact Pressure subplot
CATEGORIES = [
    ("Valve Lift",           ["VAFA_"],  ["lift"]),
    ("Valve Seat Force",     ["VAFA_"],  ["seat force"]),
    ("Contact Pressure",     ["CLUB_"],  ["contact stress"]),
    ("Contact Force",        ["CDAT_"],  ["force"]),
    ("Spring Force",         ["CTOR_"],  ["force"]),
    ("Spring Coil Contact",  ["SPPR_"],  ["force coil contact"]),
    ("Lash Adjuster",        ["HLIF_"],  ["lift", "force", "working pressure"]),
    ("Finger Follower",      ["FIFO_"],  ["lift", "force"]),
]

# Which subplot each category goes to
_CAT_AXIS = {
    "Valve Lift":          "top",
    "Valve Seat Force":    "top",
    "Contact Pressure":    "bot",
    "Contact Force":       "bot",
}

_SKIP_CH = {"time", "equiv. cam angle", "equiv. crank angle", "ref. angle"}


# ── GID parser ────────────────────────────────────────────────────────────────
def _split_list(header, keyword):
    m = re.search(keyword + r"\s*=\s*\[(.*?)\]", header, re.DOTALL)
    if not m:
        return []
    raw = re.sub(r"[\r\n\t&]", " ", m.group(1))
    return [v.strip().strip("'") for v in re.split(r",\s*", raw) if v.strip().strip("'")]


def parse_gid(filepath, header_only=False):
    try:
        with open(filepath, "rb") as f:
            raw = f.read() if not header_only else f.read(8192)
        text = raw.decode("latin-1")
    except Exception:
        return None

    end_pos = text.find("END\r\n")
    if end_pos < 0:
        end_pos = text.find("END\n")
    if end_pos < 0:
        return None

    header = text[:end_pos]
    m = re.search(r"objectname\s*=\s*'([^']+)'", header)
    objectname = m.group(1) if m else ""
    m = re.search(r"speed\s*=\s*'([^']+)'", header)
    speed = float(m.group(1).strip()) if m else 0.0

    channels = _split_list(header, "CHANNEL")
    units    = _split_list(header, "UNIT")

    result = {"objectname": objectname, "speed": speed,
              "channels": channels, "units": units}

    if not header_only:
        skip = 5 if text[end_pos:end_pos+5] == "END\r\n" else 4
        data_text = text[end_pos + skip:]
        vals = np.fromstring(data_text, sep=" ")
        n = len(channels)
        if n and len(vals) % n == 0:
            result["data"] = vals.reshape(-1, n)
        else:
            result["data"] = None

    return result


# ── Catalog builder ───────────────────────────────────────────────────────────
def build_catalog(rpm_folder_path):
    results_dir = os.path.join(rpm_folder_path, "results")
    if not os.path.isdir(results_dir):
        return {}

    all_gid = {f: os.path.join(results_dir, f)
               for f in os.listdir(results_dir) if f.endswith(".GID")}

    catalog = {}
    _sep = chr(92)   # backslash separator in GID objectname
    sppr_per_spring = {}
    ctor_per_spring = {}

    for cat_name, prefixes, ch_filter in CATEGORIES:
        matched = sorted(f for f in all_gid if any(f.startswith(p) for p in prefixes))
        tiles = []

        for fname in matched:
            fpath = all_gid[fname]
            info = parse_gid(fpath, header_only=True)
            if not info:
                continue

            obj = info["objectname"]
            spring = obj.split(_sep)[0] if _sep in obj else obj

            # SPPR: only one end_coil_valve file per spring
            if fname.startswith("SPPR_"):
                if "end_coil_valve" not in obj:
                    continue
                if sppr_per_spring.get(spring, 0) >= 1:
                    continue
                sppr_per_spring[spring] = 1

            # CTOR: only end_coil_head _spring elements, 1 per spring
            if fname.startswith("CTOR_"):
                if "end_coil_head" not in obj or "_spring" not in obj:
                    continue
                if ctor_per_spring.get(spring, 0) >= 1:
                    continue
                ctor_per_spring[spring] = 1

            channels = info.get("channels", [])
            units_list = info.get("units", [])

            # Build short label: "SPGx · end_coil_type" or plain tail
            if _sep in obj:
                spring_short = spring.replace("INTr_", "")
                coil_raw = obj.split(_sep)[-1]
                coil_simple = "_".join(coil_raw.split("_")[:3]) if coil_raw.startswith("end_") else coil_raw
                short = f"{spring_short} · {coil_simple}"
            else:
                short = obj

            for i, ch in enumerate(channels):
                if ch in _SKIP_CH:
                    continue
                if ch_filter and ch not in ch_filter:
                    continue
                unit = units_list[i] if i < len(units_list) else ""
                tiles.append({
                    "filepath":    fpath,
                    "objectname":  obj,
                    "short_name":  short,
                    "channel":     ch,
                    "channel_idx": i,
                    "unit":        unit,
                    "category":    cat_name,
                    "plot_axis":   _CAT_AXIS.get(cat_name, "top"),
                })

        if tiles:
            catalog[cat_name] = tiles

    return catalog


# ── All-RPM catalog loader thread ─────────────────────────────────────────────
# Loads all 6 RPM result directories in one background pass and returns a
# merged catalog:  {cat_name: [tiles…]}  where every tile carries rpm info.
class AllRpmLoader(QThread):
    done = Signal(dict)

    def run(self):
        merged = {}
        for idx, (lbl, folder) in enumerate(zip(RPM_LABELS, RPM_FOLDERS)):
            rpm = int(lbl.replace("rpm", ""))
            cat = build_catalog(os.path.join(BASE, folder))
            for cat_name, tiles in cat.items():
                for t in tiles:
                    t["rpm"]       = rpm
                    t["rpm_label"] = lbl
                    t["rpm_idx"]   = idx
                merged.setdefault(cat_name, []).extend(tiles)
        self.done.emit(merged)


# ── Draggable tile ────────────────────────────────────────────────────────────
class TileWidget(QFrame):
    def __init__(self, tile_info: dict, parent=None):
        super().__init__(parent)
        self.tile_info = tile_info
        self._drag_start = None

        self.setFixedHeight(46)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolTip(tile_info["objectname"])

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 3)
        layout.setSpacing(1)

        top = QLabel(f"{tile_info['short_name']}  ·  {tile_info['channel']} [{tile_info['unit']}]")
        top.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        rpm  = tile_info.get("rpm", 7000)
        lbl  = tile_info.get("rpm_label", "")
        bg, border = RPM_TILE_COLORS.get(rpm, ("#f0f4f8", "#c8d0da"))

        rpm_tag = QLabel(f"● {lbl}")
        rpm_tag.setFont(QFont("Segoe UI", 7))
        rpm_tag.setStyleSheet(f"color:{border}; border:none; background:transparent;")

        layout.addWidget(top)
        layout.addWidget(rpm_tag)

        self.setStyleSheet(f"""
            TileWidget {{
                background:{bg}; border:1.5px solid {border};
                border-radius:4px; margin:1px 2px;
            }}
            TileWidget:hover {{ background:{bg}; border:2px solid {border}; }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton) or self._drag_start is None:
            return
        if (event.position().toPoint() - self._drag_start).manhattanLength() \
                < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime = QMimeData()
        mime.setData("application/x-tile",
                     QByteArray(json.dumps(self.tile_info).encode("utf-8")))
        drag.setPixmap(self.grab())
        drag.setHotSpot(self._drag_start)
        drag.setMimeData(mime)
        drag.exec(Qt.DropAction.CopyAction)


# ── Left panel ────────────────────────────────────────────────────────────────
FOCUS_CATEGORIES = ["Valve Lift", "Contact Pressure"]

# Sub-header colours for category labels inside each RPM group
CAT_HEADER_COLORS = {
    "Valve Lift":       ("#1565C0", "#E3F2FD"),   # (text, bg)
    "Contact Pressure": ("#B71C1C", "#FFEBEE"),
}


class TilePanel(QWidget):
    """
    Shows tiles for ALL six RPM points simultaneously.
    Structure: Speed header → Category sub-header → component tiles.
    Only Valve Lift and Contact Pressure are shown.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(3)
        self.progress.setRange(0, 0)
        layout.addWidget(self.progress)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.inner = QWidget()
        self.inner_layout = QVBoxLayout(self.inner)
        self.inner_layout.setContentsMargins(0, 0, 4, 0)
        self.inner_layout.setSpacing(0)
        self.inner_layout.addStretch()
        self.scroll.setWidget(self.inner)
        layout.addWidget(self.scroll)

        self._loader = AllRpmLoader()
        self._loader.done.connect(self._on_catalog)
        self._loader.start()

    def _on_catalog(self, catalog):
        self.progress.hide()

        # Build lookup: {rpm: {cat_name: [tiles]}}
        by_speed = {}
        for cat_name in FOCUS_CATEGORIES:
            for t in catalog.get(cat_name, []):
                by_speed.setdefault(t["rpm"], {}).setdefault(cat_name, []).append(t)

        pos = 0
        for rpm in sorted(by_speed):
            bg, border = RPM_TILE_COLORS.get(rpm, ("#f0f4f8", "#c8d0da"))

            # Speed top-level header
            spd_hdr = QLabel(f"  {rpm} rpm")
            spd_hdr.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            spd_hdr.setFixedHeight(26)
            spd_hdr.setStyleSheet(
                f"color:#fff; background:{border}; padding:2px 6px;"
                "margin-top:8px; border-radius:3px;"
            )
            self.inner_layout.insertWidget(pos, spd_hdr); pos += 1

            for cat_name in FOCUS_CATEGORIES:
                tiles = by_speed[rpm].get(cat_name, [])
                if not tiles:
                    continue
                tc, tbg = CAT_HEADER_COLORS.get(cat_name, ("#333", "#eee"))
                cat_hdr = QLabel(f"   {cat_name}")
                cat_hdr.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
                cat_hdr.setFixedHeight(18)
                cat_hdr.setStyleSheet(
                    f"color:{tc}; background:{tbg}; padding-left:8px;"
                    "margin-top:2px;"
                )
                self.inner_layout.insertWidget(pos, cat_hdr); pos += 1
                for t in tiles:
                    self.inner_layout.insertWidget(pos, TileWidget(t)); pos += 1


# ── Plot canvas ───────────────────────────────────────────────────────────────
# Valve Lift  →  top subplot (ax_top)
# Contact Pressure / Force  →  bottom subplot (ax_bot)
# All other categories default to top unless no top curves exist.

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = plt.figure(figsize=(11, 7))
        self.fig.patch.set_facecolor("#fafafa")
        self.ax_top = self.fig.add_subplot(211)
        self.ax_bot = self.fig.add_subplot(212, sharex=self.ax_top)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setAcceptDrops(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._curves = []           # (line_obj, ax)
        self._color_top = itertools.cycle(COLORS)
        self._color_bot = itertools.cycle(COLORS[5:] + COLORS[:5])

        self._init_axes()

    def _init_axes(self):
        for ax in (self.ax_top, self.ax_bot):
            ax.set_facecolor("#fafafa")
            ax.grid(True, alpha=0.25, linewidth=0.6)
            ax.tick_params(labelsize=8)

        self.ax_top.set_ylabel("Valve Lift  [mm]", fontsize=9)
        self.ax_top.set_title("Valvetrain Dynamics  —  drag tiles onto this canvas",
                               fontsize=9, pad=4)
        self.ax_bot.set_ylabel("Contact Pressure  [MPa]", fontsize=9)
        self.ax_bot.set_xlabel("Crank Angle  [°]", fontsize=9)

        self.ax_top.set_xlim(0, 720)
        self.ax_bot.set_xlim(0, 720)
        for ax in (self.ax_top, self.ax_bot):
            ax.set_xticks(range(0, 721, 90))

        self.fig.tight_layout(pad=1.8, h_pad=1.2)

    # ── drag-and-drop ─────────────────────────────────────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-tile"):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-tile"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        raw = bytes(event.mimeData().data("application/x-tile")).decode("utf-8")
        tile = json.loads(raw)
        self._add_curve(tile)
        event.acceptProposedAction()

    # ── data loading ──────────────────────────────────────────────────────────
    def _add_curve(self, tile):
        gid = parse_gid(tile["filepath"])
        if gid is None or gid.get("data") is None:
            return

        data     = gid["data"]
        channels = gid["channels"]

        try:
            xi = channels.index("equiv. crank angle")
        except ValueError:
            xi = 0

        x_raw = data[:, xi]
        y_raw = data[:, tile["channel_idx"]]

        # Fold last complete 720° cycle to [0, 720)
        x_end   = x_raw[-1]
        mask    = x_raw >= (x_end - 720.0)
        x_cyc   = x_raw[mask] % 720.0
        y_cyc   = y_raw[mask]
        order   = np.argsort(x_cyc)
        x = x_cyc[order]
        y = y_cyc[order]

        # Unit conversion
        unit = tile["unit"]
        if unit == "m":
            y = y * 1000.0;  unit = "mm"
        elif unit in ("N/m^2", "Pa"):
            y = y / 1e6;     unit = "MPa"

        label = f"{tile['short_name']} · {tile['channel']} [{unit}]"
        axis  = tile.get("plot_axis", "top")
        ax    = self.ax_bot if axis == "bot" else self.ax_top
        color = next(self._color_bot if axis == "bot" else self._color_top)

        (line,) = ax.plot(x, y, label=label, color=color, linewidth=1.3)
        self._curves.append((line, ax))
        self._refresh()

    def _refresh(self):
        for ax in (self.ax_top, self.ax_bot):
            lines = ax.get_lines()
            if lines:
                ax.legend(loc="upper right", fontsize=7,
                          framealpha=0.85, edgecolor="#aaa")
        self.fig.tight_layout(pad=1.8, h_pad=1.2)
        self.draw()

    # ── controls ──────────────────────────────────────────────────────────────
    def clear_plot(self):
        self.ax_top.cla()
        self.ax_bot.cla()
        self._curves.clear()
        self._color_top = itertools.cycle(COLORS)
        self._color_bot = itertools.cycle(COLORS[5:] + COLORS[:5])
        self._init_axes()
        self.draw()

    def remove_last(self):
        if not self._curves:
            return
        line, ax = self._curves.pop()
        line.remove()
        self._refresh()


# ── Main window ───────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Valvetrain Result Viewer — AVL Excite Timing Drive  |  vtRBint01.Ref_C10")
        self.resize(1500, 860)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ── Left ──────────────────────────────────────────────────────────────
        left = QWidget()
        left.setMinimumWidth(255)
        left.setMaximumWidth(360)
        lv = QVBoxLayout(left)
        lv.setContentsMargins(6, 6, 6, 6)
        lv.setSpacing(4)

        title = QLabel("Result Channels")
        title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title.setStyleSheet("color:#1a2e50;")
        lv.addWidget(title)

        hint = QLabel("Drag a tile → drop on the plot")
        hint.setFont(QFont("Segoe UI", 7))
        hint.setStyleSheet("color:#888; margin-bottom:4px;")
        lv.addWidget(hint)

        self.tile_panel = TilePanel()
        lv.addWidget(self.tile_panel)
        splitter.addWidget(left)

        # ── Right ─────────────────────────────────────────────────────────────
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(6, 6, 6, 6)
        rv.setSpacing(4)

        # Button bar
        btn_row = QHBoxLayout()
        for lbl, slot_name in [("Clear all", "clear_plot"), ("Remove last", "remove_last")]:
            btn = QPushButton(lbl)
            btn.setFixedHeight(26)
            btn.setFixedWidth(100)
            btn.setStyleSheet(
                "QPushButton{background:#e8edf2;border:1px solid #bcc5d0;"
                "border-radius:3px;font-size:8pt;}"
                "QPushButton:hover{background:#d0daea;}"
            )
            btn.clicked.connect(getattr(self, f"_{slot_name}"))
            btn_row.addWidget(btn)
        btn_row.addStretch()

        drop_hint = QLabel("← drop tiles here")
        drop_hint.setFont(QFont("Segoe UI", 8))
        drop_hint.setStyleSheet("color:#aaa;")
        btn_row.addWidget(drop_hint)
        rv.addLayout(btn_row)

        self.canvas = PlotCanvas()
        self.nav = NavigationToolbar(self.canvas, right)
        rv.addWidget(self.nav)
        rv.addWidget(self.canvas)

        splitter.addWidget(right)
        splitter.setSizes([300, 1200])
        root.addWidget(splitter)

    def _clear_plot(self):
        self.canvas.clear_plot()

    def _remove_last(self):
        self.canvas.remove_last()


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Light palette
    pal = app.palette()
    pal.setColor(QPalette.ColorRole.Window, QColor("#f5f7fa"))
    pal.setColor(QPalette.ColorRole.WindowText, QColor("#1a1a1a"))
    app.setPalette(pal)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
