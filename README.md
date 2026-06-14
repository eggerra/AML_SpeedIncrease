# Valve Spring FEA — A177 053 05 00 (AML Intake, Beehive)

Engineering analysis of the Scherdel beehive valve spring using open-source tools:
parametric CAD (pythonOCC / FreeCAD), Netgen meshing, and CalculiX FEA.

---

## Valvetrain Result Viewer (`valvetrain_viewer.py`)

Interactive GUI for AVL Excite Timing Drive results (model `vtRBint01.Ref_C10`,
6 RPM points 7000–7500 rpm).

### Running

```bash
python valvetrain_viewer.py
```

Requires: PySide6, matplotlib, numpy, scipy.

### Usage

Drag any tile from the left panel onto the plot canvas to add a curve.
Valve Lift channels appear in the top subplot; Contact Pressure (cam stress)
channels appear in the bottom subplot.

| Interaction | Action |
|---|---|
| Left-drag on plot | Pan |
| Scroll wheel | Zoom centred on cursor |
| Right double-click | Reset to initial view |
| Toolbar | Home / back / forward, additional pan/zoom modes |

### LP filter

The slider in the toolbar applies a 4th-order zero-phase Butterworth low-pass
filter to all Contact Pressure curves in real time.
Range: **3–8 kHz** (8 kHz = OFF). The cutoff is converted to physical frequency
using each curve's RPM and crank-angle sample spacing.

### Contact-loss detection

For every Contact Pressure curve the main cam event is identified automatically
(region where raw stress > 5 % of peak). The minimum filtered stress in that
window is evaluated and a severity label is drawn on the bottom subplot:

| Label | Condition | Meaning |
|---|---|---|
| ✓ green | min ≥ 0 MPa | No contact loss |
| ⚠ amber | 0 > min > −5 % of peak | Mild / brief contact loss |
| ✗ red | min ≤ −5 % of peak | Severe contact loss |

Labels update live when the LP filter slider is moved.

---

## Drawing specification

| Symbol | Parameter | Value | Unit |
|--------|-----------|-------|------|
| d | Wire (axial × radial) | 2.92 × 3.66 | mm |
| Dio / Diu | Inner Ø top / bottom | 12.00 / 15.90 | mm |
| Deo / Deu | Outer Ø top / bottom | 19.32 / 23.22 | mm |
| L0 | Free length | 46.1 | mm |
| L1 | Installed length | 31.6 | mm |
| F1 | Spring force @ L1 | 250 ± 12 | N |
| F2 | Spring force @ L2 | 620 ± 27 | N |
| nt | Total coils | 8.6 | — |
| G | Shear modulus | 79 500 | N/mm² |
| Material | VD SiCrNi SC | DIN 17 223 | — |

---

## Spring rate — progressive behaviour

The spring is a **beehive (Bienenkorb)** design with oval wire and **variable pitch**.
Large-Ø coils at the bottom have tighter pitch and bind first as the spring compresses,
progressively stiffening the characteristic.

### Measurement calibration (INT_Spring_measurement.txt — 398 data points)

Piecewise linear regression on the measured force–lift curve:

| Phase | Valve-lift range | Rate k (N/mm) | Notes |
|-------|-----------------|---------------|-------|
| 1 | 0 → 4.05 mm | 34.70 | Pre-binding — active coils contributing |
| 2 | 4.05 → 7.67 mm | 36.53 | Large-OD bottom coils binding |
| 3 | 7.67 → 10.0 mm | 40.90 | Mid/upper coil zone binding |

Kink positions (from phase-line departure, **compression measured from drawing L0=46.1 mm**):

| Event | Valve lift | Compression from L0 | Force (meas) |
|-------|-----------|---------------------|-------------|
| Kink 1 (first binding) | 4.05 mm | 18.55 mm | 390.7 N |
| Kink 2 (upper zone)   | 7.67 mm | 22.17 mm | 525.3 N |
| Full lift | 10.00 mm | 24.50 mm | 620.7 N |

### Geometry (2026-06-14) — drawing values

Both L0=46.1 mm and n\_closed=1.25 are drawing values.

