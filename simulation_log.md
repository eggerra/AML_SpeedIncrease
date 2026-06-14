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

## 2026-06-14 16:44:51  --  Abaqus/Standard Step 2, Inc 88, lift=6.87 mm / 10 mm
**Status:** RUNNING -- 69% complete, grinding through dense bind zone

- Step 2 (valve lift): inc 88, lift=6.87 mm of 10 mm (69%)
- Inc 80-88: all converged in 1 attempt; step sizes 0.021-0.045 mm (fine stepping)
- SDI counts per inc: 14, 11, 9, 7, 9, 6, 4, 5, 8 -- decreasing trend, contact stabilising
- No cutbacks since inc 75; solver working steadily
- Kink2 at lift=7.67 mm is 0.80 mm ahead (~25-38 more increments at current rate)

## 2026-06-14 16:54:50  --  Abaqus/Standard Step 2, Inc 99, lift=7.14 mm / 10 mm
**Status:** RUNNING -- 71% complete, steady progress toward kink2

- Step 2 (valve lift): inc 99, lift=7.14 mm of 10 mm (71%)
- Inc 89-99: all 1 attempt, no cutbacks; step sizes 0.018-0.041 mm
- SDI counts low (2-5) and stable -- coil contact pattern settled
- Equil iters 3-6 per increment -- healthy convergence
- Kink2 at lift=7.67 mm is 0.53 mm ahead (~15-30 more increments)

## 2026-06-14 17:04:51  --  Abaqus/Standard Step 2, Inc 104, lift=7.44 mm / 10 mm
**Status:** RUNNING -- 74% complete, approaching kink2

- Step 2 (valve lift): inc 104, lift=7.44 mm of 10 mm (74%)
- Inc 100-103: step sizes ramping up (0.023->0.077 mm) as contact stabilises
- Inc 104: 32 SDIs + 3 equil iters = 35 total (new contact event), still 1 attempt
- Kink2 at lift=7.67 mm is only 0.23 mm ahead -- entering second major bind zone
- High SDI count at inc 104 likely signals start of next coil group binding

## 2026-06-14 17:14:53  --  Abaqus/Standard Step 2, Inc 109, lift~7.77 mm / 10 mm
**Status:** RUNNING -- 78% complete, past kink2, cutback in progress

- Step 2 (valve lift): last converged inc 108 at lift=7.77 mm (78%); inc 109 cutting back
- Kink2 (lift=7.67 mm) crossed between inc 106 and 107
- Inc 104-108 progression through kink2 zone (SDIs: 32, 29, 23, 14, 15 -- decreasing)
- Inc 107: lift=7.70 mm (just past kink2=7.67 mm); rate now 40.9 N/mm
- Inc 109: 1U, 7 SDIs -- Abaqus cutting back; still 2.23 mm of lift remaining
- Phase 3 (highest stiffness) now active; remaining lift to full stroke is 2.23 mm

## 2026-06-14 17:24:51  --  Abaqus/Standard Step 2, Inc 120, lift=8.11 mm / 10 mm
**Status:** RUNNING -- 81% complete, Phase 3 proceeding smoothly

- Step 2 (valve lift): inc 120, lift=8.11 mm of 10 mm (81%)
- Inc 109 cutback recovered (attempt 2 at 0.012 mm); inc 110-120 all clean 1 attempt
- Step sizes recovering: 0.012 -> 0.070 mm as Phase 3 contact stabilises
- SDI counts low and stable (3-10 per inc); equil iters 0-5 -- healthy convergence
- 1.89 mm remaining to full lift (10 mm); no further cutbacks since inc 109

## 2026-06-14 17:34:53  --  Abaqus/Standard Step 2, Inc 125, lift=8.59 mm / 10 mm
**Status:** RUNNING -- 86% complete, accelerating toward full lift

- Step 2 (valve lift): inc 125, lift=8.59 mm of 10 mm (86%)
- Inc 120-125: all 1 attempt, no cutbacks; step sizes growing (0.052->0.176 mm)
- SDI counts rising again: 7, 10, 11, 12, 17, 27 -- new coil contact events in Phase 3
- Still converging in 1 attempt despite 27 SDIs at inc 125 -- solver handling well
- 1.41 mm remaining to full lift (10 mm); ~8-15 more increments at current rate

## 2026-06-14 17:44:54  --  Abaqus/Standard Step 2, Inc 133, lift=9.14 mm / 10 mm
**Status:** RUNNING -- 91% complete, final approach to full lift

- Step 2 (valve lift): inc 133, lift=9.14 mm of 10 mm (91%)
- Inc 126: 29 SDIs, 0.264 mm step (large); inc 127: cutback (1U), recovered at 0.049 mm
- Inc 128-133: stable recovery, step sizes 0.037-0.056 mm, SDIs 2-7 -- settling
- Only 0.86 mm remaining to full lift (10 mm); ~15-23 more increments at current rate
- No further issues expected; spring approaching full compression state

## 2026-06-14 17:54:51  --  Abaqus/Standard Step 2, Inc 138, lift=9.38 mm / 10 mm
**Status:** RUNNING -- 94% complete, final increments

- Step 2 (valve lift): inc 138, lift=9.38 mm of 10 mm (94%)
- Inc 134-138: all 1 attempt, no cutbacks; step sizes 0.042-0.063 mm
- SDI counts rising again (6, 13, 18, 16, 19) -- last coil contacts engaging near full lift
- All converging cleanly; equil iters 1-4 per increment
- Only 0.62 mm remaining to full lift (10 mm); ~10-15 more increments to completion

