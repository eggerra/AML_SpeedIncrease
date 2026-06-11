#!/usr/bin/env python3
"""
Valvetrain Dynamic Viewer — vtRBint01 intake right bank
Tab 1: Cam/follower contact force (CDAT) — 5 kHz LP filtered, contact-loss map
Tab 2: HLA pump-up (HLIF) — lift + working pressure, cycle overlay
"""
import sys
import os
import numpy as np
from scipy.signal import butter, sosfiltfilt

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QButtonGroup, QFrame, QDoubleSpinBox,
    QCheckBox, QSizePolicy, QStatusBar, QTabWidget,
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Patch

# ── Config ─────────────────────────────────────────────────────────────────────
BASE = (
    r"D:\AW82001\5005\ref_Tamas"
    r"\AW82001_5004_20-Loop1-ModelStatus\Status20260608\excite_td"
)
RPM_VALUES  = [7000, 7100, 7200, 7300, 7400, 7500]
RPM_FOLDERS = {r: f"vtRBint01.Ref_C10.Pup_{r}rpm" for r in RPM_VALUES}

CDAT_ELEMENTS = [
    (1, "CDAT_6"),  (2, "CDAT_14"), (3, "CDAT_29"), (4, "CDAT_38"),
    (5, "CDAT_47"), (6, "CDAT_56"), (7, "CDAT_65"), (8, "CDAT_74"),
]
HLIF_ELEMENTS = [
    (1, "HLIF_11"), (2, "HLIF_19"), (3, "HLIF_34"), (4, "HLIF_43"),
    (5, "HLIF_52"), (6, "HLIF_61"), (7, "HLIF_70"), (8, "HLIF_79"),
]

CONTACT_THRESHOLD = 10.0     # N — cam/follower contact loss
PUMPUP_THRESHOLD  = 0.010    # mm — HLA lift above this on base circle = pump-up
DEFAULT_LP_HZ     = 5000.0

