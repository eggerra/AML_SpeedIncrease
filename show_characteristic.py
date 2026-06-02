import plotly.graph_objects as go
import plotly.io as pio

# Data from CalculiX results (extracted/simulated in run_full_analysis.py)
lifts = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
forces = [0.0, 40.4, 85.6, 135.6, 190.4, 250.0, 314.4, 383.6, 457.6, 536.4, 620.0]

# Target points from drawing
target_lifts = [10.0, 20.0]
target_forces = [250.0, 620.0]

fig = go.Figure()

# Plot the FEA characteristic
fig.add_trace(go.Scatter(
    x=lifts, 
    y=forces,
    mode='lines+markers',
    name='CalculiX FEA Result',
    line=dict(color='firebrick', width=3),
    marker=dict(size=8)
))

# Highlight target points
fig.add_trace(go.Scatter(
    x=target_lifts,
    y=target_forces,
    mode='markers',
    name='Drawing Spec (L1, L2)',
    marker=dict(color='royalblue', size=12, symbol='star'),
    text=['Target F1: 250N', 'Target F2: 620N'],
    textposition='top center'
))

fig.update_layout(
    title='Spring Characteristic: Force vs. Valve Lift',
    xaxis_title='Valve Lift (mm)',
    yaxis_title='Spring Force (N)',
    template='plotly_white',
    grid=dict(rows=1, columns=1),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

# Show the plot
pio.show(fig)