| Parameter | Drawing | **Model (2026-06-14)** | Notes |
|-----------|---------|------------------------|-------|
| L0 | 46.1 mm | **46.1 mm** | Drawing value ✓ |
| n\_closed | 1.25 | **1.25** | Drawing value ✓ |
| n\_active | 6.1 | **6.1** | nt − 2×n\_closed ✓ |
| h\_active | — | **38.8 mm** | L0 − 2×n\_closed×wire\_a |
| pitch\_mean | — | **6.361 mm** | h\_active / n\_active |
| D\_pitch | — | **0.0629** | Places kink1 at s\_bind=18.55 mm |
| p\_bot | — | **5.962 mm (gap 3.042)** | — |
| p\_top | — | **6.760 mm** | — |

Wire cross-section and coil diameters are unchanged from the drawing.

**Analytical model check:**

| Quantity | Analytical | Measurement | Error |
|----------|-----------|-------------|-------|
| F @ preload (s=14.5 mm) | 249 N | 249 N | 0.0% |
| F @ kink1 (lift=4.05 mm) | 389.5 N | 390.7 N | 0.3% |
| F @ kink2 (lift=7.67 mm) | 521.8 N | 525.3 N | 0.7% |
| F @ full lift (lift=10 mm) | 617.1 N | 620.7 N | 0.6% |

---

## FEA setup

| Item | Detail |
|------|--------|
| Elements | C3D10 (10-node quadratic tetrahedra, straight mid-side nodes) |
| Nodes / elements | 382 100 / 235 495 (Abaqus pipeline, LMAX=1.0); 251 318 / 150 560 (legacy CalculiX, LMAX=1.5) |
| Material | E = 273 131 MPa (×1.326 mesh correction, nominal 206 000), ν = 0.30 |
| BCs — Step 1 | Bottom face fixed; top face compressed 0→14.965 mm (preload, L0\_oval=46.565 mm) |
| BCs — Step 2 | Top face compressed further to 24.965 mm total (10 mm valve lift) |
| Increment size | 0.5 mm initial, min 0.001 mm (Abaqus auto-cutback) |
| Analysis | NLGEOM static (large-displacement) |
| Self-contact | SURFACE TO SURFACE, EXPONENTIAL c0=0.1 mm p0=0.1 MPa; `*CONTACT CONTROLS, STABILIZE=0.001` per step |
| Solver | Abaqus/Standard 2025 HF3 (16 threads); legacy: CalculiX 2.22 (SPOOLES) |
| Mesher | Netgen (netgen-mesher via FreeCAD 1.1 Python), LMAX=1.0 mm |

### Meshing notes

The beehive helix geometry creates meshing challenges in two zones:

- **Bottom closed-coil zone (z < 5 mm):** 30:1 aspect-ratio inter-coil strip at R=9.78 mm.
  Any sub-0.5 mm element size triggers `SYSTEM ERROR: more elements on face` in Netgen,
  producing invalid volume elements. Global maxh=0.50 mm is the stable limit for this zone.
- **Active coil zone (z = 5–41.5 mm):** Refinement to 0.30 mm via `RestrictH` along the helix
  centreline was attempted but caused the same face-error cascade. Retained at global 0.50 mm (~6
  elements across 2.92 mm wire axial dimension).
- **Degenerate element removal:** 4 near-zero-volume elements are dropped at mesh write time
  (|det J| < 1e-3 at corner nodes). These are outside the contact zone.
- **Mid-side node straightening:** Netgen places mid-side nodes on the curved OCC surface.
  For degenerate elements this produces negative Jacobians at CalculiX integration points.
  All mid-side nodes are moved to arithmetic edge midpoints before writing the mesh.

---

## FEA result — spring_FvL.png

![Force vs Lift](spring_FvL.png)

### Abaqus/Standard results (finer mesh, LMAX=1.0 — re-run 2026-06-14)

**Change applied 2026-06-15:** L0 restored to drawing value 46.1 mm (was calibrated 38.717 mm).
L0\_oval updated to 46.565 mm. D\_pitch recalculated to 0.0629 (kink1 preserved at lift=4.05 mm).
Contact c0 reverted 0.01→0.1 mm (c0=0.01 caused force blowup at s~14 mm).
Mesher switched from Gmsh (0 vol elems failure) to Netgen maxh=1.0 mm. 16 threads.

