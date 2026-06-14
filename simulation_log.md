# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Run started:** 2026-06-14 15:02:38
**Job:** ValveSpring_oval_contact_abaqus

## Fix applied
- `n_closed`: 2.026 → 1.25 (drawing value)
- `n_active`: 4.548 → 6.1 (spring no longer goes solid at s≈14 mm)
- `D_pitch`:  0.0907 → 0.0776 (kink1 preserved at lift=4.05 mm)
- `L0_oval`:  39.471 → 39.182 mm
- Contact:    EXPONENTIAL c0=0.1 mm → c0=0.01 mm (10× tighter penetration)

## Progress

## 2026-06-14 15:02:38  —  CAD generation
**Status:** RUNNING

## 2026-06-14 15:02:50  —  CAD generation
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval.step (2897 kB)

## 2026-06-14 15:02:50  —  Meshing
**Status:** RUNNING — LMAX=1.0 mm, Netgen (may take 5-15 min)

## 2026-06-14 15:05:28  —  Meshing
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval_mesh.inp (4 MB)

## 2026-06-14 15:05:28  —  FEA input
**Status:** RUNNING — writing Abaqus/CalculiX INP

## 2026-06-14 15:20:43  --  CalculiX diverged (Step 1 Inc 7)
**Status:** FAILED (CalculiX) / RESTARTING

- CalculiX diverged at increment 7 of 15 (s=3.5mm of 7.58mm preload)
- Root cause: c0=0.01mm exponential contact too stiff for CalculiX;
  59K contact spring elements activated suddenly, residual reached ~1.5e21 N
- The CalculiX INP file (ValveSpring_oval_contact.inp) was written successfully
- Fix applied: spring_analysis.py now exits cleanly on CalculiX failure
  (Abaqus is the actual solver; CalculiX result not needed)
- Old Abaqus run (wrong geometry, n_closed=2.026) completed at 00:05 on 2026-06-14
- Pipeline restarted: new geometry will now proceed to Abaqus solve