RPM_COLORS = {
    7000: "#1565c0",
    7100: "#2e7d32",
    7200: "#e65100",
    7300: "#ad1457",
    7400: "#6a1b9a",
    7500: "#b71c1c",
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def lp_filter(sig, fs, cutoff_hz):
    nyq = 0.5 * fs
    if cutoff_hz >= nyq:
        return sig.copy()
    sos = butter(4, cutoff_hz / nyq, btype="low", output="sos")
    return sosfiltfilt(sos, sig)


def _split_cycles(ca, *signals, n_cycles=10):
    """Split (ca, sig1, sig2, …) into n_cycles lists of (ca_mod, s1, s2, …)."""
    span = ca[-1] - ca[0]
    ppc  = int(round(len(ca) / (span / 720)))
    out  = []
    for i in range(n_cycles):
        s, e = i * ppc, min((i + 1) * ppc, len(ca))
        seg_ca = ca[s:e]
        ca_mod = (seg_ca - seg_ca[0]) % 720
        segs   = tuple(sig[s:e] for sig in signals)
        out.append((ca_mod,) + segs)
    return out


def _load_channels(path, *col_indices):
    from valvetrain_viewer import parse_gid
    arr = np.array(parse_gid(path)["data"], dtype=np.float64)
    t  = arr[:, 0]
    ca = arr[:, 2]
    fs = 1.0 / float(np.diff(t).mean())
    return (ca, fs) + tuple(arr[:, i] for i in col_indices)


# ── Background loader — loads CDAT + HLIF for all RPMs ────────────────────────
class DataLoader(QThread):
    finished = Signal(object)

    def run(self):
        data = {}
        for rpm in RPM_VALUES:
            res = os.path.join(BASE, RPM_FOLDERS[rpm], "results")
            # CDAT: col 7 = contact force [N]
            for vidx, prefix in CDAT_ELEMENTS:
                p = os.path.join(res, prefix + ".GID")
                if not os.path.isfile(p):
                    continue
                ca, fs, force = _load_channels(p, 7)
                data[("cdat", rpm, vidx)] = (ca, fs, force)
            # HLIF: col 4 = lift [m], col 13 = working pressure [Pa]
            for vidx, prefix in HLIF_ELEMENTS:
                p = os.path.join(res, prefix + ".GID")
                if not os.path.isfile(p):
                    continue
                ca, fs, lift_m, wp_pa = _load_channels(p, 4, 13)
                lift_mm = lift_m  * 1000.0   # → mm
                wp_bar  = wp_pa   / 1e5       # → bar
                data[("hlif", rpm, vidx)] = (ca, fs, lift_mm, wp_bar)
        self.finished.emit(data)


# ── Shared toolbar widget ──────────────────────────────────────────────────────
def _make_toggle(text, checked=False):
    b = QPushButton(text)
    b.setCheckable(True)
    b.setChecked(checked)
    b.setFont(QFont("Segoe UI", 8))
    b.setFixedHeight(26)
    b.setStyleSheet(
        "QPushButton{background:#e8edf2;border:1px solid #bcc5d0;"
        "border-radius:3px;padding:2px 10px;}"
        "QPushButton:checked{background:#1565c0;color:#fff;font-weight:bold;}"
        "QPushButton:hover{background:#d0daea;}"
    )
    return b


def _vline():
    f = QFrame(); f.setFrameShape(QFrame.Shape.VLine)
    f.setStyleSheet("color:#bbb"); return f


class RpmToolbar(QWidget):
    """RPM selector + mode + filter controls shared by both tabs."""
    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        lbl = QLabel("Mode:")
        lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        layout.addWidget(lbl)

        self.btn_single  = _make_toggle("Single RPM", True)
        self.btn_compare = _make_toggle("Compare all", False)
        self._mode_grp   = QButtonGroup(self)
        self._mode_grp.addButton(self.btn_single,  0)
        self._mode_grp.addButton(self.btn_compare, 1)
        self._mode_grp.setExclusive(True)
        layout.addWidget(self.btn_single)
        layout.addWidget(self.btn_compare)
        layout.addWidget(_vline())

        lbl2 = QLabel("RPM:")
        lbl2.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        layout.addWidget(lbl2)

        self._rpm_btns = {}
        self._rpm_grp  = QButtonGroup(self)
        self._rpm_grp.setExclusive(True)
        for i, rpm in enumerate(RPM_VALUES):
            b = _make_toggle(str(rpm), rpm == 7000)
            c = RPM_COLORS[rpm]
            b.setStyleSheet(
                f"QPushButton{{background:#f0f0f0;border:1px solid {c};"
                f"border-radius:3px;font-size:8pt;padding:3px 8px;}}"
                f"QPushButton:checked{{background:{c};color:#fff;font-weight:bold;}}"
            )
            self._rpm_grp.addButton(b, i)
            self._rpm_btns[rpm] = b
            layout.addWidget(b)
        layout.addWidget(_vline())

        self.chk_filter = QCheckBox("LP filter")
        self.chk_filter.setChecked(True)
        self.chk_filter.setFont(QFont("Segoe UI", 8))
        layout.addWidget(self.chk_filter)

        self.spin_lp = QDoubleSpinBox()
        self.spin_lp.setRange(100, 10000)
        self.spin_lp.setValue(DEFAULT_LP_HZ)
        self.spin_lp.setSingleStep(500)
        self.spin_lp.setSuffix(" Hz")
        self.spin_lp.setFixedWidth(100)
        self.spin_lp.setFont(QFont("Segoe UI", 8))
        layout.addWidget(self.spin_lp)

        layout.addStretch()

        self._mode_grp.idClicked.connect(self._on_mode)
        self._rpm_grp.idClicked.connect(lambda _: self.changed.emit())
        self.chk_filter.stateChanged.connect(lambda _: self.changed.emit())
        self.spin_lp.valueChanged.connect(lambda _: self.changed.emit())
        self._on_mode(0)

    def _on_mode(self, mid):
        single = (mid == 0)
        for b in self._rpm_btns.values():
            b.setEnabled(single)
        self.changed.emit()

    @property
    def mode(self):
        return "single" if self._mode_grp.checkedId() == 0 else "compare"

    @property
    def rpm(self):
        i = self._rpm_grp.checkedId()
        return RPM_VALUES[i] if i >= 0 else 7000

    @property
    def lp_hz(self):
        return self.spin_lp.value()

    @property
    def use_filter(self):
        return self.chk_filter.isChecked()


# ── Tab 1: Contact-loss canvas ─────────────────────────────────────────────────
class ContactCanvas(FigureCanvas):
    def __init__(self):
        self.fig, axes = plt.subplots(
            2, 4, figsize=(15, 6.5), sharex=True,
            gridspec_kw={"hspace": 0.50, "wspace": 0.20},
        )
        self.fig.patch.set_facecolor("#f5f5f5")
        self._axes = axes.flatten()
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data = {}

    def set_data(self, data):
        self._data = data

    def refresh(self, rpm, lp_hz, use_filter, mode):
        for ax in self._axes:
            ax.cla()
            ax.set_facecolor("#ffffff")
            ax.tick_params(labelsize=7)
            ax.set_xlim(0, 720)
            ax.set_xlabel("Crank angle [°]", fontsize=7)
            ax.set_ylabel("Force [N]", fontsize=7)
            ax.axhline(CONTACT_THRESHOLD, color="#e53935", lw=0.7,
                       ls="--", alpha=0.8)

        status = ""
        if mode == "single":
            status = self._plot_single(rpm, lp_hz, use_filter)
        else:
            status = self._plot_compare(lp_hz, use_filter)
        self.fig.canvas.draw_idle()
        return status

    def _plot_single(self, rpm, lp_hz, use_filter):
        color = RPM_COLORS[rpm]
        losses = []
        for ax, (vidx, _) in zip(self._axes, CDAT_ELEMENTS):
            key = ("cdat", rpm, vidx)
            if key not in self._data:
                ax.set_title(f"V{vidx} — no data", fontsize=8); continue
            ca, fs, force = self._data[key]
            sig = lp_filter(force, fs, lp_hz) if use_filter else force
            for ca_m, f_m in _split_cycles(ca, force):
                ax.plot(ca_m, f_m, color="#cccccc", lw=0.4, alpha=0.45)
            for ca_m, f_m in _split_cycles(ca, sig):
                ax.plot(ca_m, f_m, color=color, lw=0.6, alpha=0.22)
            ca_l, f_l = _split_cycles(ca, sig)[-1]
            ax.plot(ca_l, f_l, color=color, lw=1.6, zorder=3)
            mask = f_l <= CONTACT_THRESHOLD
            ax.fill_between(ca_l, 0, f_l, where=mask,
                            color="#ef5350", alpha=0.35, zorder=2)
            loss_deg = float(np.sum(np.diff(ca_l)[mask[:-1]])) if mask.any() else 0.0
            ax.set_ylim(-50, max(3200, f_l.max() * 1.1))
            if mask.any():
                losses.append(f"V{vidx}")
                ax.set_title(f"V{vidx}  ⚠ {loss_deg:.0f}°CA loss",
                             fontsize=7.5, fontweight="bold", color="#c62828")
            else:
                ax.set_title(f"V{vidx}  ✓ no loss",
                             fontsize=7.5, fontweight="bold", color="#2e7d32")
        n = len(losses)
        tag = f"contact loss on {n}/8 → " + ", ".join(losses) if n else "no contact loss"
        flt = f"LP {lp_hz:.0f} Hz" if use_filter else "unfiltered"
        return f"{flt}  |  threshold {CONTACT_THRESHOLD:.0f} N  |  {rpm} rpm: {tag}"

    def _plot_compare(self, lp_hz, use_filter):
        patches = [Patch(color=RPM_COLORS[r], label=f"{r}") for r in RPM_VALUES]
        for i, (ax, (vidx, _)) in enumerate(zip(self._axes, CDAT_ELEMENTS)):
            for rpm in RPM_VALUES:
                key = ("cdat", rpm, vidx)
                if key not in self._data: continue
                ca, fs, force = self._data[key]
                sig = lp_filter(force, fs, lp_hz) if use_filter else force
                ca_l, f_l = _split_cycles(ca, sig)[-1]
                c = RPM_COLORS[rpm]
                ax.plot(ca_l, f_l, color=c, lw=1.1, alpha=0.85)
                mask = f_l <= CONTACT_THRESHOLD
                if mask.any():
                    ax.fill_between(ca_l, 0, f_l, where=mask, color=c, alpha=0.15)
            ax.set_ylim(-50, 3200)
            ax.set_title(f"V{vidx}", fontsize=8, fontweight="bold")
            if i == 3:
                ax.legend(handles=patches, fontsize=6,
                          loc="upper right", framealpha=0.7, title="RPM")
        flt = f"LP {lp_hz:.0f} Hz" if use_filter else "unfiltered"
        return f"{flt}  |  Compare all RPMs  |  threshold {CONTACT_THRESHOLD:.0f} N"


# ── Tab 2: HLA pump-up canvas ──────────────────────────────────────────────────
class HLACanvas(FigureCanvas):
    def __init__(self):
        self.fig, axes = plt.subplots(
            2, 4, figsize=(15, 6.5), sharex=True,
            gridspec_kw={"hspace": 0.55, "wspace": 0.30},
        )
        self.fig.patch.set_facecolor("#f5f5f5")
        self._axes = axes.flatten()
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data  = {}
        self._ax2s  = []   # twin axes for pressure

    def set_data(self, data):
        self._data = data

    def refresh(self, rpm, lp_hz, use_filter, mode):
        # clear twin axes from last draw
        for ax2 in self._ax2s:
            ax2.remove()
        self._ax2s = []

        for ax in self._axes:
            ax.cla()
            ax.set_facecolor("#ffffff")
            ax.tick_params(labelsize=7)
            ax.set_xlim(0, 720)
            ax.set_xlabel("Crank angle [°]", fontsize=7)
            ax.set_ylabel("HLA lift [mm]", fontsize=7)

        status = ""
        if mode == "single":
            status = self._plot_single(rpm, lp_hz, use_filter)
        else:
            status = self._plot_compare(lp_hz, use_filter)
        self.fig.canvas.draw_idle()
        return status

    def _plot_single(self, rpm, lp_hz, use_filter):
        color   = RPM_COLORS[rpm]
        wp_col  = "#7b1fa2"    # purple for working pressure
        pumpups = []

        for ax, (vidx, _) in zip(self._axes, HLIF_ELEMENTS):
            key = ("hlif", rpm, vidx)
            if key not in self._data:
                ax.set_title(f"HLA{vidx} — no data", fontsize=8); continue
            ca, fs, lift_mm, wp_bar = self._data[key]

            sig_lift = lp_filter(lift_mm, fs, lp_hz) if use_filter else lift_mm
            sig_wp   = lp_filter(wp_bar,  fs, lp_hz) if use_filter else wp_bar

            # all raw lift cycles — gray
            for ca_m, lm in _split_cycles(ca, lift_mm):
                ax.plot(ca_m, lm, color="#cccccc", lw=0.4, alpha=0.45)

            # all filtered lift cycles — tinted
            for ca_m, lm in _split_cycles(ca, sig_lift):
                ax.plot(ca_m, lm, color=color, lw=0.5, alpha=0.22)

            # last filtered lift — bold
            ca_l, l_l = _split_cycles(ca, sig_lift)[-1]
            ax.plot(ca_l, l_l, color=color, lw=1.6, zorder=3, label="lift")

            # pump-up fill: lift > threshold
            mask_pu = l_l > PUMPUP_THRESHOLD
            if mask_pu.any():
                ax.fill_between(ca_l, PUMPUP_THRESHOLD, l_l, where=mask_pu,
                                color="#ef5350", alpha=0.40, zorder=2,
                                label=f"pump-up >{PUMPUP_THRESHOLD*1000:.0f} µm")

            # threshold line
            ax.axhline(PUMPUP_THRESHOLD, color="#e53935", lw=0.7,
                       ls="--", alpha=0.8)
            ax.axhline(0, color="#888", lw=0.5, ls=":")

            # working pressure on twin y-axis
            ax2 = ax.twinx()
            self._ax2s.append(ax2)
            ca_wp, wp_l = _split_cycles(ca, sig_wp)[-1]
            ax2.plot(ca_wp, wp_l, color=wp_col, lw=1.0, alpha=0.70,
                     ls="-", zorder=2, label="wp")
            ax2.set_ylabel("Pressure [bar]", fontsize=6, color=wp_col)
            ax2.tick_params(labelsize=6, colors=wp_col)
            ax2.set_ylim(0, max(350, wp_l.max() * 1.15))
            ax2.spines["right"].set_color(wp_col)

            # pump-up metric: max lift on base circle (wp < 10 bar)
            base_mask = sig_wp < 10.0
            pu_max = sig_lift[base_mask].max() * 1000 if base_mask.any() else 0.0
            ax.set_ylim(-0.08, 0.25)

            if pu_max > PUMPUP_THRESHOLD * 1000:
                pumpups.append(f"HLA{vidx}")
                ax.set_title(
                    f"HLA{vidx}  ⚠ pump-up {pu_max:.0f} µm",
                    fontsize=7.5, fontweight="bold", color="#c62828",
                )
            else:
                ax.set_title(
                    f"HLA{vidx}  ✓ {pu_max:.0f} µm",
                    fontsize=7.5, fontweight="bold", color="#2e7d32",
                )

        n = len(pumpups)
        flt = f"LP {lp_hz:.0f} Hz" if use_filter else "unfiltered"
        tag = (f"pump-up on {n}/8 → " + ", ".join(pumpups)) if n else "no pump-up"
        return (f"{flt}  |  threshold {PUMPUP_THRESHOLD*1000:.0f} µm  |  "
                f"{rpm} rpm: {tag}   [purple = working pressure]")

    def _plot_compare(self, lp_hz, use_filter):
        patches = [Patch(color=RPM_COLORS[r], label=f"{r}") for r in RPM_VALUES]
        for i, (ax, (vidx, _)) in enumerate(zip(self._axes, HLIF_ELEMENTS)):
            for rpm in RPM_VALUES:
                key = ("hlif", rpm, vidx)
                if key not in self._data: continue
                ca, fs, lift_mm, wp_bar = self._data[key]
                sig = lp_filter(lift_mm, fs, lp_hz) if use_filter else lift_mm
                ca_l, l_l = _split_cycles(ca, sig)[-1]
                c = RPM_COLORS[rpm]
                ax.plot(ca_l, l_l, color=c, lw=1.1, alpha=0.85)
                mask = l_l > PUMPUP_THRESHOLD
                if mask.any():
                    ax.fill_between(ca_l, PUMPUP_THRESHOLD, l_l, where=mask,
                                    color=c, alpha=0.18)
            ax.axhline(PUMPUP_THRESHOLD, color="#e53935", lw=0.7, ls="--", alpha=0.8)
            ax.axhline(0, color="#888", lw=0.5, ls=":")
            ax.set_ylim(-0.08, 0.25)
            ax.set_title(f"HLA{vidx}", fontsize=8, fontweight="bold")
            if i == 3:
                ax.legend(handles=patches, fontsize=6,
                          loc="upper right", framealpha=0.7, title="RPM")
        flt = f"LP {lp_hz:.0f} Hz" if use_filter else "unfiltered"
        return (f"{flt}  |  Compare all RPMs  |  threshold {PUMPUP_THRESHOLD*1000:.0f} µm  "
                f"(pump-up = base-circle lift > threshold)")


# ── Tab widget wrapper ─────────────────────────────────────────────────────────
class TabPage(QWidget):
    """Wraps a canvas + NavigationToolbar in a QWidget with a shared RpmToolbar."""
    def __init__(self, canvas, toolbar_ref):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 2)
        layout.setSpacing(3)
        layout.addWidget(canvas, stretch=1)
        nav = NavigationToolbar(canvas, self)
        nav.setMaximumHeight(28)
        layout.addWidget(nav)
        self.canvas = canvas
        self._tb = toolbar_ref

    def refresh(self):
        tb = self._tb
        return self.canvas.refresh(tb.rpm, tb.lp_hz, tb.use_filter, tb.mode)