## 2026-06-14 18:04:53  --  Abaqus/Standard Step 2, Inc 143, lift=9.58 mm / 10 mm
**Status:** RUNNING -- 96% complete, two-cutback event at inc 141, now recovered

- Step 2 (valve lift): inc 143, lift=9.58 mm of 10 mm (96%)
- Inc 139-140: clean, step sizes growing (0.070->0.106 mm), SDIs 25-26
- Inc 141: two unconverged attempts (1U, 2U) before converging on attempt 3 at 0.005 mm
  -- hardest convergence event since inc 67; likely final coil group seating
- Inc 142-143: recovered at 0.005-0.007 mm, 1-2 SDIs, 4 equil iters -- stable
- Only 0.42 mm remaining; step size now very small -- ~55-85 more increments to finish

## 2026-06-14 18:14:53  --  Abaqus/Standard Step 2, Inc 152, lift=9.72 mm / 10 mm
**Status:** RUNNING -- 97% complete, final 0.28 mm

- Step 2 (valve lift): inc 152, lift=9.72 mm of 10 mm (97%)
- Inc 143-146: step sizes recovering (0.007->0.025 mm); inc 147: another cutback
- Inc 147: 1U then converged on attempt 2 at 0.009 mm
- Inc 148-152: stable at 0.010-0.021 mm, SDIs 5-11, all 1 attempt
- 0.28 mm remaining at ~0.010-0.021 mm steps; ~13-28 increments to full lift (10 mm)

## 2026-06-14 18:24:50  --  Abaqus/Standard Step 2, Inc 157, lift=9.81 mm / 10 mm
**Status:** RUNNING -- 98% complete, 0.19 mm to full lift

- Step 2 (valve lift): inc 157, lift=9.81 mm of 10 mm (98%)
- Inc 153-157: all 1 attempt, no cutbacks; step sizes 0.011-0.027 mm
- SDIs fluctuating (4, 12, 17, 8, 14) but all converging cleanly
- 0.19 mm remaining; ~7-17 increments to completion at current step sizes

## 2026-06-14 18:34:53  --  Abaqus/Standard Step 2, Inc 169, lift=9.87 mm / 10 mm
**Status:** RUNNING -- 99% complete, 0.13 mm to full lift

- Step 2 (valve lift): inc 169, lift=9.87 mm of 10 mm (99%)
- Inc 159: cutback (1U), recovered on attempt 2 at 0.0028 mm
- Inc 160-169: stable at 0.0028-0.0095 mm; step sizes slowly growing again
- SDIs 1-8, equil iters 0-6 -- converging cleanly
- 0.13 mm remaining; ~14-46 increments to finish at current rate

## 2026-06-14 18:44:52  --  Abaqus/Standard Step 2, Inc 172, lift=9.88 mm / 10 mm
**Status:** RUNNING -- 99% complete, 0.12 mm remaining, frequent small cutbacks

- Step 2 (valve lift): inc 172 (attempt 2), lift=9.88 mm of 10 mm (99%)
- Inc 170: cutback (1U, 7 SDIs), recovered at 0.0036 mm
- Inc 172: another cutback (1U, 13 SDIs), recovered at 0.0020 mm
- Step sizes oscillating 0.002-0.014 mm as final coil contacts seat
- 0.12 mm remaining; solver grinding through very tight contact at near-full compression

## 2026-06-14 18:54:52  --  Abaqus/Standard Step 2, Inc 175, lift=9.89 mm / 10 mm
**Status:** RUNNING -- 99% complete, 0.11 mm remaining, very small steps

- Step 2 (valve lift): inc 175, lift=9.89 mm of 10 mm (99%)
- Inc 173-175: clean 1-attempt, SDIs 1, 1, 8; step sizes 0.002-0.003 mm
- Only advanced 0.01 mm since last update (10 increments) -- very fine stepping
- 0.11 mm remaining; at 0.002-0.003 mm steps ~37-55 more increments to finish
- Convergence healthy; solver locked into tiny steps due to dense coil contact

## 2026-06-14 19:05:47  --  Abaqus/Standard Step 2, Inc 175+, lift~9.89 mm / 10 mm
**Status:** RUNNING -- .sta stalled 14 min; solver actively iterating on next increment

- Last .sta entry: inc 175, lift=9.89 mm (99%), step size 0.003 mm (18:50)
- .msg confirms Abaqus RUNNING: working on eq. iteration 12 of next increment
  - 149,091 equations, 4 threads, 5.6s per matrix factorisation
  - Scaled residual force: 0.162 (target ~0.005) -- not yet converged
  - Max contact penetration: 40 um -- normal, within tolerance
  - Contact constraints: CONVERGED; force equilibrium still iterating
- Solver not stuck; dense contact at near-full lift requires many iterations
- 0.11 mm remaining to full lift (10 mm)

## 2026-06-14 19:15:16  --  Abaqus/Standard Step 2, Inc 177, lift=9.89 mm / 10 mm
**Status:** RUNNING -- 2 new increments since last update; working on inc 178

- Step 2: inc 177 last completed (9.89 mm lift, 99%); inc 178 iterating now
- Inc 176: 33 SDIs + 12 equil iters = 45 total (hardest since inc 105); converged 1 attempt
- Inc 177: 9 SDIs + 10 equil iters = 19 total; step size 0.0045 mm, converged
- .msg (live): inc 178 iterating -- penetration error 12.9 um, scaled residual -1.94
  (not yet converged; contact force error TOO LARGE warning -- normal near full bind)
- Solver active: 4 threads, 6.2s/factorisation, 149k equations
- ~0.11 mm still remaining at ~0.0045 mm steps; ~24 more increments estimated
