import bpy
import bmesh
import numpy
from math import pi, sin, cos
import os, os.path

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

def gen_verts(params, h0=1.7, resolution=64):
    per, x0, y0, r2, t_b, t_t = params
    x0 = x0 * h0
    y0 = y0 * h0
    r2 = r2 * h0
    verts = []
    # Add initial
    verts.append([0, 0, 0])
    # Add circles
    for t in numpy.linspace(-(t_b - pi / 2), (t_t - pi / 2), resolution):
        verts.append([0, x0 + r2 * cos(t), y0 + r2 * sin(t)])
    # Final point
    verts.append([0, 0, per * h0])
    return verts
        
def read_csv(f_name):
    param_lines = numpy.genfromtxt(f_name, 
                                   comments="#", 
                                   delimiter=",")
    return param_lines

f_name = "/Users/tiantian/polybox/Research/3-(Done)-graphene-F16CuPc-hydrophobic/droplet-pressure/results/blender_input.csv"
z_shift = 0.72
#verts = [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)] #test vertices
param_lines = read_csv(f_name)
curvOBJ = gen_revolved(gen_verts(param_lines[0]))
scene = bpy.context.scene
scene.objects.link(curvOBJ)
curvOBJ.layers[1] = True
curvOBJ.location = (0, 0, z_shift)



