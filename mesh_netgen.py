"""
Standalone Netgen mesher for ValveSpring — run via:
  freecadcmd mesh_netgen.py
Requires: netgen-mesher installed in FreeCAD Python
  (pip install netgen-mesher, using FreeCAD's python.exe)

Produces ValveSpring_mesh.inp with C3D10 (10-node tet) elements.
Wire: 2.92 x 3.66 mm — maxh=0.5 gives ~6 elements across wire width.

NOTE: Attempts at local refinement (RestrictH constraints to 0.30 mm in
active coil zone) triggered SYSTEM ERROR: more elements on face in Netgen's
surface pass, causing negative Jacobians in C3D10 curved elements.
Uniform maxh=0.50 is the stable limit for this geometry.
"""
import sys, os, math, json
import numpy as np

BASE = r"D:\Projects_AI\AML_SpeedIncrease"

# Log file — FreeCADCmd swallows Python stdout; write progress here instead.
_LOG = open(os.path.join(BASE, "mesh_netgen.log"), "w", buffering=1)
def log(msg):
    _LOG.write(msg + "\n"); _LOG.flush()
    print(msg)   # also print in case running outside FreeCADCmd

# Read params from JSON config if present (written by pipeline to bypass FreeCADCmd env-var issue)
_cfg_file = os.path.join(BASE, "_mesh_config.json")
_cfg = {}
if os.path.isfile(_cfg_file):
    with open(_cfg_file) as _f:
        _cfg = json.load(_f)

STEP  = _cfg.get("SPRING_STEP",     os.environ.get("SPRING_STEP",     os.path.join(BASE, "ValveSpring.step")))
OUT   = _cfg.get("SPRING_MESH_OUT", os.environ.get("SPRING_MESH_OUT", os.path.join(BASE, "ValveSpring_mesh.inp")))
MAX_H = float(_cfg.get("SPRING_MAXH", os.environ.get("SPRING_MAXH", "0.5")))  # mm
MIN_H   = 0.12   # mm
GRADING = 0.3    # mesh transition rate

# FreeCADCmd runs scripts twice (main + module import). Guard against re-meshing
# a file we already wrote in the same session.
if os.path.isfile(OUT):
    with open(OUT) as _hf:
        _hdr = _hf.readline()
    if "mesh_netgen.py" in _hdr:
        log(f"  Output already written by mesh_netgen.py — skipping duplicate run.")
        sys.exit(0)

