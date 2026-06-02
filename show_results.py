import FreeCAD, FreeCADGui, os

doc = FreeCAD.open(os.path.abspath("ValveSpring_FEA.FCStd"))
FreeCADGui.showMainWindow()
FreeCADGui.activateWorkbench("FemWorkbench")
FreeCADGui.updateGui()

# Hide geometry and mesh
for name in ["Spring", "FEMMesh"]:
    obj = doc.getObject(name)
    if obj:
        obj.ViewObject.Visibility = False

# Find all pipelines and show the last one (full lift)
pipelines = sorted([o for o in doc.Objects if "Pipeline" in o.Name], key=lambda o: o.Name)
print(f"Pipelines found: {[p.Name for p in pipelines]}")

if pipelines:
    final = pipelines[-1]
    final.ViewObject.Visibility = True
    try:
        final.ViewObject.Field = "Von Mises Stress"
        print(f"Field set to Von Mises Stress on {final.Name}")
    except Exception as e:
        print(f"Field error: {e}")

doc.recompute()
FreeCADGui.updateGui()
FreeCADGui.SendMsgToActiveView("ViewFit")
FreeCADGui.updateGui()
print("Done.")
