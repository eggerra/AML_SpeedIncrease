"""
Abaqus CAE noGUI script — mesh ValveSpring_oval.step at 0.5 mm global size.
Run as: abaqus cae noGUI=mesh_abaqus_hpc.py
Output: ValveSpring_abq_mesh.inp (orphan mesh, C3D10)
"""
from abaqus import *
from abaqusConstants import *
from caeModules import *
from mesh import ElemType
import sys, os

STEP_FILE   = os.path.join(os.getcwd(), 'ValveSpring_oval.step')
JOB_NAME    = 'ValveSpring_abq_mesh'
GLOBAL_SIZE = 0.25

print('=== Abaqus CAE mesh script ===')
print('STEP : ' + STEP_FILE)
print('Size : ' + str(GLOBAL_SIZE) + ' mm')

# Import STEP -> AcisFile object
acis = mdb.openStep(STEP_FILE, scaleFromFile=OFF)

# Create a deformable part from the geometry
p = mdb.models['Model-1'].PartFromGeometryFile(
    name='ValveSpring',
    geometryFile=acis,
    combine=False,
    dimensionality=THREE_D,
    type=DEFORMABLE_BODY,
    scale=1.0,
)

n_cells = len(p.cells)
n_faces = len(p.faces)
print('Part cells : ' + str(n_cells))
print('Part faces : ' + str(n_faces))

if n_cells == 0:
    print('ERROR: no solid cells in imported geometry')
    sys.exit(1)

# Assign quadratic tet element type (C3D10)
p.setMeshControls(regions=p.cells, elemShape=TET, technique=FREE)
p.setElementType(
    regions=(p.cells,),
    elemTypes=(
        ElemType(elemCode=C3D10, elemLibrary=STANDARD),
        ElemType(elemCode=C3D6,  elemLibrary=STANDARD),
        ElemType(elemCode=C3D4,  elemLibrary=STANDARD),
    )
)

# Global seed at 0.5 mm
p.seedPart(size=GLOBAL_SIZE, deviationFactor=0.1, minSizeFactor=0.1)

# Generate mesh
p.generateMesh()

n_nodes = len(p.nodes)
n_elems = len(p.elements)
print('Nodes    : ' + str(n_nodes))
print('Elements : ' + str(n_elems))

if n_nodes == 0:
    print('ERROR: mesh generation produced 0 nodes')
    sys.exit(1)

# Detect actual element type from first element
first_elem = p.elements[0]
conn_len = len(first_elem.connectivity)
if conn_len == 10:
    elem_type = 'C3D10'
elif conn_len == 4:
    elem_type = 'C3D4'
else:
    elem_type = 'C3D' + str(conn_len)
print('Elem type: ' + elem_type + ' (' + str(conn_len) + ' nodes/elem)')

# Renumber nodes 1..N and elements 1..M — avoids any 0-based label ambiguity.
# elem.connectivity returns node labels (per Abaqus docs), but some versions
# return 0-based indices; rebuilding from scratch is safest.
nodes_list = list(p.nodes)
elems_list = list(p.elements)

# Map original node object -> sequential label 1..N
node_new_label = {}
for i, nd in enumerate(nodes_list):
    node_new_label[nd.label] = i + 1

out_path = os.path.join(os.getcwd(), JOB_NAME + '.inp')
with open(out_path, 'w') as f:
    f.write('*NODE\n')
    for i, nd in enumerate(nodes_list):
        c = nd.coordinates
        f.write('%d, %.6f, %.6f, %.6f\n' % (i + 1, c[0], c[1], c[2]))
    f.write('*ELEMENT, TYPE=' + elem_type + ', ELSET=Evolumes\n')
    for i, elem in enumerate(elems_list):
        # connectivity holds 0-based positional indices into p.nodes;
        # our renumbering assigns new label = index + 1
        conn = ', '.join(str(n + 1) for n in elem.connectivity)
        f.write('%d, %s\n' % (i + 1, conn))
print('Written  : ' + out_path)
print('=== Done ===')