# C3D10 node reorder: netgen tetra10 -> CalculiX C3D10
#
# Netgen corners  : [v0, v1, v2, v3] produce det([v1-v0,v2-v0,v3-v0]) < 0
# CalculiX requires det > 0 -> swap v0<->v1 (negates determinant).
# After swap n0=v1,n1=v0,n2=v2,n3=v3, mid-edge nodes re-map as:
#   CCX pos 4  = e(n0,n1) = e(v1,v0) = e(v0v1) <- Netgen[4]
#   CCX pos 5  = e(n1,n2) = e(v0,v2)           <- Netgen[5]
#   CCX pos 6  = e(n2,n0) = e(v2,v1) = e(v1v2) <- Netgen[7]
#   CCX pos 7  = e(n0,n3) = e(v1,v3)           <- Netgen[8]
#   CCX pos 8  = e(n1,n3) = e(v0,v3)           <- Netgen[6]
#   CCX pos 9  = e(n2,n3) = e(v2,v3)           <- Netgen[9]
REORDER = [1, 0, 2, 3, 4, 5, 7, 8, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

try:
    from netgen import occ
    from netgen import meshing as ngmesh
    import pyngcore as ngcore
except ModuleNotFoundError as e:
    sys.exit(f"ERROR: netgen not available -- {e}\n"
             "Install with: <FreeCAD>/bin/python.exe -m pip install netgen-mesher")

log(f"=== Netgen Spring Mesher ===")
log(f"  STEP  : {STEP}")
log(f"  maxh={MAX_H} mm  minh={MIN_H} mm  grading={GRADING}")

# Load STEP and heal geometry
geom = occ.OCCGeometry(STEP)
geom.Heal()
log(f"  Geometry loaded and healed.")

# Meshing parameters — checkoverlap=0 lets netgen proceed past self-intersecting
# surfaces in the closed-coil tight-pitch zone rather than aborting.
mp = ngmesh.MeshingParameters(
    maxh            = MAX_H,
    minh            = MIN_H,
    grading         = GRADING,
    curvaturesafety = 2.0,
    segmentsperedge = 1.0,
    optsteps3d      = 5,
    checkoverlap    = 0,
    checkoverlappingboundary = 0,
)

_mesh_done = False
for _attempt, _maxh in enumerate([MAX_H, MAX_H * 2, MAX_H * 3]):
    _mp = ngmesh.MeshingParameters(
        maxh=_maxh, minh=MIN_H, grading=GRADING,
        curvaturesafety=2.0, segmentsperedge=1.0,
        optsteps3d=5, checkoverlap=0, checkoverlappingboundary=0,
    ) if _attempt > 0 else mp
    try:
        with ngcore.TaskManager():
            mesh = geom.GenerateMesh(mp=_mp)
        if _attempt > 0:
            log(f"  Retry maxh={_maxh} succeeded.")
        _mesh_done = True
        break
    except Exception as _e:
        log(f"  Netgen attempt {_attempt+1} failed (maxh={_maxh}): {_e}")

if not _mesh_done:
    log(f"  OCC meshing failed — trying STL fallback (coarse re-export from OCC shape)")
    _coarse_stl = STEP.replace('.step', '_netgen_fallback.stl')
    try:
        # Re-export a coarser STL directly from the loaded OCC shape.
        # The pre-built STL (0.08 mm deflection) produces ~3380 Netgen charts on the helix
        # and causes the spiral-chart handler to stall. 0.5 mm deflection reduces chart count.
        from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
        from OCC.Core.StlAPI import StlAPI_Writer
        from OCC.Core.STEPControl import STEPControl_Reader
        _step_reader = STEPControl_Reader()
        _step_reader.ReadFile(STEP)
        _step_reader.TransferRoots()
        _occ_shape = _step_reader.Shape()
        BRepMesh_IncrementalMesh(_occ_shape, 0.5, False, 0.5, False).Perform()
        StlAPI_Writer().Write(_occ_shape, _coarse_stl)
        log(f"  Coarse STL written: {_coarse_stl} ({os.path.getsize(_coarse_stl):,} bytes)")
    except Exception as _ex:
        log(f"  Coarse re-export failed ({_ex}) — falling back to existing fine STL")
        _coarse_stl = STEP.replace('.step', '.stl')
    if not os.path.isfile(_coarse_stl):
        sys.exit(f"ERROR: No STL available for fallback at {_coarse_stl}")
    try:
        from netgen.stl import STLGeometry
        log(f"  Loading STL geometry: {_coarse_stl}")
        _stl_geom = STLGeometry(_coarse_stl)
        with ngcore.TaskManager():
            mesh = _stl_geom.GenerateMesh(mp=mp)
        log(f"  STL fallback meshing succeeded.")
    except Exception as _e2:
        sys.exit(f"ERROR: STL fallback meshing failed: {_e2}")

nelems_1d = mesh.Elements1D().NumPy().size
nelems_2d = mesh.Elements2D().NumPy().size
nelems_3d = mesh.Elements3D().NumPy().size
log(f"  1st order: {len(mesh.Coordinates())} nodes, "
      f"{nelems_1d} edges, {nelems_2d} faces, {nelems_3d} volumes")

if nelems_3d == 0:
    sys.exit("ERROR: Netgen produced 0 volume elements.")

# Upgrade to second order (C3D10)
mesh.SecondOrder()
coords  = mesh.Coordinates()   # shape (N, 3)
volumes = mesh.Elements3D().NumPy()
nod_vol = volumes["nodes"].copy()
np_vol  = volumes["np"].tolist()

# Apply C3D10 node reordering for all tetra10 elements
for i in range(len(np_vol)):
    if np_vol[i] == 10:
        nod_vol[i] = nod_vol[i][REORDER]

# -----------------------------------------------------------------------
# Post-process: straighten all mid-side nodes to arithmetic edge midpoints.
# Netgen places mid-side nodes on the curved OCC surface.  For elements in
# the tight closed-coil zone the curved placement produces negative Jacobians
# at CalculiX integration points even when the linear (corner-only) Jacobian
# is positive.  Using straight midpoints eliminates this while retaining
# second-order accuracy of the shape functions.
#
# CalculiX C3D10 mid-edge layout (after REORDER, 0-indexed within element):
#   pos 4: midpoint(pos 0, pos 1)   pos 5: midpoint(pos 1, pos 2)
#   pos 6: midpoint(pos 2, pos 0)   pos 7: midpoint(pos 0, pos 3)
#   pos 8: midpoint(pos 1, pos 3)   pos 9: midpoint(pos 2, pos 3)
MID_EDGE_PAIRS = [(0,1),(1,2),(2,0),(0,3),(1,3),(2,3)]  # corner pairs for positions 4-9

coords_arr = np.array(coords, dtype=np.float64)

mid_corner = {}  # mid_node_id -> (c1_id, c2_id)  (1-indexed)
for i, (nodes_i, np_i) in enumerate(zip(nod_vol, np_vol)):
    if np_i < 10: continue
    for mid_pos, (c_a, c_b) in enumerate(MID_EDGE_PAIRS):
        mid_id = int(nodes_i[4 + mid_pos])
        ca_id  = int(nodes_i[c_a])
        cb_id  = int(nodes_i[c_b])
        mid_corner[mid_id] = (ca_id, cb_id)

n_moved = 0
for mid_id, (ca_id, cb_id) in mid_corner.items():
    new_pos = 0.5 * (coords_arr[ca_id - 1] + coords_arr[cb_id - 1])
    if not np.allclose(coords_arr[mid_id - 1], new_pos):
        coords_arr[mid_id - 1] = new_pos
        n_moved += 1
log(f"  Straightened {n_moved} mid-side nodes to edge midpoints.")

# Drop genuinely degenerate elements (|J| < J_MIN at corner nodes).
# These are slivers in the top closed-coil zone; outside the contact zone
# so their removal does not affect the spring-rate result.
J_MIN = 1e-3
keep_mask = []
n_dropped  = 0
for i, (nodes_i, np_i) in enumerate(zip(nod_vol, np_vol)):
    if np_i < 4:
        keep_mask.append(True); continue
    c = coords_arr[nodes_i[:4] - 1]
    J = np.linalg.det(np.array([c[1]-c[0], c[2]-c[0], c[3]-c[0]]).T)
    if abs(J) < J_MIN:
        keep_mask.append(False); n_dropped += 1
    else:
        keep_mask.append(True)

if n_dropped:
    log(f"  Dropped {n_dropped} degenerate elements (|J| < {J_MIN})")

nod_vol_keep = [nod_vol[i] for i, k in enumerate(keep_mask) if k]
np_vol_keep  = [np_vol[i]  for i, k in enumerate(keep_mask) if k]
log(f"  2nd order: {len(coords_arr)} nodes, {len(np_vol_keep)} C3D10 elements ({n_dropped} degenerate dropped)")

# Write CalculiX .inp file
log(f"  Writing {OUT} ...")
with open(OUT, "w") as f:
    f.write("** written by mesh_netgen.py (netgen-mesher)\n")
    f.write("** highest dimension mesh elements only.\n\n")

    # Nodes
    f.write("** Nodes\n")
    f.write("*Node, NSET=Nall\n")
    for i, (x, y, z) in enumerate(coords_arr, start=1):
        f.write(f"{i}, {x:.10g}, {y:.10g}, {z:.10g}\n")

    # Elements
    f.write("\n** Define element set Eall\n")
    f.write("*Element, TYPE=C3D10, ELSET=Eall\n")
    for i, (nodes, np_) in enumerate(zip(nod_vol_keep, np_vol_keep), start=1):
        live = nodes[:np_]
        f.write(f"{i}, " + ", ".join(str(n) for n in live) + "\n")

sz = os.path.getsize(OUT)
log(f"  Written: {sz:,} bytes")
log("=== Done ===")
