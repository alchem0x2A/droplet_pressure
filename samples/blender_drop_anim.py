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
    curv_obj = bpy.data.objects.new("curveobj", curvData)
    mod = curv_obj.modifiers.new("screw", "SCREW")
    mod.use_smooth_shade = True
    mod.steps = 64
    mod.use_normal_flip = True #    
    return curv_obj

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

def add_shape_keys(curv_obj, param_lists):
    """Add shape keys for each single frames
    param_list is already the params without first line
    """
    curv_obj.shape_key_add("basis")
    curv_obj.data.shape_keys.use_relative = False
    for i, params in enumerate(param_lists):
        verts = gen_verts(params)
        key = curv_obj.shape_key_add("step-{}".format(i))
        for j, v in enumerate(verts):
            x, y, z = v
            key.data[j].co = (x, y, z)
    
    return
    
def gen_timeline(curv_obj, 
                 other_obj=None, #another object to align
                 start_frame=1,
                 period=5, stop=1, repeat=4):
    # default
    sk = curv_obj.data.shape_keys
    keys = curv_obj.data.shape_keys.key_blocks
    max_eval_time = keys[-1].frame #the eval_time
    for i in range(repeat):
        start = start_frame + (period + stop) * 2 * i
        tp1 = start + period
        tp2 = tp1 + stop
        tp3 = tp2 + period
        sk.eval_time = 0
        sk.keyframe_insert("eval_time", frame=start)
        sk.keyframe_insert("eval_time", frame=tp3)
        sk.eval_time = max_eval_time
        sk.keyframe_insert("eval_time", frame=tp1)
        sk.keyframe_insert("eval_time", frame=tp2)
    if other_obj is not None:
        for i in range(repeat):
            start = start_frame + (period + stop) * 2 * i
            tp1 = start + period
            tp2 = tp1 + stop
            tp3 = tp2 + period
            bpy.context.scene.frame_set(start)
            other_obj.location.z = curv_obj.location.z \
                                   + curv_obj.dimensions.z
            other_obj.keyframe_insert("location", frame=start)
            other_obj.keyframe_insert("location", frame=tp3)
            bpy.context.scene.frame_set(tp1)
            other_obj.location.z = curv_obj.location.z \
                                   + curv_obj.dimensions.z
            other_obj.keyframe_insert("location", frame=tp1)
            other_obj.keyframe_insert("location", frame=tp2)
    return
        
    
    
    
        


f_name = "/Users/tiantian/polybox/Research/3-(Done)-graphene-F16CuPc-hydrophobic/droplet-pressure/results/blender_input.csv"
z_shift = 0.72
param_lines = read_csv(f_name)
curv_obj = gen_revolved(gen_verts(param_lines[0]))
scene = bpy.context.scene
scene.objects.link(curv_obj)
curv_obj.layers[1] = True
curv_obj.data.materials.append(bpy.data.materials["Hg"])
add_shape_keys(curv_obj, param_lines[1:])
curv_obj.location = (0, 0, z_shift)
gen_timeline(curv_obj, other_obj=bpy.data.objects["drain"],
             start_frame=22)



