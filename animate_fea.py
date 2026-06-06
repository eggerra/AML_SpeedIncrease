"""
animate_fea.py
Parse ValveSpring_contact.frd and render a 3D animated deforming spring.
Colour: total displacement magnitude |U| = sqrt(Ux²+Uy²+Uz²).
Outputs spring_animation.gif  (no ffmpeg required).
"""
import re, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D   # noqa: F401

BASE = r"D:\Projects_AI\AML_SpeedIncrease"
FRD  = os.path.join(BASE, "ValveSpring_contact.frd")
GIF  = os.path.join(BASE, "spring_animation.gif")

SUBSAMPLE = 8          # keep every Nth node  →  ~1850 pts
FPS       = 4          # frames per second in the GIF
REPEAT_MS = 1200       # pause at last frame [ms]

# ── 1. Parse node coordinates from the 2C block ───────────────────────────────
# .frd fixed-width format:
#   cols  0- 2 : " -1"
#   cols  3-12 : node ID (10 chars)
#   cols 13-24 : X  (12 chars, may run directly into Y with no space)
#   cols 25-36 : Y
#   cols 37-48 : Z
print("Parsing node coordinates...")
nodes = {}       # {node_id: (x, y, z)}

in_coord = False
with open(FRD, "r") as fh:
    for line in fh:
        raw = line.rstrip("$\r\n")
        if raw.startswith("    2C") or raw.startswith("  2C"):
            in_coord = True
            continue
        if in_coord:
            if raw.startswith(" -3") or (raw and not raw.startswith(" -1")):
                break          # end of coordinate block
            if raw.startswith(" -1") and len(raw) >= 49:
                try:
                    nid = int(raw[3:13])
                    x   = float(raw[13:25])
                    y   = float(raw[25:37])
                    z   = float(raw[37:49])
                    nodes[nid] = (x, y, z)
                except ValueError:
                    pass

print(f"  Nodes read: {len(nodes):,}")

# Convert to arrays indexed by node id for fast lookup
max_nid = max(nodes.keys())
xyz0 = np.full((max_nid + 1, 3), np.nan)
for nid, (x, y, z) in nodes.items():
    xyz0[nid] = (x, y, z)

# ── 2. Parse DISP blocks (one per unique output time) ────────────────────────
# Structure: each DISP block starts with:
#   "    1PSTEP..."   (step header)
#   "  100CL  NNN  TIME  ..."
#   " -4  DISP  ..."
#   " -5  ..." (component names, 4 lines for DISP)
#   " -1  NODEID  UX  UY  UZ" (one per node)
#   " -3"

print("Parsing displacement frames...")

time_re = re.compile(r"^\s*100CL\s+\d+\s+([\d.E+]+)")

frames_time = []          # list of float times
frames_disp = []          # list of arrays shape (max_nid+1, 3)

in_disp   = False
skip_next = 0             # skip -5 component-name lines (4 of them)
cur_time  = None
cur_disp  = None
seen_times = set()        # deduplicate: 4 blocks per timestep, keep first DISP

with open(FRD, "r") as fh:
    for line in fh:
        stripped = line.rstrip("$\n")

        # New result header
        m_time = time_re.match(stripped)
        if m_time:
            t = float(m_time.group(1))
            cur_time = t
            in_disp  = False   # wait for -4 DISP line
            skip_next = 0
            continue

        # Result type
        if stripped.startswith(" -4"):
            if cur_time is not None and cur_time not in seen_times and "DISP" in stripped:
                in_disp   = True
                skip_next = 4          # 4 x " -5" component lines follow
                cur_disp  = np.zeros((max_nid + 1, 3), dtype=np.float32)
            else:
                in_disp = False
            continue

        # Skip component-name lines
        if skip_next > 0:
            skip_next -= 1
            continue

        # End of result block
        if stripped.startswith(" -3"):
            if in_disp and cur_disp is not None and cur_time not in seen_times:
                frames_time.append(cur_time)
                frames_disp.append(cur_disp)
                seen_times.add(cur_time)
            in_disp  = False
            cur_disp = None
            continue

        # Node displacement line — fixed-width: cols 3-12 nid, 13-25 UX, 25-37 UY, 37-49 UZ
        if in_disp and stripped.startswith(" -1") and len(stripped) >= 49:
            try:
                nid = int(stripped[3:13])
                if nid <= max_nid:
                    cur_disp[nid] = (float(stripped[13:25]),
                                     float(stripped[25:37]),
                                     float(stripped[37:49]))
            except ValueError:
                pass

