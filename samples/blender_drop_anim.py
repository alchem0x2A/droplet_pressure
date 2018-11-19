import bpy
import bmesh
import numpy

def gen_revolved(verts):
    """Generate revolved shape using vertices
    """
    curvData = bpy.data.curves.new("curve", type="CURVE")
    curvData.dimensions="3D"
    poly = curvData.splines.new("POLY")
    poly.points.add(len(verts))
    # Add vertices to the curve
    for i in range(len(verts)):
        x, y, z = verts[i]
        poly.points[i].co = (x, y, z, 1)
    curvOBJ = bpy.data.objects.new("curveobj", curvData)
    mod = curvOBJ.modifiers.new("screw", "SCREW")
    mod.use_smooth_shade = True
    mod.steps = 64
    mod.use_normal_flip = True #    
    return curvOBJ

    
verts = [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)] #test vertices
curvOBJ = gen_revolved(verts)
scene = bpy.context.scene
scene.objects.link(curvOBJ)
curvOBJ.layers[1] = True



