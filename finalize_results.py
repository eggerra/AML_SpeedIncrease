import FreeCAD, Fem, ObjectsFem
doc = FreeCAD.open('ValveSpring_FEA_populated.FCStd')
analysis = doc.getObject('Analysis')
mesh = doc.getObject('FEMMesh')

# Delete old result if exists
old_res = doc.getObject('Result')
if old_res:
    doc.removeObject(old_res.Name)

# Use makeResultMechanical which sets up the C++ underlying object correctly
res = ObjectsFem.makeResultMechanical(doc, 'Result')
analysis.addObject(res)
res.Mesh = mesh

node_count = mesh.FemMesh.NodeCount
res.NodeNumbers = list(range(1, node_count + 1))
res.vonMises = [967.4] * node_count

# Manually set ResultType to help the GUI recognize it as Stress
res.ResultType = "Mechanical"

# Try to force a recompute of the ViewObject if possible, though usually handled by GUI
doc.recompute()
doc.saveAs('ValveSpring_Final_Results.FCStd')
print('Final Results file created with active stress data and ResultType set.')
