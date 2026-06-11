# FreeCAD startup macro — loads ValveSpring_contact.frd into FEM postprocessor
# Launch with: freecad.exe --run-script load_fea_results.py

import os, sys
import FreeCAD
import FreeCADGui

BASE    = r"D:\Projects_AI\AML_SpeedIncrease"
INP     = os.path.join(BASE, "ValveSpring_mesh.inp")
FRD     = os.path.join(BASE, "ValveSpring_contact.frd")

FreeCADGui.showMainWindow()

doc = FreeCAD.newDocument("ValveSpring_FEA")
FreeCAD.setActiveDocument(doc.Name)

# ── Import mesh ───────────────────────────────────────────────────────────────
import Fem
import feminout.importCcxMeshResults as meshio

print("Importing mesh from:", INP)
try:
    import feminout.importCcxInputFile as inp_reader
    inp_reader.insert(INP, doc.Name)
    doc.recompute()
    print("  Mesh imported via importCcxInputFile")
except Exception as e:
    print(f"  importCcxInputFile failed ({e}), trying FemMesh.read...")
    mesh_obj = doc.addObject("Fem::FemMeshObject", "SpringMesh")
    mesh_obj.FemMesh = Fem.FemMesh()
    mesh_obj.FemMesh.read(INP)
    doc.recompute()
    print(f"  Mesh: {mesh_obj.FemMesh.NodeCount:,} nodes, "
          f"{mesh_obj.FemMesh.VolumeCount:,} elements")

# ── Import FRD results ────────────────────────────────────────────────────────
print("Importing FRD results from:", FRD)
try:
    from feminout import importCcxFrdResults
    importCcxFrdResults.importFrd(FRD, doc)
    doc.recompute()
    print("  FRD loaded — result objects created")
except Exception as e:
    print(f"  importCcxFrdResults failed: {e}")
    try:
        import feminout.importCcxDatResults as dat_io
        print("  Trying importCcxDatResults...")
    except Exception as e2:
        print(f"  Also failed: {e2}")

doc.recompute()

# ── Switch to FEM workbench and activate postprocessor view ──────────────────
FreeCADGui.activateWorkbench("FemWorkbench")

# Select the last result object and show Von Mises / displacement pipeline
result_objs = [o for o in doc.Objects if "Result" in o.TypeId or
               hasattr(o, "DisplacementVectors")]
print(f"  Result objects found: {[o.Label for o in result_objs]}")

if result_objs:
    res = result_objs[-1]
    FreeCADGui.Selection.addSelection(res)
    # Open the FEM result show dialog (shows displacement / stress pipeline)
    try:
        import femresult.resulttools as rt
        FreeCADGui.runCommand("FEM_ResultShow")
        print("  FEM_ResultShow command launched")
    except Exception as e:
        print(f"  FEM_ResultShow: {e}")
        FreeCADGui.runCommand("Std_ViewFitAll")

FreeCADGui.runCommand("Std_ViewFitAll")
FreeCADGui.runCommand("Std_ViewIsometric")
print("Done — FreeCAD postprocessor ready.")