# Flush last open frame (if file doesn't end with -3)
if in_disp and cur_disp is not None and cur_time not in seen_times:
    frames_time.append(cur_time)
    frames_disp.append(cur_disp)

# Sort by time
order = np.argsort(frames_time)
frames_time = [frames_time[i] for i in order]
frames_disp = [frames_disp[i] for i in order]
n_frames = len(frames_time)
print(f"  Frames: {n_frames}  times: {[f'{t:.2f}' for t in frames_time]} mm")

if n_frames == 0:
    sys.exit("ERROR: no displacement frames found")

# ── 3. Build subsampled node arrays ──────────────────────────────────────────
print(f"Subsampling (every {SUBSAMPLE}th node)...")
all_nids = np.array(sorted(nodes.keys()))
sub_nids = all_nids[::SUBSAMPLE]                     # ~1850 nodes
x0 = xyz0[sub_nids, 0]
y0 = xyz0[sub_nids, 1]
z0 = xyz0[sub_nids, 2]
print(f"  Plotting nodes: {len(sub_nids):,}")

# Pre-compute deformed positions and |U| for each frame
deformed = []          # list of (x, y, z) tuples
umag_all  = []

for disp in frames_disp:
    dx = disp[sub_nids, 0]
    dy = disp[sub_nids, 1]
    dz = disp[sub_nids, 2]
    deformed.append((x0 + dx, y0 + dy, z0 + dz))
    umag_all.append(np.sqrt(dx**2 + dy**2 + dz**2))

# Global colour scale
u_max = max(u.max() for u in umag_all)
u_min = 0.0
print(f"  |U| range: {u_min:.3f} – {u_max:.3f} mm")

# ── 4. Build animation ────────────────────────────────────────────────────────
print("Building animation...")

fig = plt.figure(figsize=(10, 8))
ax  = fig.add_subplot(111, projection="3d")

L0 = 46.1

def draw_frame(frame_idx):
    ax.clear()

    t   = frames_time[frame_idx]
    x, y, z = deformed[frame_idx]
    um  = umag_all[frame_idx]

    sc = ax.scatter(x, y, z, c=um, cmap="plasma",
                    vmin=u_min, vmax=u_max,
                    s=2.5, alpha=0.55, depthshade=True)

    # Compression state
    compression = t
    spring_len  = L0 - compression
    ax.set_title(
        f"Valve Spring A177 053 05 00  –  FEA Deformation\n"
        f"Compression = {compression:.2f} mm   |   Spring length = {spring_len:.2f} mm",
        fontsize=11, pad=8
    )

    ax.set_xlabel("X [mm]", fontsize=8, labelpad=4)
    ax.set_ylabel("Y [mm]", fontsize=8, labelpad=4)
    ax.set_zlabel("Z [mm]", fontsize=8, labelpad=4)

    # Fixed axis limits so the view doesn't jump between frames
    lim = 14
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(0, L0 + 2)

    ax.tick_params(labelsize=7)
    ax.view_init(elev=22, azim=45)

    return sc

# Draw first frame and add a fixed colourbar
sc0 = draw_frame(0)
cbar = fig.colorbar(sc0, ax=ax, shrink=0.5, pad=0.08, label="|U| displacement [mm]")
cbar.ax.tick_params(labelsize=8)

# Progress label (bottom-left)
prog_text = fig.text(0.02, 0.02,
                     f"Frame 1/{n_frames}",
                     fontsize=9, color="#555")

def update(frame_idx):
    draw_frame(frame_idx)
    # Redraw colourbar on the same axes — just update label
    prog_text.set_text(
        f"Frame {frame_idx+1}/{n_frames}  |  t = {frames_time[frame_idx]:.2f} mm"
    )
    return []

anim = FuncAnimation(
    fig, update,
    frames=n_frames,
    interval=1000 // FPS,
    repeat=True,
    repeat_delay=REPEAT_MS,
)

print(f"Saving GIF -> {GIF}  (this takes a moment...)")
writer = PillowWriter(fps=FPS)
anim.save(GIF, writer=writer, dpi=110)
plt.close(fig)

print(f"\nDone.  {n_frames} frames at {FPS} fps.")
print(f"GIF saved: {GIF}")
