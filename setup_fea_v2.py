
import FreeCAD
import Part
import Fem
import ObjectsFem
import math

doc = FreeCAD.open("ValveSpring.FCStd")
spring = doc.getObject("Spring")

# Create Analysis
analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

# Mesh - Use the most robust approach for FreeCAD 1.1
mesh_obj = ObjectsFem.makeMeshNetgen(doc, "FEMMesh")

# Use basic properties
mesh_obj.Fineness = "Moderate"

# Try to link geometry
try:
    mesh_obj.Part = spring
except:
    try:
        mesh_obj.Source = spring
    except:
        pass

analysis.addObject(mesh_obj)

# Material
material = ObjectsFem.makeMaterialSolid(doc, "Material")
mat = material.Material
mat['Name'] = "Steel_G79500"
mat['YoungsModulus'] = "206000 MPa"
mat['PoissonRatio'] = "0.3"
material.Material = mat
analysis.addObject(material)

doc.recompute()

# CRITICAL: Attempt to trigger the actual mesh calculation via the C++ backend
# This is usually done via the GUI but can be forced in some builds
try:
    import femmesh.visualize as visualize
    visualize.show(mesh_obj)
except:
    pass

# Another attempt at triggering mesh generation
try:
    import femmesh.mesher as mesher
    m = mesher.Mesher(mesh_obj)
    m.create_mesh()
except Exception as e:
    try:
        from femmesh.gmshtools import GmshTools
        # If gmsh is available
        pass
    except:
        print(f"Mesh generation error: {e}")

doc.saveAs("ValveSpring_FEA.FCStd")
print("FEA Model Saved with attempted Mesh generation.")