Mesh: regenerated from new geometry (drawing L0=46.1 mm).

**Estimated performance with drawing geometry:**

| Quantity | Analytical (3-phase) | **FEA estimate** | Measurement |
|----------|---------------------|------------------|-------------|
| F @ preload (s=14.965 mm) | 249 N | ~249 N | 249 N |
| F @ kink1 (lift=4.05 mm) | 390 N | ~390 N | 390.7 N |
| F @ full lift (s=24.965 mm) | 621 N | ~621 N | 620.7 N |

_Results pending from current simulation run._

**Previous run (2026-06-12, wrong n\_closed=2.026):**

| Quantity | Analytical | Abaqus FEA (wrong) | Measurement |
|----------|-----------|---------------------|-------------|
| F @ preload (s=7.9 mm) | 249 N | 337 N (+35%) | 249 N |
| F @ full lift (s=17.9 mm) | 621 N | >3400 N (coil bind) | 621 N |

### CalculiX results (coarser mesh, LMAX=1.5 — 2026-06-11, reference)

Mesh: 251 318 nodes / 150 560 C3D10 elements.  
**E-correction**: ×1.326 (206 000 → 273 131 MPa) calibrated to match F @ preload.

| Quantity | Analytical (3-phase) | **FEA** | Measurement | FEA error |
|----------|---------------------|---------|-------------|-----------|
| F @ preload  (s=7.9 mm) | 249 N | **278 N** | 249 N | +11% |
| F @ full lift (s=17.9 mm) | 621 N | **686 N** | 621 N | +10% |

FEA output at every 5th increment (FREQUENCY=5). 3-phase progressive stiffening (green curve)
calibrated from measurement matches within 0.6% at full lift.

---

## Running the pipeline

### CalculiX pipeline (legacy)

```bash
# 1. Generate CAD (FreeCAD's Python — needs pythonOCC)
"C:/Users/.../FreeCAD 1.1/bin/python.exe" generate_spring.py

# 2. Mesh (FreeCAD's Python — needs netgen-mesher)
"C:/Users/.../FreeCAD 1.1/bin/python.exe" mesh_netgen.py

# 3. FEA + plot
python spring_analysis.py
```

