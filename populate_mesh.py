import FreeCAD, Fem
doc = FreeCAD.open('ValveSpring_FEA_meshed.FCStd')
m = doc.getObject('Mesh')
fm_obj = doc.getObject('FEMMesh')
new_fm = Fem.FemMesh()
for p in m.Mesh.Points:
    new_fm.addNode(p.x, p.y, p.z)

# Add elements (facets) as Faces in FemMesh
# FemMesh.addFace(v1, v2, v3) where v1, v2, v3 are node IDs (1-indexed)
for facet in m.Mesh.Facets:
    new_fm.addFace([idx + 1 for idx in facet.PointIndices])
fm_obj.FemMesh = new_fm
doc.saveAs('ValveSpring_FEA_populated.FCStd')
print(f'Nodes added: {fm_obj.FemMesh.NodeCount}')
