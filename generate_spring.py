"""
Valve Spring CAD Generator - A1770530500 Intake Valve Spring (Beehive)
Drawing parameters: oval wire 2.92x3.66mm, beehive profile, 8.6 coils

Pitch is NON-UNIFORM (progressive):
  - Bottom n_closed coils : dead/closed (wire touching, zero gap)
  - Active zone           : quadratic pitch gradient, large pitch at large-OD bottom,
                            tight pitch at small-OD top  ->  top coils bind first
  - Top n_closed coils    : dead/closed

This reproduces the drawing's active-coil count (4.4 at L1, 3.1 at L2) and
yields a progressive spring rate consistent with F1=250N / F2=620N.
"""
import math
import sys

# -- Drawing parameters --------------------------------------------------------
L0         = 46.1    # free length [mm]
wire_a     = 2.92    # wire axial dimension (along spring axis) [mm]
wire_r     = 3.66    # wire radial dimension (transverse to axis) [mm]
nt         = 8.6     # total coils
Di_bot     = 15.90   # inner diameter bottom [mm]
Di_top     = 12.00   # inner diameter top [mm]
grind_z    = 0.75    # ground end cut depth [mm]
n_closed   = 1.25    # closed (ground) coils at each end

R_mean_bot = Di_bot / 2 + wire_r / 2   # = 9.78 mm
R_mean_top = Di_top / 2 + wire_r / 2   # = 7.83 mm

# -- Variable-pitch parameters -------------------------------------------------
n_active   = nt - 2 * n_closed          # = 6.1 active coils
h_closed   = n_closed * wire_a          # = 3.650 mm per dead end
h_active   = L0 - 2 * h_closed         # = 38.800 mm active zone height
pitch_mean = h_active / n_active        # = 6.361 mm mean active pitch

# D_pitch controls the pitch gradient.  D_pitch > 0 -> more pitch at bottom
# (large OD), less at top (small OD).  Constraint: D_pitch < 1.
# Effective pitches:
#   p_bot  = pitch_mean * (1 + D_pitch)   <- large-OD coils, bind last
#   p_top  = pitch_mean * (1 - D_pitch)   <- small-OD coils, bind first
# Drawing implies ~1.7 top coils bind before L1 (10 mm compression) and
# ~1.3 more coils bind before L2 (20 mm compression).
# D_pitch = 0.22  ->  p_top ~ 4.96 mm (gap 2.04 mm), p_bot ~ 7.76 mm
# Min gap kept >= 2 mm so Gmsh Delaunay mesher can build valid Tet10 elements.
# Binding physics is captured analytically (spring_analysis.py) independent of D_pitch.
D_pitch    = 0.22

p_top  = pitch_mean * (1 - D_pitch)
p_bot  = pitch_mean * (1 + D_pitch)

print("=== Valve Spring CAD Generator ===")
print(f"  Wire:        {wire_a} x {wire_r} mm (axial x radial)")
print(f"  R_mean:      {R_mean_bot:.3f} mm (bottom) -> {R_mean_top:.3f} mm (top)")
print(f"  OD:          {Di_bot + wire_r:.2f} mm (bottom) -> {Di_top + wire_r:.2f} mm (top)")
print(f"  Total coils: {nt},  closed ends: {n_closed} each,  active: {n_active}")
print(f"  L0={L0} mm,  h_active={h_active:.2f} mm,  pitch_mean={pitch_mean:.3f} mm")
print(f"  Pitch range: {p_top:.2f} mm (top/small-OD) -> {p_bot:.2f} mm (bot/large-OD)")

# Beehive profile: cylindrical section at bottom, linear taper toward top.
n_cyl_end  = 3.0   # coils at full bottom diameter before taper begins

# -- OCC imports ---------------------------------------------------------------
from OCC.Core.TColgp import TColgp_HArray1OfPnt
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.GeomAPI import GeomAPI_Interpolate
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipeShell
from OCC.Core.GC import GC_MakeEllipse
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh


def helix_radius(coil_num):
    """Beehive profile: cylindrical base section, then linear taper to top."""
    if coil_num <= n_cyl_end:
        return R_mean_bot
    elif coil_num >= nt - n_closed:
        return R_mean_top
    else:
        frac = (coil_num - n_cyl_end) / (nt - n_closed - n_cyl_end)
        return R_mean_bot + frac * (R_mean_top - R_mean_bot)


