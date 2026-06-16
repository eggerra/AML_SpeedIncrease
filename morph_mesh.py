"""
morph_mesh.py — Remap Z coordinates of existing spring mesh to match new L0 / n_closed.

The existing mesh (ValveSpring_abq_mesh.inp, n_closed=1.25, L0=47.43mm) is the only
working mesh.  All direct re-meshing attempts fail (Abaqus CAE noGUI: 0 nodes; Gmsh:
0 volume elements; Netgen OCC: triangulation fails on face 2; Netgen STL: stalls).

Strategy: piecewise-linear Z-mapping preserves element connectivity.
  Zone 1  bottom grind  [0,      grind_z]       → unchanged
  Zone 2  bottom closed [grind_z, h_closed_old] → remap to [grind_z, h_closed_new]
  Zone 3  active zone   [h_closed_old, L-h_c_old] → remap to [h_closed_new, L-h_c_new]
  Zone 4  top closed    [L-h_c_old, L-grind_z]  → remap to [L-h_c_new, L-grind_z_new]
  Zone 5  top grind     [L-grind_z, L_old]      → remap to [L-grind_z, L_new]

X, Y coordinates are unchanged (beehive radius profile unchanged).
"""
import os, sys

BASE = r"D:\Projects_AI\AML_SpeedIncrease"

# Original mesh parameters (ValveSpring_abq_mesh.inp, n_closed=1.25, L0=47.43mm)
L0_OLD      = 47.43
N_CLOSED_OLD = 1.25
WIRE_A       = 2.92
GRIND_Z      = 0.75

H_CLOSED_OLD = N_CLOSED_OLD * WIRE_A    # 3.65 mm
Z_BOUNDS_OLD = [
    0.0,
    GRIND_Z,                             # 0.75
    H_CLOSED_OLD,                        # 3.65
    L0_OLD - H_CLOSED_OLD,              # 43.78
    L0_OLD - GRIND_Z,                   # 46.68
    L0_OLD,                             # 47.43
]


def remap_z(z_old, z_bounds_old, z_bounds_new):
    """Map a single Z coordinate from old geometry to new via piecewise-linear zones."""
    for i in range(len(z_bounds_old) - 1):
        z0, z1 = z_bounds_old[i], z_bounds_old[i + 1]
        if z0 <= z_old <= z1:
            if z1 == z0:
                return z_bounds_new[i]
            t = (z_old - z0) / (z1 - z0)
            return z_bounds_new[i] + t * (z_bounds_new[i + 1] - z_bounds_new[i])
    # Extrapolate for nodes slightly outside range (grind nodes)
    if z_old < z_bounds_old[0]:
        return z_bounds_new[0] + (z_old - z_bounds_old[0])
    return z_bounds_new[-1] + (z_old - z_bounds_old[-1])


def morph(src_inp, dst_inp, L0_new, n_closed_new):
    h_closed_new = n_closed_new * WIRE_A
    z_bounds_new = [
        0.0,
        GRIND_Z,
        h_closed_new,
        L0_new - h_closed_new,
        L0_new - GRIND_Z,
        L0_new,
    ]
    print(f"  Morphing: L0={L0_OLD} -> {L0_new}mm, n_closed={N_CLOSED_OLD} -> {n_closed_new}")
    print(f"  Z zones old: {[f'{v:.3f}' for v in Z_BOUNDS_OLD]}")
    print(f"  Z zones new: {[f'{v:.3f}' for v in z_bounds_new]}")

    # Parse INP — preserve all non-node lines verbatim
    lines_out = []
    node_mode = False
    n_nodes = 0
    z_min_old, z_max_old = float('inf'), float('-inf')
    z_min_new, z_max_new = float('inf'), float('-inf')

    with open(src_inp) as fh:
        for line in fh:
            stripped = line.strip()
            up = stripped.upper()

            if up.startswith('*NODE') and 'PRINT' not in up and 'FILE' not in up:
                node_mode = True
                lines_out.append(line)
                continue
            elif up.startswith('*') and node_mode:
                node_mode = False

            if node_mode:
                parts = stripped.split(',')
                if len(parts) >= 4:
                    try:
                        nid = parts[0].strip()
                        x   = float(parts[1])
                        y   = float(parts[2])
                        z   = float(parts[3])
                        z_min_old = min(z_min_old, z)
                        z_max_old = max(z_max_old, z)
                        z_new = remap_z(z, Z_BOUNDS_OLD, z_bounds_new)
                        z_min_new = min(z_min_new, z_new)
                        z_max_new = max(z_max_new, z_new)
                        lines_out.append(f'{nid}, {x:.6f}, {y:.6f}, {z_new:.6f}\n')
                        n_nodes += 1
                        continue
                    except ValueError:
                        pass

            lines_out.append(line)

    with open(dst_inp, 'w') as fh:
        fh.writelines(lines_out)

    sz = os.path.getsize(dst_inp)
    print(f"  Nodes morphed: {n_nodes:,}  Z old=[{z_min_old:.3f},{z_max_old:.3f}] -> "
          f"new=[{z_min_new:.3f},{z_max_new:.3f}]")
    print(f"  Written: {dst_inp}  ({sz // 1024} kB)")
    return n_nodes


if __name__ == '__main__':
    SRC = os.path.join(BASE, 'ValveSpring_abq_mesh.inp')
    if not os.path.isfile(SRC):
        sys.exit(f'ERROR: source mesh not found: {SRC}')

    # Support single-case mode: morph_mesh.py <dst_path> <L0> <n_closed>
    if len(sys.argv) == 4:
        dst      = sys.argv[1]
        L0_new   = float(sys.argv[2])
        nc_new   = float(sys.argv[3])
        print(f'=== {os.path.basename(dst)} ===')
        morph(SRC, dst, L0_new, nc_new)
        print('=== Done ===')
    else:
        # Default: generate all three sweep cases
        cases = [
            ('ValveSpring_250N_mesh.inp', 47.58, 0.8),
            ('ValveSpring_265N_mesh.inp', 48.26, 0.8),
            ('ValveSpring_280N_mesh.inp', 48.95, 0.8),
        ]
        for fname, L0_new, nc_new in cases:
            dst = os.path.join(BASE, fname)
            print(f'\n=== {fname} ===')
            morph(SRC, dst, L0_new, nc_new)
        print('\n=== All morphs done ===')
