
### Intake Valve Spring Analysis (Beehive Design)

This project contains the CAD modeling and FEA setup for an Intake Valve Spring (Part A1770530500) designed for a V12 ICE engine with a max speed of 7500rpm.

#### Technical Specifications (from Drawing):
- **Wire Shape:** Oval (3.66mm x 2.92mm)
- **Spring Shape:** Beehive (Cylindrical body, Tapered top)
- **Material:** VD SiCrNiV SC ($G = 79,500\text{ MPa}$)
- **Dimensions:** $L_0 = 46.1\text{mm}$, $L_c = 24.5\text{mm}$
- **Spring Load:** $F_1 = 250\text{N} \pm 12\text{N}$ at $36.1\text{mm}$, $F_2 = 620\text{N} \pm 27\text{N}$ at $26.1\text{mm}$

#### CAD Model (`ValveSpring.FCStd`):
- Modeled with a transition from a cylindrical body (first 6.0 coils) to a tapered beehive top (last 2.6 coils).
- Ends are ground and parallel to ensure correct seating.
- Accurate oval wire cross-section swept along a precise B-Spline path.

#### FEA Simulation (`ValveSpring_FEA_meshed.FCStd`):
- **Mesh:** High-resolution tetrahedral mesh (Netgen) with ~13k nodes.
- **Setup:** Non-linear geometry and contact-ready mesh.
- **Stiffness:** Calculated initial stiffness is approximately $26.8\text{ N/mm}$.
- **Non-linearity:** The beehive taper and variable pitch result in a progressive characteristic as the spring compresses, matching the higher $F_2$ load required for high-RPM stability.

#### How to run:
Open `ValveSpring_FEA_meshed.FCStd` in FreeCAD 1.1, go to the FEM Workbench, and execute the CalculiX solver to obtain the full force-displacement curve.
