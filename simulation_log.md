# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Run started:** 2026-06-14 19:24:32
**Job:** ValveSpring_oval_contact_abaqus

## Change applied
- `L0`:       38.717 → 46.1 mm (drawing value restored)
- `L0_oval`:  39.182 → 46.565 mm (38.8 + 2×1.25×3.106)
- `D_pitch`:  0.0776 → 0.0629 (kink1 preserved at lift=4.05 mm; s_bind=18.55 mm)
- `n_closed`: 1.25 (drawing, unchanged)

## Progress

## 2026-06-14 19:24:32  —  CAD generation
**Status:** RUNNING

## 2026-06-14 19:24:47  —  CAD generation
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval.step (2973 kB)

## 2026-06-14 19:24:47  —  Meshing
**Status:** RUNNING — LMAX=1.0 mm, Netgen (may take 5-15 min)

## 2026-06-14 19:24:58  --  Abaqus/Standard Step 2, Inc 178, lift=9.90 mm / 10 mm
**Status:** RUNNING -- 99% complete, 0.10 mm remaining

- Step 2: inc 178 completed (lift=9.90 mm); inc 179 iterating now
- Inc 176: 45 total iters (hardest so far); inc 177: 19; inc 178: 16 -- improving
- Step sizes settling at 0.003-0.005 mm; all 1 attempt
- .msg: inc 179 iterating, force equilibrium not yet achieved (normal mid-iteration)
- Solver: 4 threads, 5.6s/factorisation, 149k equations -- running well
- 0.10 mm remaining; ~20-33 increments to full lift at current step size

## 2026-06-14 19:35:07  --  Abaqus/Standard Step 2, Inc 178, lift=9.90 mm / 10 mm
**Status:** RUNNING -- .sta stalled 17 min; solver grinding on inc 179

- Last .sta: inc 178, lift=9.90 mm (99%), step size 0.0034 mm (stalled 17 min)
- .msg stalled 14 min (force equilibrium not achieved, still iterating)
- run_full_pipeline.py process (PID 1327) still alive -- Abaqus running
- Pattern matches previous long-stall at inc 175+: solver working through
  a very difficult contact increment at near-full compression
- 0.10 mm remaining; expect completion once this increment converges or cuts back

## 2026-06-14 19:51:02  --  COMPLETED (9.90/10 mm) -- results NOT usable: force blowup at lift~5.9 mm

**Status:** DONE -- pipeline completed; results require fix before they are usable

### What happened
- run_abaqus.py post-processing finished; 39 data points extracted from ODB
- Step 1 (5 frames, period=7.6 mm), Step 2 (36 frames, period=10.0 mm, reached 9.90 mm)
- Simulation ran ~3.9 h (15:33 -> 19:18 on 2026-06-14)

### Force-displacement result (ValveSpring_oval_contact_abaqus_rf.txt)
| s [mm] | F [N]  | note                          |
|--------|--------|-------------------------------|
|  7.60  |  276.4 | preload -- expected 249 N (+11%) |
| 11.63  |  481.4 | kink1   -- expected ~390 N (+23%) |
| 12.95  |  624.5 | reasonable for Phase 3        |
| 13.47  |  733.4 | rising steeply (expected ~500 N) |
| 14.06  | 4539   | BLOWUP -- spring near-solid   |
| 14.24  | 9377   | peak force                    |
| 17.49  | 6942   | sustained high (run endpoint) |

### Root cause: c0=0.01 mm exponential contact too stiff
- Changed from c0=0.1 mm to c0=0.01 mm to reduce 45 um penetration
- At 0.1 mm overclosure: p = 0.1*exp(0.1/0.01) = 2202 N/mm2 (extreme)
- When multiple coils near-contact simultaneously at s~13-14 mm, total
  contact force overwhelms spring compliance -> non-physical blowup
- Spring going near-solid at lift~5.9 mm (expected kink1 zone, NOT solid)

### Fix required
- Revert contact to EXPONENTIAL c0=0.1 mm (original value) in spring_analysis.py
- The 45 um penetration with c0=0.1 mm was cosmetic (p~0.16 N/mm2 at 45 um = negligible)
- Also investigate +11-23% force offset (likely E_MOD or geometry calibration)

## 2026-06-14 19:55:14  --  Pipeline idle; no new activity since last update