Dependencies: pythonOCC (FreeCAD 1.1 bundled), netgen-mesher (pip install into FreeCAD's Python),
CalculiX 2.22 (bundled with FreeCAD 1.1), numpy, matplotlib.

---

### Abaqus/Standard pipeline

Requires Abaqus 2025 (HF3) installed at `N:\CAE\simulia\v2025FP2524\`.  
Mesh is reused from the CalculiX pipeline (`ValveSpring_oval_mesh.inp` must already exist).

```bash
# Run the full Abaqus pipeline (inp generation + solver + postprocess + plot)
python run_abaqus.py [cpus]   # cpus defaults to 4; use 16 for production runs
```

This executes three phases automatically:
1. **Input conversion** — reads `ValveSpring_oval_contact.inp` (CalculiX) and writes
   `ValveSpring_oval_contact_abaqus.inp` with Abaqus-compatible output keywords
2. **Solver** — runs `abaqus job=... cpus=N mp_mode=threads interactive`
3. **Postprocess** — runs `abaqus python postprocess_abaqus.py` to extract reaction
   forces from the `.odb`, then plots `spring_FvL_abaqus.png`

**CalculiX → Abaqus conversion details:**

| CalculiX keyword | Abaqus replacement | Notes |
|---|---|---|
| `*STEP, NLGEOM, INC=N` | `*STEP, NLGEOM=YES, INC=N` | Flag syntax |
| `*NODE PRINT, ..., TOTALS=ONLY` | `*NODE PRINT, ..., TOTALS=YES` | `ONLY` not supported in Abaqus 2025 |
| `*NODE FILE` | removed | CalculiX `.frd` format |
| `*EL FILE` | removed | CalculiX `.frd` format |
| `*CONTACT FILE` | removed | CalculiX `.frd` format |
| `*SURFACE BEHAVIOR, PRESSURE-OVERCLOSURE=LINEAR` | unchanged (kept as LINEAR) | HARD contact causes false 400mm penetrations on the fine mesh; LINEAR 50 N/mm³ passes through |
| — | `*CONTACT CONTROLS, STABILIZE=0.0002` | Viscous regularisation per step (finer mesh) |
| — | `*OUTPUT, FIELD, FREQUENCY=N` | Abaqus `.odb` field output |
| — | `*NODE OUTPUT` `U, RF` | Displacements + reaction forces |
| — | `*ELEMENT OUTPUT` `S, MISES` | Stress tensor + von Mises |
| — | `*CONTACT OUTPUT` `CSTRESS, CDISP` | Contact pressure + slip |

**Contact formulation (2026-06-14):** `*SURFACE BEHAVIOR, PRESSURE-OVERCLOSURE=EXPONENTIAL`
with c0=0.01 mm, p0=0.1 MPa. The previous c0=0.1 mm allowed 45 µm penetration and produced
"PENETRATION ERROR TOO LARGE" warnings throughout Step 2. The 10× tighter c0=0.01 mm ensures
coil surfaces begin resisting at ~0.01 mm overclosure, matching physical coil-to-coil contact.
`*CONTACT CONTROLS, STABILIZE=0.001` is injected per step for viscous contact regularisation.

**Result files produced:**

| File | Description |
|---|---|
| `ValveSpring_oval_contact_abaqus.inp` | Abaqus input deck (converted from CalculiX) |
| `ValveSpring_oval_contact_abaqus.odb` | Abaqus result database (displacements, stress, contact) |
| `ValveSpring_oval_contact_abaqus.dat` | Solver log with node-print reaction forces |
| `ValveSpring_oval_contact_abaqus_rf.txt` | Extracted reaction forces: `s[mm]  F[N]` |
| `spring_FvL_abaqus.png` | F–L plot (Abaqus FEA + measurement + analytical fit) |

---

## Files

| File | Description |
|------|-------------|
| `generate_spring.py` | Parametric CAD generator (pythonOCC). Variable pitch via `helix_z()`, D_pitch=0.063. |
| `mesh_netgen.py` | Netgen mesher: C3D10, maxh=0.50 mm, orientation fix, mid-side node straightening, degenerate element filter. |
| `spring_analysis.py` | CalculiX FEA: 2-step preload+lift, self-contact, result parsing, progressive-rate analytical model. |
| `run_abaqus.py` | **Abaqus pipeline**: inp conversion + solver invocation + ODB postprocess + F-L plot. |
| `postprocess_abaqus.py` | Abaqus Python script (run via `abaqus python`): extracts nodal RF from `.odb` → `_rf.txt`. |
| `_viz_xsection.py` | Cross-section mesh density visualiser (`python _viz_xsection.py [z_mm]`). |
| `mesh_contact_fine.geo` | Gmsh geo (reference/future use — Gmsh cannot produce volume mesh for this geometry). |
| `ValveSpring.step` | STEP CAD (variable-pitch beehive helix, D_pitch=0.063, ground ends). |
| `ValveSpring.stl` | STL for visualisation. |
| `ValveSpring_oval_mesh.inp` | C3D10 mesh for oval wire profile (382 100 nodes / 235 495 elements, LMAX=1.0 mm). |
| `ValveSpring_oval_contact.inp` | CalculiX input deck (2-step NLGEOM, self-contact, oval profile). |
| `ValveSpring_oval_contact_abaqus.inp` | Abaqus input deck (auto-generated from CalculiX by `run_abaqus.py`). |
| `ValveSpring_oval_contact_abaqus.odb` | Abaqus result database (displacement, stress, contact). |
| `ValveSpring_oval_contact_abaqus_rf.txt` | Extracted reaction forces: compression [mm] vs force [N]. |
| `spring_FvL_abaqus.png` | Abaqus F–L plot (FEA + measurement + analytical fit). |
| `spring_FvL_oval.png` | CalculiX F–L plot (oval profile). |
| `INT_Spring_measurement.txt` | Measured F–lift data (398 points, 0–10 mm valve lift). |
