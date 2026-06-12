"""
Valve Spring CAD Generator - A1770530500 Intake Valve Spring (Beehive)
Drawing parameters: oval wire 2.92x3.66mm, beehive profile, 8.6 coils

Pitch is NON-UNIFORM (progressive):
  - Bottom n_closed coils : dead/closed (wire touching, zero gap)
  - Active zone           : quadratic pitch gradient, small pitch at large-OD bottom,
                            large pitch at small-OD top  ->  bottom coils bind first
  - Top n_closed coils    : dead/closed

Bottom coils (large OD, softer) bind first as the spring is compressed.
The remaining active coils are the stiffer small-OD top coils, producing an
increasing spring rate (progressive behaviour) consistent with F1=250N / F2=620N.

Calibration (2026-06-11) — aligned to INT_Spring_measurement.txt:
  Drawing L0=46.1 mm produces F1_FEA=374 N vs measured 249 N because the
  nominal geometry gives k_FEA~26 N/mm while the measurement implies ~35 N/mm.
  Two free parameters (L0, n_closed) were fitted to two measurement constraints:
    1. F1=249 N at L1=31.6 mm  (preload force)
    2. kink1 at lift=4.05 mm from L1  (first coil-binding event)
  These uniquely require k_FEA=35 N/mm → n_active=4.548, n_closed=2.026.
  L0=38.72 mm then follows from F1=k_FEA*(L0-L1).
  D_pitch is re-derived from the kink position with the new geometry.
  Wire cross-section and coil diameters are unchanged from the drawing.
"""
import math
import sys
import numpy as _np

# -- Drawing parameters (wire cross-section and diameters unchanged) -----------
wire_a     = 2.92    # wire axial dimension (along spring axis) [mm]
wire_r     = 3.66    # wire radial dimension (transverse to axis) [mm]
nt         = 8.6     # total coils
Di_bot     = 15.90   # inner diameter bottom [mm]
Di_top     = 12.00   # inner diameter top [mm]
grind_z    = 0.75    # ground end cut depth [mm]

# -- Calibrated parameters (fitted to INT_Spring_measurement.txt) --------------
# L0 and n_closed are the two free parameters calibrated against:
#   F1=249 N at L1=31.6 mm  AND  kink1 at lift=4.05 mm from L1.
L0         = 38.717  # free length [mm]   (drawing: 46.1 mm; calibrated to match F1)
n_closed   = 2.026   # closed coils per end (drawing: 1.25; calibrated to match k_FEA=35 N/mm)

R_mean_bot = Di_bot / 2 + wire_r / 2   # = 9.78 mm
R_mean_top = Di_top / 2 + wire_r / 2   # = 7.83 mm

# -- Variable-pitch parameters -------------------------------------------------
n_active   = nt - 2 * n_closed          # = 4.548 active coils
h_closed   = n_closed * wire_a          # = 5.916 mm per dead end
h_active   = L0 - 2 * h_closed         # = 26.885 mm active zone height
pitch_mean = h_active / n_active        # = 5.911 mm mean active pitch

# D_pitch controls the pitch gradient.  D_pitch > 0 -> less pitch at bottom
# (large OD), more pitch at top (small OD).
# Re-derived for the calibrated geometry to place kink1 at lift=4.05 mm from L1:
#   s_bind = h_active*(1-D_pitch) - n_active*wire_a = s_preload + 4.05
#   s_preload = L0-L1 = 38.717-31.6 = 7.117 mm  ->  s_bind = 11.167 mm
#   -> D_pitch = 1 - (s_bind + n_active*wire_a)/h_active = 0.0907
# D_pitch = 0.0907  ->  p_bot = 5.375 mm (gap 2.455 mm), p_top = 6.447 mm
D_pitch    = 0.0907

p_bot  = pitch_mean * (1 - D_pitch)
p_top  = pitch_mean * (1 + D_pitch)

print("=== Valve Spring CAD Generator ===")
print(f"  Wire:        {wire_a} x {wire_r} mm (axial x radial)")
print(f"  R_mean:      {R_mean_bot:.3f} mm (bottom) -> {R_mean_top:.3f} mm (top)")
print(f"  OD:          {Di_bot + wire_r:.2f} mm (bottom) -> {Di_top + wire_r:.2f} mm (top)")
print(f"  Total coils: {nt},  closed ends: {n_closed} each,  active: {n_active}")
print(f"  L0={L0} mm,  h_active={h_active:.2f} mm,  pitch_mean={pitch_mean:.3f} mm")
print(f"  Pitch gradient: {p_bot:.2f} mm (bot/large-OD) -> {p_top:.2f} mm (top/small-OD)  ratio={p_top/p_bot:.2f}x")

