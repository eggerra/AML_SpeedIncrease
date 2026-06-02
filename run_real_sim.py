import os
import sys

# Add FreeCAD path
sys.path.append(r"C:\Users\eggerra\AppData\Local\Programs\FreeCAD 1.1\bin")

import FreeCAD
import Fem
import ObjectsFem
from femtools import ccxtools

def run_real_simulation():
    doc_path = "ValveSpring_FEA_populated.FCStd"
    if not os.path.exists(doc_path):
        print(f"Error: {doc_path} not found.")
        return

    print(f"Opening {doc_path}...")
    doc = FreeCAD.open(doc_path)
    analysis = doc.getObject("Analysis")
    solver = doc.getObject("CalculiX")
    
    # Check if solver exists, if not create it
    if not solver:
        print("CalculiX solver not found. Creating a new one...")
        try:
            solver = ObjectsFem.makeSolverCalculiXCcxTools(doc, "CalculiX")
        except AttributeError:
            solver = ObjectsFem.makeSolverCalculiX(doc, "CalculiX")
        analysis.addObject(solver)
        
        # Configure non-linear
        if hasattr(solver, "GeometricalNonlinearity"):
            solver.GeometricalNonlinearity = 'nonlinear'
        elif hasattr(solver, "GeometriesNonLinear"):
            solver.GeometriesNonLinear = 'True'
        
        # Add to analysis group if not already there
        if solver not in analysis.Group:
            analysis.addObject(solver)
    
    # Ensure boundary conditions are in the analysis
    # Let's find them in the document
    fixed = doc.getObject("FixedBottom")
    displ = doc.getObject("DisplacementTop")
    if fixed and fixed not in analysis.Group:
        analysis.addObject(fixed)
    if displ and displ not in analysis.Group:
        analysis.addObject(displ)

    # Add element geometry for shell thickness if using 2D elements
    print("Adding 2D element geometry (Thickness)...")
    try:
        el_geom = ObjectsFem.makeElementGeometry2D(doc, "ElementGeometry2D")
        el_geom.Thickness = 3.0 # Approximate representative thickness
        analysis.addObject(el_geom)
    except Exception as e:
        print(f"Warning: Could not add 2D element geometry: {e}")

    doc.recompute()

    # Configure solver path explicitly if needed, but usually it finds ccx.exe in bin
    # We will use ccxtools to run it
    print("Preparing CalculiX solver...")
    fea = ccxtools.CcxTools(solver)
    
    # Check if we can write the .inp file
    print("Writing .inp file...")
    fea.update_objects()
    fea.write_inp_file()
    
    print(f"Working Directory: {fea.working_dir}")
    print(f"Inp File: {fea.inp_file_name}")
    
    print("Starting CCX execution...")
    # This runs the solver and waits for it
    fea.ccx_run()
    
    print("Simulation finished. Checking for results...")
    # Load results back into FreeCAD
    fea.load_results()
    
    # Check if a Result object was created
    results = [o for o in doc.Objects if o.TypeId == 'Fem::FemResultObjectMechanical']
    if results:
        print(f"Successfully created {len(results)} result object(s).")
        # Save the document with real results
        output_path = "ValveSpring_Real_Results.FCStd"
        doc.saveAs(output_path)
        print(f"Saved results to {output_path}")
    else:
        print("No result object found after simulation.")
        # Check logs
        if os.path.exists(os.path.join(fea.working_dir, fea.base_name + ".log")):
            with open(os.path.join(fea.working_dir, fea.base_name + ".log"), "r") as f:
                print("--- CCX LOG ---")
                print(f.read())

if __name__ == "__main__":
    run_real_simulation()
