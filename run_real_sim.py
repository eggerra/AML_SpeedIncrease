import os
import sys

if 'FreeCAD' not in sys.modules:
    sys.path.append(r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin")

import FreeCAD
import Fem
import ObjectsFem
from femtools import ccxtools

def run_real_sim():
    doc_path = "ValveSpring_FEA_meshed.FCStd"
    if not os.path.exists(doc_path):
        print(f"Error: {doc_path} not found.")
        return

    doc = FreeCAD.open(doc_path)
    analysis = doc.getObject("Analysis")
    spring = doc.getObject("Spring")
    femmesh_obj = doc.getObject("FEMMesh")

    # Add constraints if they don't exist
    if not doc.getObject("FixedBottom"):
        faces = spring.Shape.Faces
        bottom_face_idx = -1
        top_face_idx = -1
        for i, f in enumerate(faces):
            z = f.CenterOfMass.z
            if abs(z) < 0.1: bottom_face_idx = i + 1
            elif abs(z - 46.1) < 0.5: top_face_idx = i + 1
        
        fixed = doc.addObject("Fem::ConstraintFixed", "FixedBottom")
        fixed.References = [(spring, f"Face{bottom_face_idx}")]
        analysis.addObject(fixed)
        
        displ = doc.addObject("Fem::ConstraintDisplacement", "DisplacementTop")
        displ.References = [(spring, f"Face{top_face_idx}")]
        displ.zFree = False
        displ.zDisplacement = -5.0
        analysis.addObject(displ)

    # Re-import mesh into FemMesh
    m = doc.getObject('Mesh')
    import FemMesh
    new_fm = FemMesh.FemMesh()
    for p in m.Mesh.Points:
        new_fm.addNode(p.x, p.y, p.z)
    for facet in m.Mesh.Facets:
        new_fm.addFace([idx + 1 for idx in facet.PointIndices])
    femmesh_obj.FemMesh = new_fm

    # Solver Setup
    solver = doc.getObject("CalculiX")
    if not solver:
        try:
            solver = ObjectsFem.makeSolverCalculiXCcxTools(doc, "CalculiX")
        except:
            solver = ObjectsFem.makeSolverCalculiX(doc, "CalculiX")
        analysis.addObject(solver)
    
    # Minimal settings for a quick run
    if hasattr(solver, "GeometriesNonLinear"):
        solver.GeometriesNonLinear = 'True'
    elif hasattr(solver, "GeometricalNonlinearity"):
        solver.GeometricalNonlinearity = 'nonlinear'
    solver.IncrementsMaximum = 5 
    
    doc.recompute()
    
    print("Initializing CcxTools...")
    fea = ccxtools.CcxTools(solver)
    fea.update_objects()
    fea.setup_working_dir()
    
    print(f"Working directory: {fea.working_dir}")
    
    print("Writing .inp file...")
    fea.write_inp_file()
    
    print("Starting CCX run...")
    # This might fail if ccx binary is not found, but we want to see the error/log
    try:
        fea.run()
        print("Run finished.")
    except Exception as e:
        print(f"Run failed: {e}")
        
    # Check for log files in working directory
    if os.path.exists(fea.working_dir):
        files = os.listdir(fea.working_dir)
        print(f"Files in working dir: {files}")
        for f in files:
            if f.endswith(".log") or f.endswith(".dat"):
                print(f"--- Content of {f} ---")
                with open(os.path.join(fea.working_dir, f), 'r') as log_file:
                    print(log_file.read())

if __name__ == "__main__":
    run_real_sim()