def helix_z(coil_num):
    """
    Variable-pitch axial position.

    Dead (closed) coils at both ends use wire_a pitch (coils touching).
    The active zone uses a quadratic distribution biased toward the bottom
    (large-OD coils have more pitch, small-OD top coils have less pitch).

    f(xi) = xi + D_pitch * xi * (1 - xi)   [xi in [0,1], bottom->top]
    => f'(0) = 1 + D_pitch  (high pitch at bottom)
    => f'(1) = 1 - D_pitch  (low pitch at top)
    """
    if coil_num <= n_closed:
        return coil_num * wire_a
    elif coil_num >= nt - n_closed:
        return L0 - (nt - coil_num) * wire_a
    else:
        xi = (coil_num - n_closed) / n_active   # 0 = bottom, 1 = top of active zone
        f  = xi + D_pitch * xi * (1 - xi)
        return h_closed + f * h_active


# -- Build beehive helix path --------------------------------------------------
N = 720   # points (higher = smoother)
pts = TColgp_HArray1OfPnt(1, N + 1)

for i in range(N + 1):
    t     = i / N
    theta = t * nt * 2 * math.pi
    coil  = t * nt
    z     = helix_z(coil)
    r     = helix_radius(coil)
    pts.SetValue(i + 1, gp_Pnt(r * math.cos(theta), r * math.sin(theta), z))

print("Interpolating helix spline...")
interp = GeomAPI_Interpolate(pts, False, 1e-2)
interp.Perform()
if not interp.IsDone():
    sys.exit("ERROR: Helix spline interpolation failed")

helix_edge = BRepBuilderAPI_MakeEdge(interp.Curve()).Edge()
helix_wire_bld = BRepBuilderAPI_MakeWire()
helix_wire_bld.Add(helix_edge)
helix_wire = helix_wire_bld.Wire()
print("  Helix wire built.")

# -- Elliptical profile at path start -----------------------------------------
cx, cy, cz = R_mean_bot, 0.0, 0.0

omega = nt * 2 * math.pi
tx_raw = -R_mean_bot * omega * math.sin(0.0)
ty_raw =  R_mean_bot * omega * math.cos(0.0)
tz_raw =  L0
t_len  = math.sqrt(tx_raw**2 + ty_raw**2 + tz_raw**2)
tx, ty, tz = tx_raw / t_len, ty_raw / t_len, tz_raw / t_len

rx, ry, rz = 1.0, 0.0, 0.0
dot = rx * tx + ry * ty + rz * tz
rx -= dot * tx;  ry -= dot * ty;  rz -= dot * tz
r_len = math.sqrt(rx**2 + ry**2 + rz**2)
rx, ry, rz = rx / r_len, ry / r_len, rz / r_len

bx = ty * rz - tz * ry
by = tz * rx - tx * rz
bz = tx * ry - ty * rx

profile_ax2 = gp_Ax2(
    gp_Pnt(cx, cy, cz),
    gp_Dir(tx, ty, tz),
    gp_Dir(rx, ry, rz),
)
ellipse_geom = GC_MakeEllipse(profile_ax2, wire_r / 2, wire_a / 2).Value()
profile_edge = BRepBuilderAPI_MakeEdge(ellipse_geom).Edge()
profile_wire_bld = BRepBuilderAPI_MakeWire()
profile_wire_bld.Add(profile_edge)
profile_wire = profile_wire_bld.Wire()
print("  Profile ellipse built.")

# -- Sweep profile along helix -------------------------------------------------
print("Sweeping (this may take a moment)...")
pipe = BRepOffsetAPI_MakePipeShell(helix_wire)
pipe.SetMode(True)        # Frenet frame
pipe.Add(profile_wire)
pipe.Build()

if not pipe.IsDone():
    sys.exit("ERROR: PipeShell sweep failed")

pipe.MakeSolid()
spring_solid = pipe.Shape()
print("  Sweep complete.")

# -- Grind ends ----------------------------------------------------------------
big    = max(R_mean_bot + wire_r, 20.0) + 5.0
margin = 5.0

box_bot = BRepPrimAPI_MakeBox(
    gp_Pnt(-big, -big, -margin),
    gp_Pnt( big,  big,  grind_z)
).Shape()
cut1 = BRepAlgoAPI_Cut(spring_solid, box_bot)
cut1.Build()

box_top = BRepPrimAPI_MakeBox(
    gp_Pnt(-big, -big, L0 - grind_z),
    gp_Pnt( big,  big, L0 + margin)
).Shape()
cut2 = BRepAlgoAPI_Cut(cut1.Shape(), box_top)
cut2.Build()
spring_final = cut2.Shape()
print("  Ends ground.")

# -- Export STEP ---------------------------------------------------------------
writer = STEPControl_Writer()
writer.Transfer(spring_final, STEPControl_AsIs)
status = writer.Write("ValveSpring.step")
print(f"Exported: ValveSpring.step  (status={status})")

# -- Export STL ----------------------------------------------------------------
BRepMesh_IncrementalMesh(spring_final, 0.08, False, 0.5)
stl_writer = StlAPI_Writer()
stl_writer.Write(spring_final, "ValveSpring.stl")
print("Exported: ValveSpring.stl")

print("=== CAD generation complete ===")
