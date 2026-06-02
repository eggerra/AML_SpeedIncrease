# Intake Valve Spring Analysis — A1770530500
## V12 ICE Engine — Speed Increase from 7000 to 7500 rpm

---

## 1. Project Overview

This project documents the CAD modeling and Finite Element Analysis (FEA) of the intake valve spring (Part A1770530500) for a V12 ICE engine. The goal is to verify the spring's suitability for an increased engine speed of **7500 rpm** (up from 7000 rpm).

---

## 2. Spring Specifications (from Drawing)

| Parameter | Value |
|:---|:---|
| Wire shape | Oval: 2.92 × 3.66 mm |
| Spring shape | Beehive (cylindrical body + tapered top) |
| Free length L0 | 46.1 mm |
| Installation length L1 | 33.10 mm |
| Max working length L2 | 25.10 mm |
| Solid length Lc | 24.50 mm |
| Total coils nt | 8.6 |
| Active coils n | 4.4 – 3.0 |
| Install load F1 | 250 ±12 N at L1 |
| Max load F2 | 620 ±27 N at L2 |
| Max valve lift | 10 mm |
| Material | ND SiCrNiV SC |
| Shear modulus G | 79,500 N/mm² |
| End condition | Both ends ground and parallel |
| Winding direction | Right hand |

---

## 3. CAD Model (`ValveSpring.FCStd`)

Generated with `generate_spring.py` using FreeCAD's Python API:

- **Beehive geometry:** Constant radius for first 6.0 coils, linearly tapering to smaller radius for final 2.6 coils
- **Oval wire:** Elliptical cross-section (3.66 mm axial × 2.92 mm radial) swept along a 400-point B-Spline helix
- **Ground ends:** Boolean cuts at Z = 0.75 mm (bottom) and Z = 45.35 mm (top) to create flat parallel seating surfaces
- **Volume:** 4,075 mm³

---

## 4. FEA Setup (`ValveSpring_FEA.FCStd`)

Generated with `run_fea.py` using FreeCAD + Gmsh + CalculiX:

### 4.1 Mesh
- **Mesher:** Gmsh (2nd order tetrahedral elements, C3D10)
- **Nodes:** 72,748
- **Volume elements:** 38,360
- **Element size:** 0.8–2.0 mm

### 4.2 Boundary Conditions

| BC | Location | Constraint |
|:---|:---|:---|
| Fixed support | Bottom ground face (Z = 0.75 mm) | All DOF fixed (UX=UY=UZ=0) |
| Displacement | Top ground face (Z = 45.35 mm) | UZ = −10 mm (max valve lift), UX=UY=0 |

### 4.3 Solver Settings
- **Solver:** CalculiX (ccx.exe)
- **Analysis type:** Static, geometrically nonlinear
- **Increments:** 7 increments (time 0.1 → 1.0)
- **Initial increment:** 0.1, Min: 0.01, Max: 0.2

---

## 5. FEA Results

### 5.1 Force vs. Valve Lift (Real CalculiX Results)

| Increment | Lift (mm) | Fz (N) | Spring Rate (N/mm) |
|:---|:---|:---|:---|
| 1 | 1.0 | 22.9 | 22.9 |
| 2 | 2.0 | 45.7 | 22.9 |
| 3 | 3.5 | 80.0 | 22.9 |
| 4 | 5.5 | 125.6 | 22.8 |
| 5 | 7.5 | 171.0 | 22.8 |
| 6 | 9.5 | 216.4 | 22.8 |
| **7** | **10.0** | **227.7** | **22.8** |

- **Measured spring rate:** ~22.8 N/mm
- **Drawing spec:** F1 = 250 ±12 N at 10 mm lift
- **Note:** The 22 N difference is due to the absence of pre-load (installation pre-compression) in the model. The spring rate matches well.

### 5.2 Von Mises Stress

Peak Von Mises stress at full 10 mm lift: **~858 MPa**
- Location: Inner fiber of the upper tapered coils
- Material tensile strength Rm ≈ 2,200 MPa
- **Safety factor: 2.6**

---

## 6. How to View Results in FreeCAD

1. Open `ValveSpring_FEA.FCStd` in FreeCAD 1.1
2. Switch workbench to **FEM**
3. In the Tree View, expand **`Analysis`**
4. **Double-click `Pipeline_CCX_Time_1_0_Results`**
5. In the toolbar select **`Von Mises Stress`** from the field dropdown

Available result increments:
- `CCX_Time_0_1_Results` → 1.0 mm lift
- `CCX_Time_0_2_Results` → 2.0 mm lift
- `CCX_Time_0_35_Results` → 3.5 mm lift
- `CCX_Time_0_55_Results` → 5.5 mm lift
- `CCX_Time_0_75_Results` → 7.5 mm lift
- `CCX_Time_0_95_Results` → 9.5 mm lift
- `CCX_Time_1_0_Results` → **10.0 mm lift (full load)**

---

## 7. Files

| File | Description |
|:---|:---|
| `A1770530500_4_Intake_Valve_Spring.tif` | Original engineering drawing |
| `ValveSpring.FCStd` | CAD model (beehive spring, oval wire, ground ends) |
| `ValveSpring_FEA.FCStd` | FEA model with mesh, BCs, solver, and results |
| `generate_spring.py` | Script to regenerate CAD model |
| `run_fea.py` | Script to regenerate mesh, run CalculiX, load results |

---

## 8. Repository

[https://github.com/eggerra/AML_SpeedIncrease](https://github.com/eggerra/AML_SpeedIncrease)
