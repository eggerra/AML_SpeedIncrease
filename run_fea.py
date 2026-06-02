"""
FEA: Mesh + CalculiX solve + open results in FreeCAD post-processor
Part: A1770530500 - Intake Valve Spring
"""
import sys, os, math, traceback
sys.path.append('.')
import FreeCAD, FreeCADGui, ObjectsFem
from femmesh import gmshtools
from femtools import ccxtools

L0 = 46.1

def run():
    print("[1/6] Opening CAD model...", flush=True)
    doc = FreeCAD.open(os.path.abspath("ValveSpring.FCStd"))
    spring = doc.getObject("Spring")
    print(f"      Volume: {spring.Shape.Volume:.1f} mm^3", flush=True)

    print("[2/6] Creating FEM analysis...", flush=True)
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

    mat = ObjectsFem.makeMaterialSolid(doc, "Material")
    mat.Material = {
        "Name":          "ND_SiCrNiV_SC",
        "YoungsModulus": "206000 MPa",
        "PoissonRatio":  "0.3",
        "Density":       "7850 kg/m^3",
    }
    analysis.addObject(mat)

    print("[3/6] Generating solid mesh with Gmsh...", flush=True)
    mesh_obj = ObjectsFem.makeMeshGmsh(doc, "FEMMesh")
    mesh_obj.Shape              = spring
    mesh_obj.CharacteristicLengthMax = "2.0 mm"
    mesh_obj.CharacteristicLengthMin = "0.8 mm"
    mesh_obj.ElementOrder       = "2nd"
    mesh_obj.ElementDimension   = "3D"
    analysis.addObject(mesh_obj)
    doc.recompute()

    gm = gmshtools.GmshTools(mesh_obj)
    err = gm.create_mesh()
    print(f"      Gmsh: {err}", flush=True)
    print(f"      Nodes:   {mesh_obj.FemMesh.NodeCount}", flush=True)
    print(f"      Volumes: {mesh_obj.FemMesh.VolumeCount}", flush=True)

    if mesh_obj.FemMesh.VolumeCount == 0:
        print("ERROR: No volume elements — aborting.", flush=True)
        return

    print("[4/6] Applying boundary conditions...", flush=True)
    faces = spring.Shape.Faces
    z_vals = sorted([(i+1, f.CenterOfMass.z) for i, f in enumerate(faces)], key=lambda x: x[1])
    bot_idx = z_vals[0][0]
    top_idx = z_vals[-1][0]
    print(f"      Fixed face {bot_idx} (z={z_vals[0][1]:.2f})", flush=True)
    print(f"      Displaced face {top_idx} (z={z_vals[-1][1]:.2f})", flush=True)

    fixed = ObjectsFem.makeConstraintFixed(doc, "FixedBottom")
    fixed.References = [(spring, f"Face{bot_idx}")]
    analysis.addObject(fixed)

    displ = ObjectsFem.makeConstraintDisplacement(doc, "DisplacementTop")
    displ.References   = [(spring, f"Face{top_idx}")]
    displ.zFree        = False
    displ.zDisplacement = -10.0   # 10 mm compression (max valve lift)
    displ.xFree        = False;  displ.xDisplacement = 0.0
    displ.yFree        = False;  displ.yDisplacement = 0.0
    analysis.addObject(displ)

    print("[5/6] Configuring CalculiX solver...", flush=True)
    solver = ObjectsFem.makeSolverCalculiXCcxTools(doc, "CalculiX")
    solver.AnalysisType                    = "static"
    solver.GeometricalNonlinearity         = "nonlinear"
    solver.TimeInitialIncrement            = 0.1
    solver.TimePeriod                      = 1.0
    solver.TimeMinimumIncrement            = 0.01
    solver.TimeMaximumIncrement            = 0.2
    analysis.addObject(solver)
    doc.recompute()

    fea = ccxtools.CcxTools()
    fea.analysis = analysis
    fea.solver   = solver
    fea.update_objects()
    fea.setup_working_dir()
    print(f"      Working dir: {fea.working_dir}", flush=True)

    errs = fea.check_prerequisites()
    if errs:
        print(f"      Prerequisites: {errs}", flush=True)
        return
    print("      Prerequisites OK", flush=True)

    fea.write_inp_file()
    print(f"      INP: {fea.inp_file_name}", flush=True)

    print("[6/6] Running CalculiX...", flush=True)
    fea.run()

    # Load results back into FreeCAD
    fea.load_results()
    doc.recompute()
    doc.saveAs(os.path.abspath("ValveSpring_FEA.FCStd"))
    print("Saved: ValveSpring_FEA.FCStd", flush=True)

    print("=== Simulation complete — opening results in FreeCAD GUI ===", flush=True)

try:
    run()
except Exception:
    traceback.print_exc()
