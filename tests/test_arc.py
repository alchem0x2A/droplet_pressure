import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Path, PathPatch, Circle, FancyArrowPatch
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

v1 = gen_arc((1, 0), 1, numpy.radians(-45), numpy.radians(45))
v2 = gen_arc((-1, 0), 1, numpy.radians(135), numpy.radians(225))

verts = numpy.concatenate((v1, v2, (v1[0], v1[0])))
codes = [1] + [2] * (63 + 64 + 1) + [79]

# code2.setflags(write=True)
# code2[0] = 2
# codes = numpy.concatenate((code1, code2))
# verts = numpy.concatenate((v1, v2))
# print(v1, code1)
# print(v2, code2)
# print(verts, codes)
patch = PathPatch(Path(verts, codes))
patch.set_alpha(0.5)

circle = Circle((1, 0), radius=1,
                ls="--", fill=False,
                edgecolor="red")

arr1 = FancyArrowPatch((0, 0), (2, 0),
                       mutation_scale=30,
                       linewidth=0,
                       facecolor="gray")

arr2 = FancyArrowPatch((1, 0), v1[-1],
                       mutation_scale=30,
                       linewidth=0,
                       facecolor="gray")
# collect = PatchCollection([patch, circle], alpha=0.2)
# ax.add_patch(arc1)
# ax.add_patch(arc2)
ax.add_patch(patch)
ax.add_patch(circle)
ax.add_patch(arr1)
ax.add_patch(arr2)
assert len(ax.patches) == 4
# ax.add_collection(collect)
# plt.ion()
# plt.show()
# time.sleep(10)
# plt.close()
