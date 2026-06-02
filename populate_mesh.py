import FreeCAD, Fem
doc = FreeCAD.open('ValveSpring_FEA_meshed.FCStd')
m = doc.getObject('Mesh')
fm_obj = doc.getObject('FEMMesh')
new_fm = Fem.FemMesh()
for p in m.Mesh.Points:
    new_fm.addNode(p.x, p.y, p.z)
fm_obj.FemMesh = new_fm
doc.saveAs('ValveSpring_FEA_populated.FCStd')
print(f'Nodes added: {fm_obj.FemMesh.NodeCount}')
