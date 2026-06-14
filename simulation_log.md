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

## 2026-06-14 16:14:53  --  Abaqus/Standard Step 2, Inc 70, lift=5.87 mm / 10 mm
**Status:** RUNNING -- 59% of valve lift complete

- Step 2 (valve lift): inc 70, lift=5.87 mm of 10 mm (59%)
- Inc 61-66: inc size ramped up from 0.040 to 0.300 mm (solver gaining confidence)
- Inc 67: two unconverged attempts (4U, 4U) then converged on attempt 3 at 0.028 mm
  (contact event -- likely second group of coils beginning to bind)
- Inc 68-70: recovered, inc size growing again (0.042 -> 0.095 mm)
- Next milestone: kink2 at lift=7.67 mm (~1.8 mm ahead)

## 2026-06-14 16:24:52  --  Abaqus/Standard Step 2, Inc 75, lift~6.43 mm / 10 mm
**Status:** RUNNING -- 64% complete, active contact zone, cutbacks in progress

- Step 2 (valve lift): inc 75 in progress (last converged: inc 74 at lift=6.43 mm, 64%)
- Inc 71-72: smooth ramp-up to 0.21 mm steps
- Inc 73: 1U (32 SDIs -- heavy contact event), recovered on attempt 2 at 0.080 mm
- Inc 74: converged but 7 SDIs + 7 equil iters (14 total) -- coils actively binding
- Inc 75: 1U, 16 SDIs -- cutback in progress; solver working through contact zone
- Approaching kink2 region (lift=7.67 mm, ~1.24 mm ahead); expect continued cutbacks

## 2026-06-14 16:34:55  --  Abaqus/Standard Step 2, Inc 79, lift=6.60 mm / 10 mm
**Status:** RUNNING -- 66% complete, stepping carefully through bind zone

- Step 2 (valve lift): inc 79, lift=6.60 mm of 10 mm (66%)
- Inc 75 recovered (attempt 2 at 0.030 mm step after 16-SDI cutback)
- Inc 76-78: stable at 0.030 mm, 5-9 SDIs per increment (coils continuously binding)
- Inc 79: 35 SDIs + 9 equil iters = 44 total -- heaviest increment yet, but converged
- Step size holding at ~0.030-0.045 mm; solver in deepest contact zone
- Kink2 at lift=7.67 mm is 1.07 mm ahead (~24-35 more increments at current step size)
