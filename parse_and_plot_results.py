import re, glob, os, sys

# CalculiX .dat results from the run
# time=1.0 corresponds to 10mm displacement (full lift)
# Fz values extracted from FEMMesh.dat
ccx_data = [
    (0.10, 22.32),
    (0.20, 44.61),
    (0.35, 77.99),
    (0.575, 127.97),
    (0.9125, 202.70),
    (1.00, 222.04),
]

print("=== CalculiX FEA Results: Force vs. Valve Lift ===")
print(f"{'Time':>8} | {'Lift (mm)':>10} | {'Fz (N)':>10}")
print("-" * 38)
for t, fz in ccx_data:
    lift = t * 10.0
    print(f"{t:8.4f} | {lift:10.2f} | {fz:10.2f}")

print()
print(f"Spring rate (linear): {222.04/10.0:.1f} N/mm")
print(f"Drawing spec F1 at 10mm: 250 +/- 12 N")
print(f"FEA result at 10mm: 222.0 N  (note: no pre-load applied)")

# Plotly visualization
import plotly.graph_objects as go
from plotly.subplots import make_subplots

lifts = [t * 10.0 for t, _ in ccx_data]
forces = [fz for _, fz in ccx_data]

# Extrapolate to full 0-20mm range using the spring rate
k = 222.04 / 10.0  # N/mm from FEA
lifts_full = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
# Non-linear: use FEA data for 0-10mm, extrapolate with increasing rate for 10-20mm
forces_full = [0, 8.9, 17.8, 31.2, 51.2, 80.8, 127.97*10/3.5, 202.70*10/5.75, 222.04, 222.04*1.35, 222.04*1.8]
# Use actual FEA data points
forces_fea = [0] + [fz for t, fz in ccx_data if t * 10 in [2, 4, 6, 8, 10]]

# Build interpolated curve from actual CCX data
import numpy as np
t_arr = np.array([0] + [t for t, _ in ccx_data])
f_arr = np.array([0] + [fz for _, fz in ccx_data])
lift_arr = t_arr * 10.0

fig = make_subplots(rows=1, cols=2,
    subplot_titles=("Spring Force vs. Valve Lift (CalculiX FEA)", "Spring Rate vs. Valve Lift"),
    horizontal_spacing=0.12)

# Plot 1: Force vs Lift
fig.add_trace(go.Scatter(
    x=lift_arr, y=f_arr,
    mode='lines+markers',
    name='CalculiX FEA',
    line=dict(color='firebrick', width=3),
    marker=dict(size=9)
), row=1, col=1)

# Drawing spec points
fig.add_trace(go.Scatter(
    x=[10.0], y=[250.0],
    mode='markers',
    name='Drawing Spec F1=250N',
    marker=dict(color='royalblue', size=14, symbol='star'),
), row=1, col=1)

# Tolerance band
fig.add_trace(go.Scatter(
    x=[10.0, 10.0], y=[238.0, 262.0],
    mode='lines',
    name='Tolerance ±12N',
    line=dict(color='royalblue', width=2, dash='dash'),
), row=1, col=1)

# Plot 2: Spring rate (dF/dx)
rates = np.diff(f_arr) / np.diff(lift_arr)
lift_mid = (lift_arr[:-1] + lift_arr[1:]) / 2
fig.add_trace(go.Scatter(
    x=lift_mid, y=rates,
    mode='lines+markers',
    name='Spring Rate k (N/mm)',
    line=dict(color='green', width=3),
    marker=dict(size=9)
), row=1, col=2)

fig.update_xaxes(title_text="Valve Lift (mm)", row=1, col=1)
fig.update_yaxes(title_text="Spring Force (N)", row=1, col=1)
fig.update_xaxes(title_text="Valve Lift (mm)", row=1, col=2)
fig.update_yaxes(title_text="Spring Rate k (N/mm)", row=1, col=2)

fig.update_layout(
    title="Beehive Valve Spring - CalculiX FEA Results (A1770530500)",
    template='plotly_white',
    height=550,
    legend=dict(x=0.01, y=0.99)
)

fig.show()
print("Plot displayed.")
