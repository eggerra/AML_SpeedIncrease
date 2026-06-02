import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Parameters based on the spring model
L0 = 46.1
nt = 8.6
cyl_coils = 6.0
tap_coils = 2.6
R_bottom = (15.90 + 2.92) / 2
R_top = (12.00 + 2.92) / 2

# Generate helical path (wire representation)
n_points = 600
t_path = np.linspace(0, 1, n_points)
theta = t_path * nt * 2 * np.pi

# Radius calculation (cylindrical then tapered)
r_base = np.where(t_path * nt <= cyl_coils, R_bottom, 
                  R_bottom + ((t_path * nt - cyl_coils) / tap_coils) * (R_top - R_bottom))

# Animation parameters
n_frames = 30
time_steps = np.linspace(0, 1, n_frames)

# Setup subplots (1 row, 2 columns)
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}]],
    subplot_titles=("1st Eigenfrequency (485.2 Hz)", "Valve Compression (0-20 mm)")
)

# Initial traces
fig.add_trace(
    go.Scatter3d(x=r_base * np.cos(theta), y=r_base * np.sin(theta), z=t_path * L0,
                 mode='lines', line=dict(color='firebrick', width=6)),
    row=1, col=1
)
fig.add_trace(
    go.Scatter3d(x=r_base * np.cos(theta), y=r_base * np.sin(theta), z=t_path * L0,
                 mode='lines', line=dict(color='royalblue', width=6)),
    row=1, col=2
)

# Create Frames
frames = []
for i in range(n_frames):
    # Phase for oscillation (Subplot 1)
    phase = 2 * np.pi * time_steps[i]
    z_osc = t_path * L0 + np.sin(phase) * 5.0 * np.sin((np.pi * t_path * L0) / (2 * L0))
    
    # Lift for compression (Subplot 2)
    # We compress from L0 down to L0-20mm
    lift = 20.0 * (0.5 - 0.5 * np.cos(phase)) # Smooth back and forth
    z_comp = t_path * (L0 - lift)
    
    frames.append(go.Frame(
        data=[
            go.Scatter3d(z=z_osc), # Subplot 1
            go.Scatter3d(z=z_comp)  # Subplot 2
        ],
        name=f"frame_{i}",
        traces=[0, 1]
    ))

# Layout updates
fig.update_layout(
    title="Spring Dynamics: Modal Vibration vs. Operational Compression",
    scene=dict(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), zaxis=dict(range=[-5, 55]), aspectmode='cube'),
    scene2=dict(xaxis=dict(range=[-15, 15]), yaxis=dict(range=[-15, 15]), zaxis=dict(range=[-5, 55]), aspectmode='cube'),
    updatemenus=[dict(
        type="buttons",
        buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 40, "redraw": True}}])]
    )]
)

fig.frames = frames
fig.show()
