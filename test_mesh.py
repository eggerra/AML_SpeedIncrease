import sys
sys.path.append('.')
import FreeCAD, ObjectsFem
doc = FreeCAD.newDocument()
solver = ObjectsFem.makeSolverCalculiXCcxTools(doc, "CalculiX")
print([p for p in solver.PropertiesList if 'Time' in p or 'Nonlin' in p or 'Geom' in p or 'Iter' in p or 'Incr' in p])