# Beehive profile: cylindrical section at bottom, linear taper toward top.
# n_cyl_end=3.5: extends the large-OD (soft) bottom section by 0.5 coil vs the
# previous 3.0 setting.  More large-OD coils bind first at lift=4.34 mm, which
# explains the small initial rate change (35→36.5 N/mm) seen in the measurement.
n_cyl_end  = 3.5   # coils at full bottom diameter before taper begins

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

# -- Wire cross-section profile selection -------------------------------------
# "ellipse" : pure ellipse with semi-axes wire_r/2 x wire_a/2  (default)
# "oval"    : oval per thesis DFE6113_5004_00 formula (40), c=OVAL_C,
#             area-matched to the ellipse cross-section
# In FreeCAD: argv[0]=FreeCADCmd, argv[1]=script path, argv[2]=first user arg
_os = __import__("os")
WIRE_PROFILE = _os.environ.get(
    "SPRING_PROFILE",
    sys.argv[2] if len(sys.argv) > 2 else "ellipse",
)
# numpy version compatibility: trapezoid (>=2.0) vs trapz (<2.0)
_trapz = getattr(_np, "trapezoid", None) or getattr(_np, "trapz")
OVAL_C = 0.1      # oval parameter from formula (40): 0 < c <= 0.3
# b_oval that makes oval_area(a=1.83, b, c=OVAL_C) = pi*1.83*1.46 = 8.394 mm²
# c=0.1 → b=1.45392 mm  (calibrated: reduces constant force offset vs measurement)
# c=0.2 → b=1.43585 mm  (original value, too high forces due to larger L0)
OVAL_B = 1.45392  # area-matched axial semi-parameter for oval [mm]

# The oval wire is slightly taller in the axial direction than the ellipse.
# If closed-end coil pitch = wire_a (ellipse height = 2.92mm) is used, the oval
# surface self-intersects, causing Gmsh 3D meshing to fail.
# Compute the true oval axial max extent and use it for the closed-end pitch.
if WIRE_PROFILE == "oval":
    _t_ov = _np.linspace(0, 2 * _np.pi, 2000)
    _y_ov = OVAL_B * _np.cos(_t_ov) * _np.exp(OVAL_C * (wire_r / 2) * _np.sin(_t_ov))
    _wire_a_eff = 2.0 * float(_np.max(_np.abs(_y_ov))) + 0.15  # +0.15mm mesh clearance
    # Preserve calibrated h_active (active zone height → spring rate unchanged)
    wire_a   = _wire_a_eff        # update closed-coil pitch
    h_closed = n_closed * wire_a  # override: closed-end height
    L0       = h_active + 2 * h_closed  # adjusted free length for oval wire
    print(f"  Oval wire axial eff: {_wire_a_eff:.3f} mm  (ellipse: 2.92 mm)  "
          f"-> L0_oval={L0:.3f} mm")

