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
    analysis = ObjectsFem.makeAnalysis(doc, "ModalAnalysis")

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
    mesh_obj = ObjectsFem.makeMeshGmsh(doc, "FEMMesh_Modal")
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
        print("ERROR: No volume elements generated.", flush=True)
        return

    print("[5/7] Applying fixed boundary condition (bottom face)...", flush=True)
    faces = spring.Shape.Faces
    z_vals = [(i+1, f.CenterOfMass.z) for i, f in enumerate(faces)]
    z_vals.sort(key=lambda x: x[1])
    bottom_face_idx = z_vals[0][0]
    print(f"      Bottom face {bottom_face_idx} z={z_vals[0][1]:.2f}", flush=True)

    fixed = ObjectsFem.makeConstraintFixed(doc, "FixedBottom_Modal")
    fixed.References = [(spring, f"Face{bottom_face_idx}")]
    analysis.addObject(fixed)

    print("[6/7] Configuring CalculiX solver for modal analysis...", flush=True)
    solver = ObjectsFem.makeSolverCalculiXCcxTools(doc, "CalculiX_Modal")
    solver.AnalysisType = "frequency"
    solver.EigenmodesCount = 10
    solver.GeometricalNonlinearity = "linear"
    analysis.addObject(solver)
    doc.recompute()

    print("[7/7] Running CalculiX modal analysis...", flush=True)
    fea = ccxtools.CcxTools()
    fea.analysis = analysis
    fea.solver = solver
    fea.update_objects()
    fea.setup_working_dir()
    print(f"      Working dir: {fea.working_dir}", flush=True)

    errors = fea.check_prerequisites()
    if errors:
        print(f"      Prerequisites errors: {errors}", flush=True)
        return
    print("      Prerequisites OK", flush=True)

    fea.write_inp_file()
    print(f"      INP file written: {fea.inp_file_name}", flush=True)

    ret = fea.run()
    print(f"      Solver return code: {ret}", flush=True)

    # Parse .dat file for eigenfrequencies
    wd = fea.working_dir
    dat_file = os.path.join(wd, "FEMMesh_Modal.dat")
    if not os.path.exists(dat_file):
        dat_file = os.path.join(wd, "FEMMesh.dat")

    frequencies = []
    if os.path.exists(dat_file):
        print(f"\n=== Parsing {dat_file} for eigenfrequencies ===", flush=True)
        with open(dat_file, 'r', errors='replace') as f:
            content = f.read()
        print(content, flush=True)
        # Parse frequency lines: look for "E I G E N V A L U E" or frequency output
        for line in content.splitlines():
            line = line.strip()
            # CalculiX dat output: "     1   <eigenvalue>   <freq_rad/s>   <freq_hz>   <damping>"
            parts = line.split()
            if len(parts) >= 3:
                try:
                    mode_num = int(parts[0])
                    freq_hz = float(parts[2])
                    if 1 <= mode_num <= 20 and freq_hz > 0:
                        frequencies.append((mode_num, freq_hz))
                except (ValueError, IndexError):
                    pass

    # Also check all small files
    if os.path.exists(wd):
        for fname in sorted(os.listdir(wd)):
            fpath = os.path.join(wd, fname)
            size = os.path.getsize(fpath)
            if size > 0 and size < 200000 and fname.endswith(('.dat', '.sta', '.cvg')):
                print(f"\n=== {fname} ({size} bytes) ===", flush=True)
                with open(fpath, 'r', errors='replace') as f:
                    print(f.read(), flush=True)

    print("\n--- Modal Analysis Results ---", flush=True)
    if frequencies:
        print(f"{'Mode':>6} {'Frequency (Hz)':>16} {'Frequency (rpm)':>18}", flush=True)
        print("-" * 44, flush=True)
        for mode, freq in frequencies:
            print(f"{mode:>6} {freq:>16.2f} {freq*60:>18.1f}", flush=True)
        print(f"\nEngine speed: 7500 rpm = 125 Hz", flush=True)
        if frequencies:
            f1 = frequencies[0][1]
            print(f"1st natural frequency: {f1:.2f} Hz", flush=True)
            print(f"Safety margin: {f1/125:.2f}x engine excitation", flush=True)
    else:
        print("No frequencies parsed from .dat file.", flush=True)

    doc.saveAs("ValveSpring_Modal_Results.FCStd")
    print("\nSaved to ValveSpring_Modal_Results.FCStd", flush=True)

try:
    run()
except Exception:
    traceback.print_exc()
