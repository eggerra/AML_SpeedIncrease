import numpy as np
import plotly.graph_objects as go

# Parameters based on the spring model
L0 = 46.1
nt = 8.6
cyl_coils = 6.0
tap_coils = 2.6
R_bottom = 15.90 / 2 + 2.92 / 2  # Mean radius at bottom
R_top = 12.00 / 2 + 2.92 / 2     # Mean radius at top

# Generate helical path (wire representation)
n_points = 500
t = np.linspace(0, 1, n_points)
z = t * L0
theta = t * nt * 2 * np.pi

# Radius calculation (cylindrical then tapered)
r = np.zeros_like(t)
for i, ti in enumerate(t):
    coils_done = ti * nt
    if coils_done <= cyl_coils:
        r[i] = R_bottom
    else:
        # Linear taper for the remaining coils
        taper_frac = (coils_done - cyl_coils) / tap_coils
        r[i] = R_bottom + taper_frac * (R_top - R_bottom)

x = r * np.cos(theta)
y = r * np.sin(theta)

# Animation parameters for 1st Longitudinal Mode
# Mode 1 is an accordion motion: u_z(z) = A * sin(pi * z / (2 * L0)) for fixed-free
# but for a spring it's more like u_z = A * z/L0 * sin(omega*t) or similar.
# A realistic 1st mode for a fixed-base spring is displacement proportional to sin(pi*z/(2*L))
amplitude = 5.0  # Max displacement at top
frames = []
n_frames = 20
time_steps = np.linspace(0, 2 * np.pi, n_frames)

for ts in time_steps:
    # Scale factor for oscillation
    scale = np.sin(ts)
    # Displacement follows the first harmonic shape (fixed at z=0, max at z=L0)
    z_disp = scale * amplitude * np.sin((np.pi * z) / (2 * L0))
    
    frames.append(go.Frame(
        data=[go.Scatter3d(
            x=x, y=y, z=z + z_disp,
            mode='lines',
            line=dict(color='firebrick', width=6)
        )],
        name=f'frame_{ts}'
    ))

# Create the figure
fig = go.Figure(
    data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color='firebrick', width=6)
    )],
    layout=go.Layout(
        title="1st Longitudinal Eigenfrequency Animation (485.2 Hz)",
        scene=dict(
            xaxis=dict(range=[-15, 15]),
            yaxis=dict(range=[-15, 15]),
            zaxis=dict(range=[-5, 55]),
            aspectmode='cube'
        ),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}])]
        )]
    ),
    frames=frames
)

fig.show()
