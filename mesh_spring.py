"""
mesh_spring.py - FreeCAD console script
Meshes ValveSpring.step with GmshTools (Tet10) and exports ValveSpring_mesh.inp

Run with:
  FreeCADCmd.exe mesh_spring.py
"""
import sys, os

BASE  = r"D:\Projects_AI\AML_SpeedIncrease"
STEP  = os.environ.get("SPRING_STEP",     os.path.join(BASE, "ValveSpring.step"))
OUT   = os.environ.get("SPRING_MESH_OUT", os.path.join(BASE, "ValveSpring_mesh.inp"))
FCSTD = os.environ.get("SPRING_FCSTD",   os.path.join(BASE, "ValveSpring_meshed.FCStd"))

LMAX = 1.0
LMIN = 0.5

LOG = os.path.join(BASE, "mesh_spring.log")
_log = open(LOG, "w", buffering=1)
def log(msg):
    _log.write(msg + "\n")
    _log.flush()

log("=== FreeCAD Spring Mesher ===")
log(f"  STEP : {STEP}")
log(f"  LMAX = {LMAX}, LMIN = {LMIN}")

import FreeCAD, Import, ObjectsFem
from femmesh.gmshtools import GmshTools

log("  Imports OK")

doc = FreeCAD.newDocument("ValveSpring")
Import.insert(STEP, doc.Name)
doc.recompute()

solids = [o for o in doc.Objects if hasattr(o, "Shape") and o.Shape.Volume > 0]
if not solids:
    log("ERROR: no solid")
    sys.exit("no solid")
shape_obj = solids[0]
log(f"  Shape  : {shape_obj.Label}  Vol={shape_obj.Shape.Volume:.0f} mm3")

mesh_obj = ObjectsFem.makeMeshGmsh(doc, "SpringMesh")
mesh_obj.Shape                   = shape_obj
mesh_obj.CharacteristicLengthMax = f"{LMAX} mm"
mesh_obj.CharacteristicLengthMin = f"{LMIN} mm"
mesh_obj.ElementOrder            = "2nd"
mesh_obj.OptimizeStd             = True
mesh_obj.HighOrderOptimize       = "Elastic+Optimization"  # fix neg-Jacobian 2nd-order nodes
mesh_obj.WorkingDirectory        = BASE
doc.recompute()

log("Running Gmsh...")
err = GmshTools(mesh_obj).create_mesh()
log(f"  err={err!r}")
doc.recompute()

fem = mesh_obj.FemMesh
n_nodes = fem.NodeCount
n_elems = fem.VolumeCount
log(f"  Nodes={n_nodes:,}  VolElems={n_elems:,}")

if n_elems == 0:
    log("ERROR: no volume elements - trying coarser mesh")
    mesh_obj.CharacteristicLengthMax = "2.0 mm"
    mesh_obj.CharacteristicLengthMin = "0.8 mm"
    doc.recompute()
    err2 = GmshTools(mesh_obj).create_mesh()
    log(f"  Retry err={err2!r}")
    doc.recompute()
    n_nodes = mesh_obj.FemMesh.NodeCount
    n_elems = mesh_obj.FemMesh.VolumeCount
    log(f"  Retry: Nodes={n_nodes:,}  VolElems={n_elems:,}")
    if n_elems == 0:
        log("FATAL: still no volume elements")
        sys.exit("FATAL: no volume elements")

log(f"Exporting -> {OUT}")
mesh_obj.FemMesh.write(OUT)
size_kb = os.path.getsize(OUT) // 1024
log(f"  Written: {size_kb} kB")

doc.saveAs(FCSTD)
log(f"  Saved: {FCSTD}")
log("=== Meshing complete ===")
_log.close()
