# AW82001 Valvetrain Model Analysis
## AVL EXCITE Timing Drive — Intake Valve Train, Right Bank

**Model file:** `vtRBint01.etd`  
**Model path:** `D:\AW82001\5005\ref_Tamas\AW82001_5004_20-Loop1-ModelStatus\Status20260608\excite_td\`  
**EXCITE version:** 24.10  
**Analysis date:** 2026-06-10  
**Focus elements:** `INTr_HLIF*` (Hydraulic Lash Adjuster), `INTr_SPG*` (Valve Spring)

---

## 1. Model Overview

The `vtRBint01.etd` project models the **intake valve train of the right cylinder bank** for the AW82001 engine. It is one of four ETD models in the project directory (also: left-bank intake `vtLBint01.etd`, and exhaust banks). The model covers 8 intake valves (one per cylinder/valve pair), each represented by a complete element chain from camshaft to valve seat.

### 1.1 Simulation Cases

The model is set up as a sweep over engine speeds. Results subdirectories are named `vtRBint01.Ref_C10.Pup_XXXXrpm`:

| Run directory | Engine speed | Status |
|---|---|---|
| Ref_C10.Pup_7000rpm | 7000 rpm | Completed (56 MB) |
| Ref_C10.Pup_7100rpm | 7100 rpm | Completed (60 MB) |
| Ref_C10.Pup_7200rpm | 7200 rpm | Completed (60 MB) |
| Ref_C10.Pup_7300rpm | 7300 rpm | Completed (40 MB) |
| Ref_C10.Pup_7400rpm | 7400 rpm | Completed (33 MB) |
| Ref_C10.Pup_7500rpm | 7500 rpm | Completed (33 MB) |

The full load-case sweep defined in the `caseTable` spans 1500–7500 rpm. Gas load data is provided in `Loads/Gas1_RBank/FgasIn_Fgas_XXXXrpm.dat` for 1500–7000 rpm.

### 1.2 Cam Profile

**Reference cam:** `Int165_Reference.GID` (INT 165° duration specification)  
**Follower radius:** 8.5 mm  
**Maximum valve lift:** 10.0 mm  
**Natural frequency:** 1990 1/s  
**Maximum contact stress:** 1086 N/mm²  
Resolution: 0.25°/data point. Contains 48 result columns including valve lift, velocity, acceleration, contact stress, spring force, and mass force.

---

## 2. Valve Spring — `INTr_SPG*` (8 instances)

### 2.1 EXCITE Element Type

The EXCITE **SpringMacro (SPG)** element models a complete valve spring as a flexible multi-body chain of coil (SPPR) and torsion (CTOR) elements. Key capabilities:
- Progressive spring rate via force or stiffness characteristic table
- Coil-to-coil contact modeled independently from spring stiffness
- Pitch diagram defines non-uniform coil spacing
- Coupled to rigid ground body at both ends

### 2.2 Model Parameters — `INTr_SPG1` (representative; all 8 instances identical)

**EXCITE element:** `SpringMacro`, `elem24`–`elem81` (elements 24, 25, 36, 45, 54, 63, 72, 81)

#### Geometry

| Parameter | Model value | Unit |
|---|---|---|
| Spring type | Cylindrical | — |
| Wire shape | Elliptic | — |
| Elliptic wire height (lift direction) | 2.95 | mm |
| Elliptic wire width (lateral) | 3.36 | mm |
| Coil diameter reference | Outer diameter | — |
| Outer coil diameter | 23.22 | mm |
| Free length | 45.2 | mm |
| Total coils | 9.25 | — |
| End coils (valve side) | 1.0 | — |
| End coils (head side) | 2.0 | — |
| Active coils (calculated) | 6.25 | — |
| Elements per coil | 8 | — |
| Total spring mass | 32.0 | g |

#### Material

| Parameter | Model value | Unit |
|---|---|---|
| Shear modulus G | 79 500 | N/mm² |
| Young's modulus E | 210 000 | N/mm² |
| Poisson's ratio | 0.3 | — |
| Mass density | 7 850 | kg/m³ |

#### Installation & Loading

| Parameter | Model value | Unit |
|---|---|---|
| Installation definition | Preload | — |
| Preload (valve closed) | 250.0 | N |
| Installed length (derived from force table) | ≈ 36.2 | mm |
| Spring damping (relative) | 0.02 (2%) | — |
| Damping time constant | 1.4×10⁻⁵ | s |
| Absolute damping | 0.001 | N·s/mm |
| Block stiffness | 300 000 | N/mm |
| Block damping (relative) | 0.30 (30%) | — |

#### 2.3 Force Characteristic Table

The spring characteristic is defined as a **nonlinear force vs. spring length** table with 13 data points, capturing the progressive stiffening behavior:

| Spring length (mm) | Compression from free length (mm) | Spring force (N) |
|---|---|---|
| 45.2 | 0.0 | ~0 |
| 43.0 | 2.2 | 55.7 |
| 41.0 | 4.2 | 108.0 |
| 37.5 | 7.7 | 209.7 |
| 36.75 | 8.45 | 233.2 |
| **36.2** | **9.0** | **250.8** ← valve closed (preload) |
| 32.0 | 13.2 | 396.0 |
| 31.0 | 14.2 | 433.3 |
| 30.0 | 15.2 | 471.7 |
| 29.0 | 16.2 | 511.1 |
| 27.0 | 18.2 | 592.0 |
| **26.2** | **19.0** | **625.0** ← near full valve lift |
| 24.0 | 21.2 | 730.0 |

**Effective spring rate (valve-closed to full-lift, 36.2→26.2 mm):** ≈ 37.4 N/mm

#### 2.4 Stiffness Characteristic

The model also stores an explicit stiffness table (tangent rate), derived from the force characteristic:

| Spring length (mm) | Stiffness (N/mm) |
|---|---|
| 45.2 (free) | 23.9 |
| 43.0 | 23.9 |
| 41.0 | 26.1 |
| 37.5 | 29.1 |
| 36.75 | 31.3 |
| 36.2 (installed) | 32.0 |
| 32.0 | 34.6 |
| 31.0 | 37.3 |
| 30.0 | 38.4 |
| 29.0 | 39.5 |
| 27.0 | 40.4 |
| 26.2 (full lift) | 41.3 |
| ≤24.4 (near solid) | 47.7 |

#### 2.5 Coil Pitch Diagram

The spring has a **non-uniform pitch** defined by 27 data points along the coil count axis (0 to 9.25). The pitch values are small and nearly zero at the ends (closed end coils) and maximum in the center active zone, representing the beehive-type progressive geometry.

---

## 3. Hydraulic Lash Adjuster — `INTr_HLIF*` (8 instances)

### 3.1 EXCITE Element Type

The EXCITE **HydraulicLifter (HLIF)** element models a **hydraulic lash adjuster** with the following physical sub-models:
- External spring + preloaded plunger
- High-pressure oil volume (compressible, with bulk modulus from lookup table)
- Ball check valve (poppet) for oil refill from supply line
- Annular leakage gap between plunger body and lifter bore
- Linear damping model for plunger motion

The HLIF element automatically compensates valve lash by extending until contact is established, then holds via oil pressure during the lift event.

### 3.2 Model Parameters — All 8 Instances (identical)

**EXCITE element:** `ASE "Hlif"`, `elem11` (INTr_HLIF1) through `elem79` (INTr_HLIF8)

#### Mechanical Properties

| Parameter | Model value | Unit | Notes |
|---|---|---|---|
| Clearance (clea) | 1.365 | mm | Lash at assembly; HLA closes this hydraulically |
| Total mass | 6.5 | g | HLA body including oil fill |
| Plunger spring preload | 17.5 | N | HLA extension spring load |
| Plunger spring stiffness | 4.79 | N/mm | Extension spring rate |
| Structure contact stiffness (st0) | 100 000 | N/mm | Active when lash is overcome |
| Plunger displacement (dplo) | 8.6 | mm | Max plunger travel |
| Oil volume (pressure chamber) | 188 | mm³ | Working oil volume |
| Oil supply pressure (psup) | 3.0 | bar | Nominal supply pressure |
| Linear damping (damp) | INF | N·s/m | Effectively rigid when locked |
| Relative damping ratio | 0.1 | — | Used during transient |
| Motion direction (uvec) | [0, 0, −1] | — | Axial, downward |

#### Oil Properties

| Parameter | Model value | Unit | Notes |
|---|---|---|---|
| Oil density (dens) | 764 | kg/m³ | Default; variable `OilDensity` = 761.21 |
| Dynamic viscosity (visk) | 0.00384 | Pa·s | Default; variable `dyn_visco_bearings` = 0.00588 |
| Viscosity-pressure coefficient | 1.4×10⁻⁸ | m²/N | |
| Elasticity modulus (oil) | 6×10⁸ | Pa | = 600 MPa |
| Oil bulk modulus (table) | See §3.3 | N/mm² | From external file |

The global domain variables allow overriding these defaults:
- `Cyl_head_gallery` = 3.6 bar (cylinder head gallery pressure)
- `dyn_visco_bearings` = 0.00588 Pa·s
- `OilDensity` = 761.21 kg/m³

#### Ball Check Valve (Poppet)

| Parameter | Model value | Unit |
|---|---|---|
| Ball diameter | 2.9 | mm |
| Seat diameter (dbva) | 2.0 | mm |
| Max ball lift (lmax) | 0.25 | mm |
| Ball mass | 0.1 | g |
| Ball spring preload | 0.05 | N |
| Flow resonance frequency | 10 | Hz |

#### Leakage / Precision Fit

| Parameter | Model value | Unit | Notes |
|---|---|---|---|
| Gap height (gh) | 0.005 | mm | Radial clearance per side (~5 µm) |
| Gap length (gl) | 5.33 | mm | Axial length of annular gap |
| Flow coefficient (co) | 0.02 | — | |
| Flow offset force (fo) | 0.5 | N | |
| Viscous damping (vi) | 0.2 | N·s/m | |

### 3.3 Oil Bulk Modulus Data

**File:** `Loads/OilProperties/BulkM_3PrAir_120Celsius.txt`  
**Condition:** 120°C oil temperature, 3% dissolved air by volume

| Pressure (MPa) | Bulk modulus (N/mm²) |
|---|---|
| −0.10 | ~0 |
| 0 | 3.32 |
| 0.058 | 8.20 |
| 0.151 | 20.2 |
| 0.298 | 48.6 |
| 0.531 | 111.9 |
| 0.900 | 233.6 |
| 1.485 | 414.5 |
| 2.412 | 605.3 |
| 3.881 | 754.4 |
| 6.210 | 860.1 |
| 9.900 | 948.7 |
| 15.749 | 1 045.0 |
| 25.019 | 1 166.8 |
| 39.711 | 1 327.3 |

The strong nonlinearity at low pressures (dissolved air degas effect) is critical for HLA response at low supply pressures. Two additional files exist but are not referenced by the model: `BulkMRev_2PrAir.txt` and `BulkMRev_3PrAir.txt` (reverse-direction bulk modulus data).

---

## 4. Cross-Reference: Model Parameters vs. Engineering Drawings

### 4.1 Valve Spring (Model vs. Drawing A1770530500_4)

| Parameter | Model | Drawing | Match |
|---|---|---|---|
| Free length | 45.2 mm | 46.1 mm | −0.9 mm (−2%) |
| Installed length | ≈ 36.2 mm | 36.1 mm | ✓ |
| Preload force | 250 N | 250 N | ✓ |
| Full-lift length | 26.2 mm | 26.1 mm | ✓ |
| Full-lift force | 625 N | 620 N | +0.8% ✓ |
| Wire cross-section | 2.95 × 3.36 mm | 2.92 × 3.66 mm | Height ≈ ✓, Width −8% |
| Total coils | 9.25 | 8.6 | +0.65 coils |
| Active coils | 6.25 (calc.) | 6.1 | +2.5% |
| Coil type | Cylindrical | Beehive (tapered) | ✗ (see note) |
| Outer diameter | 23.22 mm (single value) | 19.6–15.7 mm (tapered) | ✗ (see note) |
| Material shear modulus | 79 500 N/mm² | — (VD SiCrNi SC) | Typical value ✓ |
| Spring mass | 32.0 g | — | — |

> **Note on cylindrical vs. beehive geometry:** The EXCITE SpringMacro element is declared as "Cylindrical" type with a single outer diameter (23.22 mm), which is an approximation of the physical beehive spring. The actual beehive taper (OD 19.6 mm at valve end, 15.7 mm at head end) is partially captured through the **non-uniform pitch diagram** and **progressive force characteristic**. The functional behavior (force vs. displacement, progressive rate) is well matched; the cylindrical simplification slightly overestimates the spatial envelope but does not significantly affect dynamic behavior in 1D simulation.

> **Free length discrepancy:** The model free length (45.2 mm) is 0.9 mm shorter than the drawing (46.1 mm). However, since the installed length and preload force are well aligned, the model appears to have been calibrated to the installed condition rather than adjusted for the free-length discrepancy. The force characteristic table is the governing input for spring loads — this is correctly set up.

### 4.2 Hydraulic Lash Adjuster (Model vs. Drawing A2700504200)

| Parameter | Model | Drawing | Match |
|---|---|---|---|
| Plunger spring preload | 17.5 N | 17.5 N (upper spring, max) | ✓ |
| Plunger spring stiffness | 4.79 N/mm | — | — |
| Oil supply type | Engine oil, 3 bar | SAE 5W, engine pressure | ✓ |
| Ball valve diameter | 2.9 mm | — | — |
| Plunger diameter (derived from gap) | — | ~10.5–10.15 mm bore | — |
| Cleanliness standard | — | DBL 6516-30 | (not in model) |

---

## 5. Model Consistency Observations

### 5.1 Valve Spring

1. **Force calibration is correct.** The force table is the authoritative input and matches the drawing specification at both the installed (250 N @ 36.2 mm) and full-lift (625 N @ 26.2 mm) conditions to within 1%.

2. **Progressive stiffening is captured.** The tangent stiffness increases from ~24 N/mm at free length to ~41 N/mm near full lift, consistent with the beehive coil-binding mechanism.

3. **Free length differs by 0.9 mm** from the drawing. This appears intentional — the model appears to have been tuned to the force characteristic from measurement or FEA, rather than using the nominal drawing geometry to analytically derive forces.

4. **Coil count (9.25 vs. 8.6) and wire width (3.36 vs. 3.66 mm)** are minor geometric deviations that affect the visual representation and mass distribution but not the primary spring force response.

5. **Spring mass (32 g)** is not specified on the drawing; the model value is reasonable for this spring size and wire section.

6. **Block stiffness (300 000 N/mm)** and block damping (0.30 relative) model solid-height contact. These are numerically stiff values to limit coil-clash penetration.

### 5.2 Hydraulic Lash Adjuster

1. **All 8 HLIF instances are identical**, as expected for a symmetric 8-valve right-bank configuration.

2. **Lash clearance (clea = 1.365 mm)** is a large initial gap. The HLA extends hydraulically to close this gap before the cam event. This value may represent a worst-case (cold-start, drained) condition.

3. **Oil supply pressure (psup = 3.0 bar) is slightly below the gallery pressure variable (Cyl_head_gallery = 3.6 bar).** The gallery pressure variable feeds the HLIF element through the control variable linkage. The 0.6 bar difference may represent line losses between gallery and lifter bore.

4. **Gap height of 5 µm (gh = 0.005 mm)** represents the annular leakage path between plunger and bore. This is a critical parameter for HLA leak-down rate and should be verified against the drawing tolerance: bore Ø10.5–10.15 mm (implied plunger Ø ~10.1–10.4 mm, giving radial clearance ~5–25 µm per side). The model value (5 µm) is at the tight end of tolerance.

5. **Infinite linear damping (damp = INF)** locks the HLA once the high-pressure chamber is sealed. This is appropriate — once the ball valve closes, the oil volume is nearly incompressible at operating pressures (bulk modulus >400 N/mm² above 1.5 MPa).

6. **Oil bulk modulus table (BulkM_3PrAir_120Celsius.txt)** uses 120°C / 3% dissolved air. This is appropriate for a high-speed engine at operating temperature. The dissolved air creates nonlinear compliance at low pressures, which governs HLA refill dynamics during the low-pressure (base-circle) phase.

### 5.3 Overall Model Quality

- The model uses a **consistent oil property set** across all 8 HLIF elements via shared domain variables.
- The spring force characteristic is **measurement-calibrated** (not analytically derived from geometry), making it the most reliable representation of actual spring behavior.
- The **cylindrical spring approximation** in EXCITE is a standard simplification for beehive springs; the progressive rate is captured through the force table.
- No FEM flexible-body meshes are used (fem/meshes.txt is empty), indicating a **rigid multi-body approach** throughout.

---

## 6. File Structure Summary

```
excite_td/
├── vtRBint01.etd          ← Main model (this analysis)
├── vtRBexh01.etd          ← Exhaust, right bank
├── vtLBint01.etd          ← Intake, left bank
├── vtLBexh01.etd          ← Exhaust, left bank
├── CamProfile/
│   └── Int165_Reference.GID   ← 165° intake cam (10 mm lift)
├── CamDesign/
│   └── Int165_Ref.vtc          ← TYCON cam design project
├── Loads/
│   ├── Gas1_RBank/             ← Gas force data, 1500–7000 rpm
│   └── OilProperties/
│       └── BulkM_3PrAir_120Celsius.txt  ← HLA oil model
├── vtRBint01.Ref_C10/          ← Case metadata (no binary results here)
└── vtRBint01.Ref_C10.Pup_*/    ← Results at 7000–7500 rpm (33–60 MB each)
```

---

## 7. References

| Document | Description |
|---|---|
| `vtRBint01.etd` | AVL EXCITE TD model, VERSION-24.10 |
| `A1770530500_4_Intake_Valve_Spring.tif` | Intake valve spring engineering drawing |
| `A2700504200_HLA_Assembly.pdf` | HLA assembly drawing (Widmann/Stahl) |
| `EXCITE_TimingDrive_UsersGuide/` | AVL EXCITE TD documentation |
| `CamProfile/Int165_Reference.GID` | Reference cam profile (165° duration) |
| `Loads/OilProperties/BulkM_3PrAir_120Celsius.txt` | Oil bulk modulus at 120°C |
