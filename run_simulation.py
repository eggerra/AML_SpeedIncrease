
import FreeCAD
import Fem
import ObjectsFem
import math
import os

doc_name = "ValveSpring_FEA_meshed.FCStd"
if not os.path.exists(doc_name):
    # Fallback to the one I created if user didn't rename it exactly as I thought
    doc_name = "ValveSpring_FEA.FCStd"

doc = FreeCAD.open(doc_name)
analysis = doc.getObject("Analysis")
spring = doc.getObject("Spring")
mesh_obj = doc.getObject("FEMMesh")

# Ensure solver is set up for non-linear
solver = doc.getObject("CalculiX")
if not solver:
    solver = ObjectsFem.makeSolverCalculixCcxtools(doc, "CalculiX")
    analysis.addObject(solver)

solver.GeometriesNonLinear = 'True'
solver.IterationsControlMax = 50

# Materials
material = doc.getObject("Material")
if not material:
    material = ObjectsFem.makeMaterialSolid(doc, "Material")
    analysis.addObject(material)

# Boundary Conditions
# Faces are: Bottom (Z=0), Top (Z=46.1)
faces = spring.Shape.Faces
bottom_face_idx = -1
top_face_idx = -1

for i, f in enumerate(faces):
    z = f.CenterOfMass.z
    if abs(z) < 0.1:
        bottom_face_idx = i + 1
    elif abs(z - 46.1) < 0.5:
        top_face_idx = i + 1

if bottom_face_idx != -1:
    fixed = doc.addObject("Fem::ConstraintFixed", "FixedBottom")
    fixed.References = [(spring, f"Face{bottom_face_idx}")]
    analysis.addObject(fixed)

if top_face_idx != -1:
    # We'll do a simple linear load first to get a baseline if full contact is too complex for cmd
    displ = doc.addObject("Fem::ConstraintDisplacement", "DisplacementTop")
    displ.References = [(spring, f"Face{top_face_idx}")]
    displ.zFixed = True
    displ.zFree = False
    displ.zDisplacement = -20.0 # 20mm compression
    analysis.addObject(displ)

# In cmd mode, actually RUNNING the solver can be tricky as it spawns external ccx
# We'll prepare the .inp file at least
try:
    from femtools import ccxtools
    fea = ccxtools.CcxTools(solver)
    fea.update_objects()
    fea.write_edit_ccx_input_file()
    print("CalculiX input file generated.")
except Exception as e:
    print(f"Solver setup error: {e}")

doc.saveAs("ValveSpring_Final.FCStd")
print("Final model saved.")
