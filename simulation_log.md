# Simulation Run Log — ValveSpring_oval_contact_abaqus (re-run 2026-06-14)

**Run started:** 2026-06-14  
**Job:** ValveSpring_oval_contact_abaqus  
**Status:** PIPELINE LAUNCHING

## Root Cause of Previous Run Failure

The previous run used `n_closed=2.026` (over-calibrated value) giving only 4.548 active
coils. With only 4.548 active coils the spring went solid at s≈14 mm during valve lift,
causing force to spike to 3400–5900 N (target F2=621 N at s=17.1 mm). Additionally the
contact exponential overclosure parameter c0=0.1 mm was too soft, causing 45 µm penetration
errors ("PENETRATION ERROR TOO LARGE") at every increment near coil binding.

## Fixes Applied

| Parameter | Previous | New | Reason |
|-----------|----------|-----|--------|
| `n_closed` | 2.026 | **1.25** | Drawing value; n_active 4.548→6.1 |
| `n_active` | 4.548 | **6.1** | Spring stays progressive through full lift |
| `D_pitch` | 0.0907 | **0.0776** | Kink1 kept at lift=4.05 mm (s=11.167 mm) |
| `p_bot` (ellipse) | 5.375 mm | **4.750 mm** | Bottom gap 2.455→1.830 mm |
| `L0_oval` | 39.471 mm | **39.182 mm** | h_active=31.417+2×1.25×3.106 |
| Contact c0 | 0.1 mm | **0.01 mm** | 10× tighter, eliminates penetration errors |
| E_MOD | 273131 MPa | **273131 MPa** | Retained (LMAX=1.0 mm mesh correction) |

## Expected Results

- Phase 1 (pre-kink): k_FEA_estimate ≈ 34 N/mm (target 34.7 N/mm, ~2% under)
- F1 at preload (s=7.58 mm): ≈ 249 N ✓
- Kink1 at lift=4.05 mm: F≈390 N ✓
- Kink2 at lift=7.67 mm: F≈525 N ✓  
- F2 at full lift (s=17.58 mm): ≈ 621 N ✓
- Spring solid length: s_solid ≈ 20.2 mm > s_full_lift=17.58 mm ✓ (no premature closing)

## Pipeline Progress

