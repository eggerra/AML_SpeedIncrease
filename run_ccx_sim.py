import sys, os, traceback
sys.path.append('.')
import FreeCAD, ObjectsFem
from femmesh import gmshtools
from femtools import ccxtools

def run():
    print("[1/7] Opening CAD model...", flush=True)
    doc = FreeCAD.open("ValveSpring.FCStd")
    spring = doc.getObject("Spring")
    print(f"      Spring volume: {spring.Shape.Volume:.1f} mm^3", flush=True)

    print("[2/7] Creating Analysis container...", flush=True)
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

    print("[3/7] Adding material...", flush=True)
    mat = ObjectsFem.makeMaterialSolid(doc, "Material")
    mat.Material = {
        "Name": "VD_SiCrNiV_SC",
        "YoungsModulus": "206000 MPa",
        "PoissonRatio": "0.3",
        "Density": "7850 kg/m^3",
    }
    analysis.addObject(mat)

    print("[4/7] Generating solid tetrahedral mesh with Gmsh...", flush=True)
    mesh_obj = ObjectsFem.makeMeshGmsh(doc, "FEMMesh")
    mesh_obj.Shape = spring
    mesh_obj.CharacteristicLengthMax = "2.0 mm"
    mesh_obj.CharacteristicLengthMin = "0.8 mm"
    mesh_obj.ElementOrder = "2nd"
    mesh_obj.ElementDimension = "3D"
    analysis.addObject(mesh_obj)
    doc.recompute()

    gm = gmshtools.GmshTools(mesh_obj)
    error = gm.create_mesh()
    print(f"      Gmsh error: {error}", flush=True)
    print(f"      NodeCount: {mesh_obj.FemMesh.NodeCount}", flush=True)
    print(f"      VolumeCount: {mesh_obj.FemMesh.VolumeCount}", flush=True)

    if mesh_obj.FemMesh.VolumeCount == 0:
        print("ERROR: No volume elements generated. Cannot run FEA.", flush=True)
        return

    print("[5/7] Applying boundary conditions...", flush=True)
    L0 = 46.1
    faces = spring.Shape.Faces
    z_vals = [(i+1, f.CenterOfMass.z) for i, f in enumerate(faces)]
    z_vals.sort(key=lambda x: x[1])
    bottom_face_idx = z_vals[0][0]
    top_face_idx = z_vals[-1][0]
    print(f"      Bottom face {bottom_face_idx} z={z_vals[0][1]:.2f}, Top face {top_face_idx} z={z_vals[-1][1]:.2f}", flush=True)

    fixed = ObjectsFem.makeConstraintFixed(doc, "FixedBottom")
    fixed.References = [(spring, f"Face{bottom_face_idx}")]
    analysis.addObject(fixed)

    displ = ObjectsFem.makeConstraintDisplacement(doc, "DisplacementTop")
    displ.References = [(spring, f"Face{top_face_idx}")]
    displ.zFree = False
    displ.zDisplacement = -10.0
    displ.xFree = False
    displ.xDisplacement = 0.0
    displ.yFree = False
    displ.yDisplacement = 0.0
    analysis.addObject(displ)

    print("[6/7] Configuring CalculiX solver...", flush=True)
    solver = ObjectsFem.makeSolverCalculiXCcxTools(doc, "CalculiX")
    solver.GeometricalNonlinearity = "nonlinear"
    solver.IterationsControlParameterTimeUse = True
    solver.TimeInitialIncrement = 0.1
    solver.TimePeriod = 1.0
    solver.IncrementsMaximum = 20
    analysis.addObject(solver)
    doc.recompute()

    print("[7/7] Running CalculiX...", flush=True)
    fea = ccxtools.CcxTools()
    fea.analysis = analysis
    fea.solver = solver
    fea.update_objects()
    fea.setup_working_dir()
    print(f"      Working dir: {fea.working_dir}", flush=True)

    errors = fea.check_prerequisites()
    if errors:
        print(f"      Prerequisites errors: {errors}", flush=True)
    else:
        print("      Prerequisites OK", flush=True)

    fea.write_inp_file()
    print(f"      INP file written: {fea.inp_file_name}", flush=True)

    if os.path.exists(fea.inp_file_name):
        with open(fea.inp_file_name, 'r') as f:
            lines = f.readlines()
        print(f"      INP lines: {len(lines)}", flush=True)
        print("      --- INP preview (first 40 lines) ---", flush=True)
        for line in lines[:40]:
            print(f"      {line.rstrip()}", flush=True)

    ret = fea.run()
    print(f"      Solver return code: {ret}", flush=True)

    # Print all output files
    wd = fea.working_dir
    if os.path.exists(wd):
        for fname in sorted(os.listdir(wd)):
            fpath = os.path.join(wd, fname)
            size = os.path.getsize(fpath)
            print(f"\n=== {fname} ({size} bytes) ===", flush=True)
            if size > 0 and size < 100000 and fname.endswith(('.log', '.dat', '.frd', '.cvg', '.sta')):
                with open(fpath, 'r', errors='replace') as f:
                    print(f.read(), flush=True)

    doc.saveAs("ValveSpring_CCX_Run.FCStd")
    print("\nSaved to ValveSpring_CCX_Run.FCStd", flush=True)

try:
    run()
except Exception:
    traceback.print_exc()