print(f"  Wire profile : {WIRE_PROFILE}" +
      (f"  (c={OVAL_C}, b_oval={OVAL_B} mm)" if WIRE_PROFILE == "oval" else ""))


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
    The active zone uses a quadratic distribution: small pitch at large-OD
    bottom (bottom coils bind first), increasing to large pitch at small-OD top.

    f(xi) = xi - D_pitch * xi * (1 - xi)   [xi in [0,1], bottom->top]
    => f'(0) = 1 - D_pitch  (low pitch at bottom -> bottom coils bind first)
    => f'(1) = 1 + D_pitch  (high pitch at top -> top coils bind last)
    """
    if coil_num <= n_closed:
        return coil_num * wire_a
    elif coil_num >= nt - n_closed:
        return L0 - (nt - coil_num) * wire_a
    else:
        xi = (coil_num - n_closed) / n_active   # 0 = bottom, 1 = top of active zone
        f  = xi - D_pitch * xi * (1 - xi)
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

if WIRE_PROFILE == "oval":
    # Oval cross-section per formula (40) of DFE6113_5004_00-MasterThesis-VATA:
    #   x(t) = a * sin(t)                    [radial direction, along r-vector]
    #   y(t) = b * cos(t) * exp(c * x(t))    [axial direction, along b-vector]
    # t in [0, 2pi]. c=0 reduces to ellipse. c=OVAL_C=0.2 here.
    # b = OVAL_B is chosen so the enclosed area equals the ellipse (pi*a*b_ell).
    # Profile is built as 4 separate non-periodic B-spline arcs (one per quadrant)
    # joined into a closed wire.  A single periodic B-spline creates a seam edge
    # in the swept BRep solid that Gmsh cannot volume-mesh.
    N_ARC = 6   # sample points per quadrant arc (includes shared endpoints)
    a_p   = wire_r / 2    # 1.83 mm — radial semi-axis (same as ellipse)
    b_p   = OVAL_B        # 1.43585 mm — area-matched axial parameter

    # Centroid via Green's theorem (high-resolution numerical integral)
    t_full = _np.linspace(0, 2 * _np.pi, 400, endpoint=False)
    u_full = a_p * _np.sin(t_full)
    v_full = b_p * _np.cos(t_full) * _np.exp(OVAL_C * u_full)
    dxdt_f = a_p * _np.cos(t_full)
    dydt_f = b_p * _np.exp(OVAL_C * u_full) * (-_np.sin(t_full) + OVAL_C * a_p * _np.cos(t_full)**2)
    A_s    = 0.5 * _trapz(u_full * dydt_f - v_full * dxdt_f, t_full)
    u_c    = (0.5 / A_s) * _trapz(u_full**2 * dydt_f, t_full)
    v_c    = -(0.5 / A_s) * _trapz(v_full**2 * dxdt_f, t_full)

    print(f"  Oval: a={a_p:.3f} b={b_p:.5f} c={OVAL_C}  "
          f"area={abs(A_s):.4f} mm2  centroid offset u_c={u_c:.4f} mm")

    def _oval_pt(t):
        u_raw = a_p * float(_np.sin(t))
        v_raw = b_p * float(_np.cos(t)) * float(_np.exp(OVAL_C * u_raw))
        u = u_raw - u_c
        v = v_raw - v_c
        return gp_Pnt(cx + u * rx + v * bx,
                      cy + u * ry + v * by,
                      cz + u * rz + v * bz)

    def _oval_tang(t):
        # d/dt of (a*sin(t), b*cos(t)*exp(c*a*sin(t))), centroid shift is constant
        du = a_p * float(_np.cos(t))
        u_raw = a_p * float(_np.sin(t))
        dv = b_p * float(_np.exp(OVAL_C * u_raw)) * (
             -float(_np.sin(t)) + OVAL_C * a_p * float(_np.cos(t))**2)
        return gp_Vec(du * rx + dv * bx,
                      du * ry + dv * by,
                      du * rz + dv * bz)

    profile_wire_bld = BRepBuilderAPI_MakeWire()
    for _q in range(4):
        t_arc = _np.linspace(_q * _np.pi / 2, (_q + 1) * _np.pi / 2, N_ARC)
        arc_pts = TColgp_HArray1OfPnt(1, N_ARC)
        for _i in range(N_ARC):
            arc_pts.SetValue(_i + 1, _oval_pt(t_arc[_i]))
        arc_interp = GeomAPI_Interpolate(arc_pts, False, 1e-4)  # False = open spline
        # Impose G1 (tangent) constraints at both endpoints so adjacent arcs are
        # C1-continuous at the quadrant boundaries → no kinks on swept surfaces
        arc_interp.Load(_oval_tang(t_arc[0]), _oval_tang(t_arc[-1]), True)
        arc_interp.Perform()
        if not arc_interp.IsDone():
            sys.exit(f"ERROR: Oval arc {_q} interpolation failed")
        profile_wire_bld.Add(BRepBuilderAPI_MakeEdge(arc_interp.Curve()).Edge())

    if not profile_wire_bld.IsDone():
        sys.exit("ERROR: Oval profile wire construction failed")
    profile_wire = profile_wire_bld.Wire()
    print("  Profile oval built (4-arc non-periodic spline).")
else:
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
_step_name = ("ValveSpring_oval.step" if WIRE_PROFILE == "oval"
              else "ValveSpring.step")
writer = STEPControl_Writer()
writer.Transfer(spring_final, STEPControl_AsIs)
status = writer.Write(_step_name)
print(f"Exported: {_step_name}  (status={status})")

# -- Export STL ----------------------------------------------------------------
_stl_name = ("ValveSpring_oval.stl" if WIRE_PROFILE == "oval"
             else "ValveSpring.stl")
BRepMesh_IncrementalMesh(spring_final, 0.08, False, 0.5)
stl_writer = StlAPI_Writer()
stl_writer.Write(spring_final, _stl_name)
print(f"Exported: {_stl_name}")

print("=== CAD generation complete ===")
