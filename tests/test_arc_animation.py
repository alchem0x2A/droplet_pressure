import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Path, PathPatch, Circle, FancyArrowPatch
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
import numpy
from numpy import pi
import time

fig = plt.figure()
ax = fig.add_subplot(111, aspect="equal")
ax.set_xlim(-2, 2)
ax.set_ylim(-1.5, 1.5)

def gen_arc(center, r, theta1, theta2):
    t = numpy.linspace(theta1, theta2, 64)
    vert = r * numpy.vstack((numpy.cos(t),
                             numpy.sin(t))).T
    return vert + center

def gen_patch(x):

    v1 = gen_arc((x, 0), 1, numpy.radians(-45), numpy.radians(45))
    v2 = gen_arc((-x, 0), 1, numpy.radians(135), numpy.radians(225))

    verts = numpy.concatenate((v1, v2, (v1[0], v1[0])))
    codes = [1] + [2] * (63 + 64 + 1) + [79]

    patch = PathPatch(Path(verts, codes))
    patch.set_alpha(0.5)
    return patch, v1[-1]        # last point

def init():
    patch, p= gen_patch(1)
    x=0
    circle = Circle((x, 0), radius=1,
                    ls="--", fill=False,
                    edgecolor="red")

    arr1 = FancyArrowPatch((0, 0), (x+1, 0),
                           mutation_scale=30,
                           linewidth=0,
                           facecolor="gray")

    arr2 = FancyArrowPatch((x, 0), p,
                           mutation_scale=30,
                           linewidth=0,
                           facecolor="gray")
    ax.add_patch(patch)
    ax.add_patch(circle)
    ax.add_patch(arr1)
    ax.add_patch(arr2)
    return ax.patches

def update(i):
    ax.patches = []
    patches = []
    x = i*0.05
    patch, p = gen_patch(x)

    circle = Circle((x, 0), radius=1,
                    ls="--", fill=False,
                    edgecolor="red")

    arr1 = FancyArrowPatch((0, 0), (x+1, 0),
                           mutation_scale=30,
                           linewidth=0,
                           facecolor="gray")

    arr2 = FancyArrowPatch((x, 0), p,
                           mutation_scale=30,
                           linewidth=0,
                           facecolor="gray")
    ax.add_patch(patch)
    ax.add_patch(circle)
    ax.add_patch(arr1)
    ax.add_patch(arr2)
    return ax.patches

anim = FuncAnimation(fig, func=update, init_func=init, frames=25)
plt.show()
    
# ax.add_collection(collect)
# plt.ion()
# plt.show()
# time.sleep(10)
# plt.close()
