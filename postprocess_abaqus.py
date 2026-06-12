"""postprocess_abaqus.py
=======================
Abaqus Python post-processor: extract nodal reaction forces from .odb.

Run as:
    abaqus python postprocess_abaqus.py <jobname>

Writes:
    <jobname>_rf.txt   — two-column text:  compression_s[mm]  force[N]
                         compression_s = cumulative step time (= mm compression from L0)
"""
import sys
import os


def main():
    job = sys.argv[1] if len(sys.argv) > 1 else "ValveSpring_oval_contact_abaqus"
    odb_path = job + ".odb"
    out_path = job + "_rf.txt"

    try:
        import odbAccess                 # available only inside  abaqus python
    except ImportError:
        print("ERROR: odbAccess not available.  Run as:  abaqus python postprocess_abaqus.py <job>")
        sys.exit(1)

    if not os.path.isfile(odb_path):
        print(f"ERROR: ODB not found: {odb_path}")
        sys.exit(1)

    print(f"Opening ODB: {odb_path}")
    odb = odbAccess.openOdb(odb_path, readOnly=True)
    assy = odb.rootAssembly

    # ------------------------------------------------------------------
    # Locate NBOT node set (assembly level first, then instance level)
    # ------------------------------------------------------------------
    nset = None
    if "NBOT" in assy.nodeSets:
        nset = assy.nodeSets["NBOT"]
        print("  Found NBOT at assembly level")
    else:
        for inst_name in assy.instances.keys():
            inst = assy.instances[inst_name]
            if "NBOT" in inst.nodeSets:
                nset = inst.nodeSets["NBOT"]
                print(f"  Found NBOT in instance: {inst_name}")
                break

    if nset is None:
        print("ERROR: NBOT node set not found in ODB")
        odb.close()
        sys.exit(1)

    # ------------------------------------------------------------------
    # Extract RF3 (Z-direction reaction force) from every output frame
    # ------------------------------------------------------------------
    results = []
    cumulative_time = 0.0

    for step_name in odb.steps.keys():
        step = odb.steps[step_name]
        print(f"  Step '{step_name}':  {len(step.frames)} frames  "
              f"(period={step.timePeriod:.3f} mm)")

        for frame in step.frames:
            # Skip initial (zero-time) frame of each step
            if frame.frameId == 0 and frame.frameValue == 0.0:
                continue

            if "RF" not in frame.fieldOutputs:
                continue

            t = cumulative_time + frame.frameValue

            rf_field = frame.fieldOutputs["RF"]
            rf_sub   = rf_field.getSubset(region=nset)

            # Sum Z-components over all NBOT nodes
            rf3 = 0.0
            for v in rf_sub.values:
                # v.data is (RF1, RF2, RF3) for 3-D
                rf3 += v.data[2]

            force = abs(rf3)
            # Skip frames with non-physical RF (solid-height lock-up produces overflow values)
            if force < 1e6:
                results.append((t, force))
            else:
                print(f"    Skipped frame at t={t:.3f} mm: RF={force:.3e} N (non-physical)")

        cumulative_time += step.timePeriod

    odb.close()

    if not results:
        print("ERROR: no reaction-force data extracted from ODB")
        sys.exit(1)

    results.sort(key=lambda x: x[0])

    with open(out_path, "w") as fh:
        fh.write("# compression_s[mm]  force[N]\n")
        for t, F in results:
            fh.write(f"{t:.6f}  {F:.4f}\n")

    print(f"Wrote {len(results)} data points -> {out_path}")
    print(f"  Compression range : {results[0][0]:.2f} – {results[-1][0]:.2f} mm")
    print(f"  Force range       : {results[0][1]:.1f} – {results[-1][1]:.1f} N")


if __name__ == "__main__":
    main()
