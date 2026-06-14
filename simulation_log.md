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
