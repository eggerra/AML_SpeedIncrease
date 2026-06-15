# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Run started:** 2026-06-16 01:07:37
**Job:** ValveSpring_oval_contact_abaqus

## Change applied
- Mesh: 0.5mm → **0.25mm** global seed (factor-2 refinement)
- Contact: EXPONENTIAL → **HARD PENALTY** (STABILIZE=0.0001)
- L0=46.1mm, L_installed=36.1mm, E=186000MPa, D_pitch=0.18 (unchanged)
- Reference (0.5mm hard): F(10mm)=262N, F(20mm)=671N

## Progress

## 2026-06-16 01:07:37  —  CAD generation
**Status:** RUNNING

## 2026-06-16 01:07:53  —  CAD generation
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval.step (2943 kB)

## 2026-06-16 01:07:53  —  Meshing
**Status:** RUNNING — Abaqus CAE noGUI 0.5 mm (may take 5-15 min)

---
### 2026-06-16 01:08

**Local job** (`ValveSpring_oval_contact_abaqus`) — FINISHED/STOPPED
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 39, step time 10.00/10.0 mm (100%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet
