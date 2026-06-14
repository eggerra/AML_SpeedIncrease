# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Run started:** 2026-06-15 01:14:24
**Job:** ValveSpring_oval_contact_abaqus

## Change applied
- `L0`:       38.717 → 46.1 mm (drawing value restored)
- `L0_oval`:  39.182 → 46.565 mm (38.8 + 2×1.25×3.106)
- `D_pitch`:  0.0776 → 0.0629 (kink1 preserved at lift=4.05 mm; s_bind=18.55 mm)
- `n_closed`: 1.25 (drawing, unchanged)

## Progress

## 2026-06-15 01:14:24  —  CAD generation
**Status:** RUNNING

## 2026-06-15 01:14:27  —  CAD generation
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval.step (2973 kB)

## 2026-06-15 01:14:27  —  Meshing
**Status:** RUNNING — maxh=1.0 mm, Netgen (may take 5-15 min)

## 2026-06-15 01:14:32  —  Meshing
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval_mesh.inp (4 MB)

## 2026-06-15 01:14:32  —  FEA input
**Status:** RUNNING — writing Abaqus/CalculiX INP

## 2026-06-15 01:14:48  --  Pipeline idle; complete since ~02:04 (13 min ago)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-15 01:24:49  --  Pipeline idle; complete since ~02:04 (23 min ago)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun
