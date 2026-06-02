
import FreeCAD
import Part
import math

# Parameters from drawing
wire_h = 3.66  # Wire height (vertical)
wire_w = 2.92  # Wire width (radial)
Diu = 15.90    # Inner diameter bottom
Dio = 12.00    # Inner diameter top
L0 = 46.1      # Free length
nt = 8.6       # Total number of coils

# Adjusted L0 for path to account for grind thickness
# The path should extend slightly beyond L0 to ensure clean cuts
path_L0 = L0 + 1.0 
path_start_z = -0.5

doc = FreeCAD.newDocument("ValveSpring")

# Use additive primitive or Helix if possible for better stability
# But beehive is specific. Let's use the Python-Part API more directly.

R_bottom = (Diu + wire_w) / 2.0
R_top = (Dio + wire_w) / 2.0

num_points = 200 # Increased resolution
points = []
# Define transition points for beehive shape
nt_cyl = 6.0
nt_taper = nt - nt_cyl

for i in range(num_points + 1):
    t = float(i) / num_points
    angle = 2 * math.pi * nt * t
    # Map t to the extended Z range
    z = path_start_z + (path_L0 - path_start_z) * t
    
    current_coil = nt * t
    if current_coil <= nt_cyl:
        r = R_bottom
    else:
        # Tapering section
        t_taper = (current_coil - nt_cyl) / nt_taper
        r = R_bottom + (R_top - R_bottom) * t_taper
        
    points.append(FreeCAD.Vector(r * math.cos(angle), r * math.sin(angle), z))

# Create a B-Spline path
path_shape = Part.BSplineCurve()
path_shape.interpolate(points)
path_edge = path_shape.toShape()

# Profile
ellipse = Part.Ellipse(FreeCAD.Vector(0,0,0), wire_h/2.0, wire_w/2.0)
profile_edge = ellipse.toShape()
profile_wire = Part.Wire(profile_edge)

# Transform profile to start
try:
    tangent_val = path_shape.tangent(0)
    if isinstance(tangent_val, FreeCAD.Vector):
        tangent = tangent_val
    else:
        tangent = FreeCAD.Vector(tangent_val[0], tangent_val[1], tangent_val[2])
except Exception:
    tangent = (points[1] - points[0]).normalize()

normal = FreeCAD.Vector(points[0].x, points[0].y, 0).normalize()
binormal = tangent.cross(normal)
rot_mat = FreeCAD.Matrix(normal.x, binormal.x, tangent.x, points[0].x,
                         normal.y, binormal.y, tangent.y, points[0].y,
                         normal.z, binormal.z, tangent.z, points[0].z,
                         0, 0, 0, 1)
profile_wire.transformShape(rot_mat)

# Sweep
sweep_shape = Part.Wire(path_edge).makePipeShell([profile_wire], True, True)

# Apply grinding at ends
# Free length is L0 (46.1mm). Bottom is at z=0, Top is at z=L0.
# The grinding should create flat parallel surfaces.
# We'll use boolean cuts with large boxes to "grind" the ends.

# Bottom grind box: Cut everything below Z=0
bottom_box = Part.makeBox(200, 200, 10.0, FreeCAD.Vector(-100, -100, -10.0))
# Top grind box: Cut everything above Z=L0
top_box = Part.makeBox(200, 200, 10.0, FreeCAD.Vector(-100, -100, L0))

# Perform cuts
# To avoid "residual volumes" (isolated fragments), we ensure the sweep covers the full range
# and then cut precisely at the boundaries.
spring_shape = sweep_shape.cut(bottom_box).cut(top_box)

spring_obj = doc.addObject("Part::Feature", "Spring")
spring_obj.Shape = spring_shape

doc.recompute()
doc.saveAs("ValveSpring.FCStd")
print("CAD model generated successfully.")
import sys
sys.exit(0)
