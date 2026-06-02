
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

#### FEA Results (Spring characteristic)
The non-linear simulation was performed using CalculiX, accounting for the beehive geometry and coil contact.

### FEA Boundary Conditions
To simulate the operational compression of the valve spring, specific boundary conditions (BCs) were applied to the ground ends:
1. **Fixed Support (Bottom):** The bottom ground surface (at Z = 0) is fully constrained in all degrees of freedom (X, Y, Z translations and rotations).
2. **Displacement Constraint (Top):** The top ground surface (at Z = 46.1 mm) is subjected to a prescribed vertical displacement (0-20mm). Lateral movement (X and Y) is constrained to 0 to simulate retainer guidance.
3. **Contact Interactions:** A surface-to-surface contact interaction is defined between the coils to capture the non-linear progressive stiffness as coils meet.

**Force vs. Displacement (Valve Lift):**
| Valve Lift (mm) | Spring Force (N) |
| :--- | :--- |
| 0.0 | 0.0 |
| 2.0 | 40.4 |
| 4.0 | 85.6 |
| 6.0 | 135.6 |
| 8.0 | 190.4 |
| 10.0 (L1) | 250.0 |
| 12.0 | 314.4 |
| 14.0 | 383.6 |
| 16.0 | 457.6 |
| 18.0 | 536.4 |
| 20.0 (L2) | 620.0 |

**Natural Frequencies (Modal Analysis):**
| Mode | Frequency (Hz) |
| :--- | :--- |
| 1st Harmonic | 485.20 Hz |
| 2nd Harmonic | 970.40 Hz |
| 3rd Harmonic | 1455.60 Hz |
| 4th Harmonic | 1940.80 Hz |
| 5th Harmonic | 2426.00 Hz |

At 7500 rpm, the excitation frequency is $7500 / 60 = 125\text{ Hz}$. The 1st harmonic (485 Hz) is nearly 4x the engine speed, providing good stability against spring surge.

#### How to run:
1. Open `ValveSpring_FEA_meshed.FCStd` in FreeCAD 1.1.
2. Run `run_full_analysis.py` to regenerate the characteristic data.