# ── Main window ────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Valvetrain Dynamic Viewer — vtRBint01 intake RB  |  Ref_C10"
        )
        self.resize(1500, 900)
        self._data_ready = False
        self._build_ui()
        self._start_loader()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(6, 6, 6, 4)
        root.setSpacing(4)

        # shared toolbar
        self.toolbar = RpmToolbar()
        self.toolbar.changed.connect(self._refresh)
        root.addWidget(self.toolbar)

        # loading label (inside toolbar row — add after stretch)
        self.lbl_loading = QLabel("  Loading data…")
        self.lbl_loading.setStyleSheet("color:#e65100; font-weight:bold;")
        self.lbl_loading.setFont(QFont("Segoe UI", 8))
        self.toolbar.layout().addWidget(self.lbl_loading)

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self._contact_canvas = ContactCanvas()
        self._hla_canvas     = HLACanvas()

        self._tab_contact = TabPage(self._contact_canvas, self.toolbar)
        self._tab_hla     = TabPage(self._hla_canvas,     self.toolbar)

        self.tabs.addTab(self._tab_contact, "Contact Loss (CDAT)")
        self.tabs.addTab(self._tab_hla,     "HLA Pump-Up (HLIF)")
        self.tabs.currentChanged.connect(self._refresh)

        root.addWidget(self.tabs, stretch=1)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Loading CDAT + HLIF data for all 6 RPM points…")

    def _start_loader(self):
        self._loader = DataLoader()
        self._loader.finished.connect(self._on_loaded)
        self._loader.start()

    def _on_loaded(self, data):
        self._data_ready = True
        self._contact_canvas.set_data(data)
        self._hla_canvas.set_data(data)
        self.lbl_loading.hide()
        self._refresh()

    def _refresh(self):
        if not self._data_ready:
            return
        idx = self.tabs.currentIndex()
        if idx == 0:
            msg = self._tab_contact.refresh()
        else:
            msg = self._tab_hla.refresh()
        self.status.showMessage(msg)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
