# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Run started:** 2026-06-15 01:05:15
**Job:** ValveSpring_oval_contact_abaqus

## Change applied
- `L0`:       38.717 → 46.1 mm (drawing value restored)
- `L0_oval`:  39.182 → 46.565 mm (38.8 + 2×1.25×3.106)
- `D_pitch`:  0.0776 → 0.0629 (kink1 preserved at lift=4.05 mm; s_bind=18.55 mm)
- `n_closed`: 1.25 (drawing, unchanged)

## Progress

## 2026-06-15 01:05:15  —  CAD generation
**Status:** RUNNING

## 2026-06-15 01:05:24  --  Pipeline COMPLETE (run_full_pipeline.py exited)

**Status:** DONE -- full pipeline finished; results confirm force blowup (same as documented)

- run_full_pipeline.py completed: CAD(14s) + mesh(158s) + INP(515s) + Abaqus(34140s=9.5h)
- Abaqus result: 39 points, compression 2.50-17.49 mm, F=87-9377 N
- .sta confirms: Step 2 reached inc 178, lift=9.90/10 mm
- Force blowup at lift~5.9 mm (s~13.5 mm) unchanged -- contact c0=0.01 mm issue
- Pipeline process (PID 1327) has now exited cleanly
- Next action: fix contact c0=0.1 mm in spring_analysis.py, rerun
