# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Run started:** 2026-06-16 09:26:50
**Job:** ValveSpring_oval_contact_abaqus

## Change applied
- **Free length increased**: L0=46.1mm → **L0=47.43mm** (+1.33mm)
- **Preload target**: 250N → **280N**  (ΔF=30N, k≈22.6N/mm, ΔL0=1.33mm)
- L_installed=36.1mm (unchanged), E=177500MPa, D_pitch=0.15 (unchanged)
- New s_preload=11.33mm (was 10.0mm), s_full_lift=21.33mm (was 20.0mm)

## Progress

## 2026-06-16 09:26:50  —  CAD generation
**Status:** RUNNING

## 2026-06-16 09:27:10  —  CAD generation
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval.step (2956 kB)

## 2026-06-16 09:27:10  —  Meshing
**Status:** RUNNING — Abaqus CAE noGUI 0.5 mm (may take 5-15 min)

---
### 2026-06-16 09:27

**Local job** (`ValveSpring_oval_contact_abaqus`) — FINISHED/STOPPED
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 39, step time 10.00/10.0 mm (100%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 09:29:30  —  Meshing
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_abq_mesh.inp (10 MB)

## 2026-06-16 09:29:30  —  FEA input
**Status:** RUNNING — writing Abaqus/CalculiX INP

## 2026-06-16 09:29:34  —  FEA input
**Status:** DONE — D:\Projects_AI\AML_SpeedIncrease\ValveSpring_oval_contact.inp (492 kB)

## 2026-06-16 09:29:34  —  Abaqus solve
**Status:** RUNNING — this typically takes 10-20 hours

---
### 2026-06-16 09:30

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): no increment data yet

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 09:34:58  —  Abaqus solve
**Status:** RUNNING — 8.4 h elapsed — Step 1 Inc 11  total=1.00 s  step=1.00 mm

## 2026-06-16 09:39:34  —  Abaqus solve
**Status:** RUNNING — 0.2 h elapsed — Step 1 Inc 17  total=2.00 s  step=2.00 mm

---
### 2026-06-16 09:40

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 1 (preload), Inc 19, step time 9.50/10.0 mm (95%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 09:45:05  —  Abaqus solve
**Status:** RUNNING — 8.6 h elapsed — Step 1 Inc 21  total=1.00 s  step=1.00 mm

## 2026-06-16 09:49:44  —  Abaqus solve
**Status:** RUNNING — 0.3 h elapsed — Step 1 Inc 25  total=1.00 s  step=3.00 mm

---
### 2026-06-16 09:50

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 1 (preload), Inc 26, step time 11.10/10.0 mm (100%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 09:55:17  —  Abaqus solve
**Status:** RUNNING — 8.8 h elapsed — Step 2 Inc 4  total=2.00 s  step=2.00 mm

## 2026-06-16 09:59:52  —  Abaqus solve
**Status:** RUNNING — 0.5 h elapsed — Step 2 Inc 9  total=2.00 s  step=3.00 mm

---
### 2026-06-16 10:00

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 9, step time 4.50/10.0 mm (45%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 10:05:27  —  Abaqus solve
**Status:** RUNNING — 8.9 h elapsed — Step 2 Inc 10  total=9.00 s  step=18.00 mm

## 2026-06-16 10:10:03  —  Abaqus solve
**Status:** RUNNING — 0.7 h elapsed — Step 2 Inc 12  total=2.00 s  step=2.00 mm

---
### 2026-06-16 10:10

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 12, step time 5.25/10.0 mm (52%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 10:15:38  —  Abaqus solve
**Status:** RUNNING — 9.1 h elapsed — Step 2 Inc 15  total=2.00 s  step=2.00 mm

## 2026-06-16 10:20:18  —  Abaqus solve
**Status:** RUNNING — 0.8 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

---
### 2026-06-16 10:20

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 17, step time 5.87/10.0 mm (59%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 10:25:48  —  Abaqus solve
**Status:** RUNNING — 9.3 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

## 2026-06-16 10:30:30  —  Abaqus solve
**Status:** RUNNING — 1.0 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

---
### 2026-06-16 10:30

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 17, step time 5.87/10.0 mm (59%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 10:36:01  —  Abaqus solve
**Status:** RUNNING — 9.4 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

## 2026-06-16 10:40:51  —  Abaqus solve
**Status:** RUNNING — 1.2 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

---
### 2026-06-16 10:40

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 17, step time 5.87/10.0 mm (59%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 10:46:24  —  Abaqus solve
**Status:** RUNNING — 9.6 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

---
### 2026-06-16 10:50

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 17, step time 5.87/10.0 mm (59%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 10:51:02  —  Abaqus solve
**Status:** RUNNING — 1.4 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

## 2026-06-16 10:56:34  —  Abaqus solve
**Status:** RUNNING — 9.8 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

---
### 2026-06-16 11:00

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 17, step time 5.87/10.0 mm (59%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 11:01:15  —  Abaqus solve
**Status:** RUNNING — 1.5 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

## 2026-06-16 11:06:58  —  Abaqus solve
**Status:** RUNNING — 10.0 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

---
### 2026-06-16 11:11

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 17, step time 5.87/10.0 mm (59%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet

## 2026-06-16 11:11:25  —  Abaqus solve
**Status:** RUNNING — 1.7 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

## 2026-06-16 11:17:08  —  Abaqus solve
**Status:** RUNNING — 10.1 h elapsed — Step 2 Inc 17  total=2.00 s  step=2.00 mm

---
### 2026-06-16 11:20

**Local job** (`ValveSpring_oval_contact_abaqus`) — RUNNING
  - Local (Win, 14 CPU): Step 2 (valve lift), Inc 17, step time 5.87/10.0 mm (59%)

**HPC job** (`279357.atgrzsl4803`) — UNKNOWN / NOT IN QUEUE
  - HPC fe6 (32 CPU, Abq2025HF4) — UNKNOWN / NOT IN QUEUE: no increment data yet
