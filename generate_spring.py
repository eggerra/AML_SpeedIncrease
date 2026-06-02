"""
Valve Spring CAD Model Generator
Part: A1770530500 - Intake Valve Spring (Beehive)
"""
import sys, os, math, traceback
sys.path.append('.')
import FreeCAD, Part
from FreeCAD import Base

# ── Spring parameters from drawing ──────────────────────────────────────────
L0          = 46.1      # free length [mm]
D_inner_bot = 15.90     # inner diameter bottom [mm]
D_inner_top = 12.00     # inner diameter top [mm]
wire_h      = 3.66      # wire height (axial) [mm]
wire_w      = 2.92      # wire width (radial) [mm]
nt          = 8.6       # total coils
n_cyl       = 6.0       # cylindrical coils (bottom section)
n_taper     = nt - n_cyl  # tapered coils (beehive top)
grind       = 0.75      # ground end thickness [mm]

R_inner_bot = D_inner_bot / 2.0
R_inner_top = D_inner_top / 2.0
R_mean_bot  = R_inner_bot + wire_w / 2.0
R_mean_top  = R_inner_top + wire_w / 2.0

pitch       = (L0 - wire_h) / (nt - 1)   # approximate pitch

print("=== Valve Spring CAD Generator ===")
print(f"L0={L0}mm, nt={nt}, pitch={pitch:.3f}mm")
print(f"R_mean: {R_mean_bot:.2f}mm (bot) -> {R_mean_top:.2f}mm (top)")

# ── Build helix path ─────────────────────────────────────────────────────────
N_PTS = 400
pts   = []
for i in range(N_PTS + 1):
    t     = i / N_PTS          # 0 → 1
    angle = t * nt * 2 * math.pi
    z     = t * L0

    # coil number at this point
    coil_num = t * nt

    # radius: cylindrical for first n_cyl coils, then taper
    if coil_num <= n_cyl:
        r = R_mean_bot
    else:
        frac = (coil_num - n_cyl) / n_taper
        r    = R_mean_bot + frac * (R_mean_top - R_mean_bot)

    pts.append(Base.Vector(r * math.cos(angle),
                           r * math.sin(angle),
                           z))

path = Part.BSplineCurve()
path.interpolate(pts)
path_edge  = path.toShape()
path_wire  = Part.Wire([path_edge])

# ── Oval cross-section (ellipse) ─────────────────────────────────────────────
# Placed at the start of the path, oriented along the path tangent
start_pt  = pts[0]
tangent   = (Base.Vector(pts[1]) - Base.Vector(pts[0])).normalize()
# Normal to tangent in XY plane → radial direction
normal    = Base.Vector(-math.sin(0), math.cos(0), 0)   # at angle=0
binormal  = tangent.cross(normal).normalize()

ellipse   = Part.Ellipse(Base.Vector(0, 0, 0),
                         wire_h / 2.0,   # major (axial)
                         wire_w / 2.0)   # minor (radial)
ellipse_edge = ellipse.toShape()
profile   = Part.Wire([ellipse_edge])

# Position profile at path start
mat = FreeCAD.Matrix()
# Rotate so ellipse major axis aligns with Z (axial)
profile_placed = profile.copy()
profile_placed.Placement = FreeCAD.Placement(
    Base.Vector(pts[0]),
    FreeCAD.Rotation(Base.Vector(0, 0, 1), Base.Vector(tangent))
)

# ── Sweep ────────────────────────────────────────────────────────────────────
print("Sweeping profile along helix path...")
try:
    spring_solid = path_wire.makePipeShell([profile_placed], True, True)
    print(f"Sweep volume: {spring_solid.Volume:.1f} mm^3")
except Exception as e:
    print(f"Sweep error: {e}")
    traceback.print_exc()
    sys.exit(1)

# ── Grind ends (cut flat at Z=grind and Z=L0-grind) ─────────────────────────
print("Grinding ends...")
bbox   = spring_solid.BoundBox
margin = 5.0
big    = 40.0

# Bottom cut: remove everything below Z=grind
cut_bot = Part.makeBox(big*2, big*2, grind + margin,
                       Base.Vector(-big, -big, -margin))
# Top cut: remove everything above Z=L0-grind
cut_top = Part.makeBox(big*2, big*2, grind + margin,
                       Base.Vector(-big, -big, L0 - grind))

spring_cut = spring_solid.cut(cut_bot)
spring_cut = spring_cut.cut(cut_top)
print(f"Final volume: {spring_cut.Volume:.1f} mm^3")

# ── Save to FreeCAD document ─────────────────────────────────────────────────
doc = FreeCAD.newDocument("ValveSpring")
feat = doc.addObject("Part::Feature", "Spring")
feat.Shape = spring_cut
doc.recompute()
doc.saveAs(os.path.abspath("ValveSpring.FCStd"))
print("Saved: ValveSpring.FCStd")
print("=== CAD generation complete ===")