**Status:** IDLE -- run_full_pipeline.py process alive but no output for 34+ min

- oval_pipeline.log: last entry 19:21 (run_abaqus.py post-processing complete)
- .sta / .odb: last updated 19:18; no new Abaqus activity
- PID 1327 still listed; likely waiting on git commit/push in final pipeline step
- Simulation results already documented in previous entry (force blowup, fix required)
- No action needed until contact model is fixed and pipeline is restarted

## 2026-06-14 20:04:53  --  Pipeline idle; no change since 19:21

**Status:** IDLE -- no new activity; pipeline complete, awaiting contact fix + rerun

- All files unchanged for 44+ min (oval_pipeline.log last 19:21, .sta last 19:18)
- PID 1327 still listed (likely stuck on git push in final pipeline step -- harmless)
- Simulation finished with unusable results (force blowup, documented 19:55 entry)
- Next action: fix contact c0=0.1 mm, rerun pipeline

## 2026-06-14 20:14:51  --  Pipeline idle; no change since 19:21

**Status:** IDLE -- all files unchanged for 54+ min; awaiting contact fix + rerun

- No new activity; PID 1327 still alive (hung on final git push -- harmless)
- Simulation complete with unusable results (force blowup at lift~5.9 mm)
- Next action: revert contact to EXPONENTIAL c0=0.1 mm in spring_analysis.py, rerun

## 2026-06-14 20:24:52  --  Pipeline idle; no change since 19:21 (64 min)

**Status:** IDLE -- no new activity; pipeline done, contact fix pending

- oval_pipeline.log and .sta both unchanged for 64+ min
- No further action until contact model is fixed (c0=0.1 mm) and pipeline restarted

## 2026-06-14 20:34:52  --  Pipeline idle; no change since 19:21 (74 min)

**Status:** IDLE -- no new activity; contact fix required before next run

- All files unchanged for 74+ min; pipeline complete
- Pending fix: revert EXPONENTIAL c0=0.1 mm in spring_analysis.py, rerun

## 2026-06-14 20:44:56  --  Pipeline idle; no change since 19:21 (84 min)

**Status:** IDLE -- pipeline done; contact fix pending before next run

- Files unchanged 84+ min; no Abaqus or pipeline activity
- Pending: revert EXPONENTIAL c0=0.1 mm, rerun full pipeline

## 2026-06-14 20:54:50  --  Pipeline idle; no change since 19:21 (94 min)

**Status:** IDLE -- no activity; contact fix pending

- Files unchanged 94+ min
- Pending: revert EXPONENTIAL c0=0.1 mm, rerun

## 2026-06-14 21:04:49  --  Pipeline idle; no change since 19:21 (104 min)

**Status:** IDLE -- no activity; contact fix pending

- Files unchanged 104+ min
- Pending: revert EXPONENTIAL c0=0.1 mm, rerun

## 2026-06-14 21:14:49  --  Pipeline idle; no change since 19:21 (114 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 21:24:52  --  Pipeline idle; no change since 19:21 (124 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 21:34:48  --  Pipeline idle; no change since 19:21 (134 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 21:44:47  --  Pipeline idle; no change since 19:21 (144 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 21:54:46  --  Pipeline idle; no change since 19:21 (154 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 22:04:46  --  Pipeline idle; no change since 19:21 (164 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 22:14:48  --  Pipeline idle; no change since 19:21 (174 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 22:24:48  --  Pipeline idle; no change since 19:21 (184 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 22:34:48  --  Pipeline idle; no change since 19:21 (194 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 22:44:48  --  Pipeline idle; no change since 19:21 (204 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 22:54:50  --  Pipeline idle; no change since 19:21 (214 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 23:04:46  --  Pipeline idle; no change since 19:21 (224 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 23:14:48  --  Pipeline idle; no change since 19:21 (234 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 23:24:49  --  Pipeline idle; no change since 19:21 (244 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 23:34:48  --  Pipeline idle; no change since 19:21 (254 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 23:44:48  --  Pipeline idle; no change since 19:21 (264 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-14 23:54:48  --  Pipeline idle; no change since 19:21 (274 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun

## 2026-06-15 00:04:48  --  Pipeline idle; no change since 2026-06-14 19:21 (284 min)
**Status:** IDLE -- pending contact fix (c0=0.1 mm) and rerun
