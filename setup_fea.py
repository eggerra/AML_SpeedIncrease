
import FreeCAD
import Part
import Fem
import ObjectsFem
import math

doc = FreeCAD.open("ValveSpring.FCStd")
spring = doc.getObject("Spring")

# Create Analysis
analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

# Mesh - using the most reliable factory method
mesh_obj = ObjectsFem.makeMeshNetgen(doc, "FEMMesh")
try:
    mesh_obj.Part = spring
except:
    try:
        mesh_obj.Source = spring
    except:
        print("Manual link required in GUI.")

# Force recompute to ensure links are established
doc.recompute()

# Material
material = ObjectsFem.makeMaterialSolid(doc, "Material")
mat = material.Material
mat['Name'] = "Steel_G79500"
mat['YoungsModulus'] = "206000 MPa"
mat['PoissonRatio'] = "0.3"
material.Material = mat
analysis.addObject(material)

# In GUI/Console, one would call C++ mesh generation.
# In freecadcmd, we try to use the python wrapper if it works.
try:
    from femmesh import netgenmesh
    n = netgenmesh.NetgenMesh(mesh_obj)
    n.create_mesh()
except:
    pass

doc.saveAs("ValveSpring_FEA.FCStd")
print("FEA Model Saved.")
