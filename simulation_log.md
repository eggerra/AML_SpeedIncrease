# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Run started:** 2026-06-14 15:21:09
**Job:** ValveSpring_oval_contact_abaqus

## Fix applied
- `n_closed`: 2.026 → 1.25 (drawing value)
- `n_active`: 4.548 → 6.1 (spring no longer goes solid at s≈14 mm)
- `D_pitch`:  0.0907 → 0.0776 (kink1 preserved at lift=4.05 mm)
- `L0_oval`:  39.471 → 39.182 mm
- Contact:    EXPONENTIAL c0=0.1 mm → c0=0.01 mm (10× tighter penetration)

## Progress

## 2026-06-14 15:21:09  —  CAD generation
**Status:** RUNNING

## 2026-06-14 15:21:23  —  CAD generation
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval.step (2897 kB)

## 2026-06-14 15:21:23  —  Meshing
**Status:** RUNNING — LMAX=1.0 mm, Netgen (may take 5-15 min)

## 2026-06-14 15:24:01  —  Meshing
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval_mesh.inp (4 MB)

## 2026-06-14 15:24:01  —  FEA input
**Status:** RUNNING — writing Abaqus/CalculiX INP

## 2026-06-14 15:25:18  --  CalculiX Step 1 (preload), Inc 2/~15
**Status:** RUNNING -- pipeline restarted at 15:21; CalculiX on Inc 2 of ~15 (s~0.5-1.0 mm of 7.58 mm preload)

- CAD: done (15:21, 2897 kB)
- Mesh: done (15:24, 4 MB, Netgen LMAX=1.0 mm)
- FEA input stage: CalculiX running (oval_pipeline.log: 509 lines, inc 2)
  - ~9000 contact spring elements per iteration (normal, stable)
  - CalculiX expected to diverge again at ~inc 7 (c0=0.01 mm exponential),
    but will now exit cleanly (fix applied) and pipeline will continue to Abaqus
- Abaqus: NOT yet started (.sta shows old run only; new job pending)

## 2026-06-14 15:32:36  —  FEA input
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval_contact.inp (177 kB)

## 2026-06-14 15:32:36  —  Abaqus solve
**Status:** RUNNING — this typically takes 10-20 hours

## 2026-06-14 15:35:15  --  Abaqus/Standard Step 1 (preload), Inc 10/~15
**Status:** RUNNING -- Abaqus started 15:33 on 2026-06-14, new geometry (n_closed=1.25)

- CalculiX: diverged at inc 7 as expected, exited cleanly (fix confirmed working)
- Abaqus: RUNNING -- ValveSpring_oval_contact_abaqus.sta shows:
  - Step 1 (preload 0->7.58 mm), inc 10 done, s=5.00 mm (66% of preload)
  - All increments converging in 1 attempt, 1-6 iters (excellent stability)
  - CONTACT CONTROLS STABILIZE=0.001 handling c0=0.01 mm without issues
  - Inc size = 0.5 mm (no reductions needed so far)
- Step 2 (10 mm valve lift) will start after ~5 more increments

## 2026-06-14 15:45:33  --  Abaqus/Standard Step 2 (valve lift), Inc 18, lift=3.28 mm
**Status:** RUNNING -- Step 2 (valve lift 0->10 mm), 3.28/10 mm complete (33%)

- Step 1 (preload): DONE
- Step 2 progress (ValveSpring_oval_contact_abaqus.sta, last line):
  - Inc 18, attempt 1U (unconverged cutback in progress), lift=3.28 mm
  - Inc sizes have dropped from 0.5 mm to 0.04-0.11 mm as coil contact increases
  - Incs 16-17: 3 severe discontinuity iterations (coil binding events)
  - Inc 18: 5 SDIs, 1U -- Abaqus cutting back; still converging
- ~67% of lift remaining (6.72 mm); expect further cutbacks near coil bind zone

## 2026-06-14 15:54:55  --  Abaqus/Standard Step 2, Inc 37, lift=3.91 mm / 10 mm
**Status:** RUNNING -- 39% of valve lift complete, converging steadily

- Step 2 (valve lift): inc 37, lift=3.91 mm of 10 mm (39%)
- Inc sizes stabilised at ~0.026-0.040 mm (fine stepping through early bind zone)
- All recent increments converging in 1 attempt, 3-5 SDIs, 4-6 total iters (healthy)
- Approaching kink1 at lift=4.05 mm (s=11.63 mm) -- first coil binding event
- No unconverged cutbacks since inc 18; solver tracking contact smoothly

## 2026-06-14 16:04:51  --  Abaqus/Standard Step 2, Inc 56, lift=4.67 mm / 10 mm
**Status:** RUNNING -- 47% of valve lift complete, past kink1

- Step 2 (valve lift): inc 56, lift=4.67 mm of 10 mm (47%)
- Kink1 (lift=4.05 mm, first coil bind) passed cleanly at inc ~42
- Inc size stable at 0.03955 mm; all increments 1 attempt, 1-2 SDIs, 4-6 iters
- Next milestone: kink2 at lift=7.67 mm (rate change 36.5->40.9 N/mm)
