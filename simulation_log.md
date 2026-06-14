# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Run started:** 2026-06-15 00:56:16
**Job:** ValveSpring_oval_contact_abaqus

## Change applied
- `L0`:       38.717 → 46.1 mm (drawing value restored)
- `L0_oval`:  39.182 → 46.565 mm (38.8 + 2×1.25×3.106)
- `D_pitch`:  0.0776 → 0.0629 (kink1 preserved at lift=4.05 mm; s_bind=18.55 mm)
- `n_closed`: 1.25 (drawing, unchanged)

## Progress

## 2026-06-15 00:56:16  —  CAD generation
**Status:** RUNNING

## 2026-06-15 00:56:31  —  CAD generation
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval.step (2973 kB)

## 2026-06-15 00:56:31  —  Meshing
**Status:** RUNNING — maxh=1.0 mm, Netgen (may take 5-15 min)

## 2026-06-15 00:56:39  —  Meshing
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval_mesh.inp (4 MB)

## 2026-06-15 00:56:39  —  FEA input
**Status:** RUNNING — writing Abaqus/CalculiX INP

## 2026-06-15 01:01:36  —  Abaqus solve
**Status:** COMPLETED — 39 result points  F=87–9377 N  wall=9.5h

## Summary
- Total wall time: 9.5h (Abaqus only)
- Plot: D:\Projects_AI\AML_SpeedIncrease\spring_FvL_abaqus.png
- RF data: D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval_contact_abaqus_rf.txt
