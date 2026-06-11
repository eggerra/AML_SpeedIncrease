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

Kink positions (from phase-line departure, **compression measured from calibrated L0=38.717 mm**):

| Event | Valve lift | Compression from L0 | Force (meas) |
|-------|-----------|---------------------|-------------|
| Kink 1 (first binding) | 4.05 mm | 11.167 mm | 390.7 N |
| Kink 2 (upper zone)   | 7.67 mm | 14.787 mm | 525.3 N |
| Full lift | 10.00 mm | 17.117 mm | 620.7 N |

### Model calibration (2026-06-11) — L0 and n\_closed fitted to measurement

The drawing parameters alone produce an inconsistency: drawing L0=46.1 mm with nominal
geometry gives k_FEA≈26 N/mm and **F1_FEA=374 N** vs measured **F1=249 N** (−50%).

Two free parameters (L0, n\_closed) were fitted to two measurement constraints:

1. **F1=249 N at L1=31.6 mm** → requires k\_FEA=35 N/mm at the preload point
2. **Kink1 at lift=4.05 mm from L1** → sets D\_pitch for the new geometry

The required rate k\_FEA=35 N/mm follows directly from (F\_kink1−F1)/lift\_kink1 = 141.7/4.05.

| Parameter | Drawing | **Calibrated** | Derivation |
|-----------|---------|----------------|------------|
| L0 | 46.1 mm | **38.717 mm** | L1 + F1/k\_FEA = 31.6 + 249/35 |
| n\_closed | 1.25 | **2.026** | k\_ana=35/0.889=39.4 N/mm → sum(Rᵢ³)=3503 mm³ |
| n\_active | 6.1 | **4.548** | nt − 2×n\_closed |
| D\_pitch | 0.063 | **0.0907** | s\_bind=11.167 mm → p\_bot=5.375 mm |
| p\_bot | 5.96 mm (gap 3.04) | **5.375 mm (gap 2.455)** | — |
| p\_top | 6.76 mm | **6.447 mm** | — |

Wire cross-section and coil diameters are unchanged from the drawing.

**Analytical model check with calibrated parameters:**

| Quantity | Analytical | Measurement | Error |
|----------|-----------|-------------|-------|
| F @ preload (s=7.12 mm) | 249 N | 249 N | 0.0% |
| F @ kink1 (lift=4.05 mm) | 389.5 N | 390.7 N | 0.3% |
| F @ kink2 (lift=7.67 mm) | 521.8 N | 525.3 N | 0.7% |
| F @ full lift (lift=10 mm) | 617.1 N | 620.7 N | 0.6% |

---

## FEA setup

| Item | Detail |
|------|--------|
| Elements | C3D10 (10-node quadratic tetrahedra, straight mid-side nodes) |
| Nodes / elements | 251 318 / 150 560 |
| Material | E = 273 131 MPa (×1.326 mesh correction, nominal 206 000), ν = 0.30 |
| BCs — Step 1 | Bottom face fixed; top face compressed 0→7.1 mm (preload) |
| BCs — Step 2 | Top face compressed further 7.1→17.1 mm (10 mm valve lift) |
| Increment size | 0.5 mm fixed (14 + 20 = 34 increments total) |
| Analysis | NLGEOM static (large-displacement) |
| Self-contact | SURFACE TO SURFACE, penalty stiffness 1000 N/mm³ (deliberately soft for convergence) |
| Solver | CalculiX 2.22 (SPOOLES symmetric) |
| Mesher | Netgen (netgen-mesher via FreeCAD 1.1 Python) |

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

### Key findings (calibrated run — 2026-06-11)

Mesh: 251 318 nodes / 150 560 C3D10 elements.  
**E-correction**: the 0.5 mm mesh under-predicts spring stiffness by ×1.326 due to coarse
torsional discretisation (≈6 elements across the 2.92 mm wire) and unconstrained closed-coil
zone compliance (h\_closed=5.9 mm per end). E is scaled from 206 000 to 273 131 MPa so that
k\_FEA × s\_preload = F1\_measured. Stress magnitudes in the .frd output must be divided by
1.326 to recover physical values; stress distributions are unaffected.

| Quantity | Analytical (3-phase) | **FEA** | Measurement | FEA error |
|----------|---------------------|---------|-------------|-----------|
| F @ preload  (s=7.12 mm) | 249 N | **248 N** | 249 N | −0.5% |
| F @ kink1    (lift=4.05 mm) | 389 N | — | 390.7 N | — |
| F @ kink2    (lift=7.67 mm) | 522 N | — | 525.3 N | — |
| F @ full lift (s=17.12 mm) | 617 N | **609 N** | 620.7 N | −1.9% |

FEA output is at every 5th increment (FREQUENCY=5 in NODE PRINT) giving 7 data points
across the full stroke. The 3-phase progressive stiffening (green curve) is calibrated
from measurement and matches within 0.6 % at full lift.

---

## Running the pipeline

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

## Files

| File | Description |
|------|-------------|
| `generate_spring.py` | Parametric CAD generator (pythonOCC). Variable pitch via `helix_z()`, D_pitch=0.063. |
| `mesh_netgen.py` | Netgen mesher: C3D10, maxh=0.50 mm, orientation fix, mid-side node straightening, degenerate element filter. |
| `spring_analysis.py` | CalculiX FEA: 2-step preload+lift, self-contact, result parsing, progressive-rate analytical model. |
| `_viz_xsection.py` | Cross-section mesh density visualiser (`python _viz_xsection.py [z_mm]`). |
| `mesh_contact_fine.geo` | Gmsh geo (reference/future use — Gmsh cannot produce volume mesh for this geometry). |
| `ValveSpring.step` | STEP CAD (variable-pitch beehive helix, D_pitch=0.063, ground ends). |
| `ValveSpring.stl` | STL for visualisation. |
| `ValveSpring_mesh.inp` | Netgen C3D10 mesh (212k nodes, 118k elements). |
| `ValveSpring_contact.inp` | CalculiX input deck (2-step NLGEOM, self-contact). |
| `ValveSpring_contact.dat` | CalculiX reaction-force results. |
| `ValveSpring_contact.frd` | CalculiX displacement + stress results (binary). |
| `spring_FvL.png` | Force vs lift plot (FEA + analytical + measurement). |
| `INT_Spring_measurement.txt` | Measured F–lift data (396 points, 0–10 mm valve lift). |
