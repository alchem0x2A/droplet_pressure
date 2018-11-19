import droplet_pressure
from droplet_pressure.droplet import Droplet
import numpy
from numpy import sin, cos, radians, pi
import os
from os.path import abspath


def gen_params(drop, h):
    """Generate parameters for visualizing the droplet
    Required params:
    r1, r2, delta_b, theta_t, theta_b.
    All lengthes scaled by h0
    """
    h0 = drop.h0
    drop.h = h
    delta_t, delta_b = drop.get_separate_height()
    r1 = drop.r1; r2 = drop.r2
    t_t = drop.theta_t; t_b = drop.theta_b
    params_pack = (h / h0,      # percentage?
                   (r1 - r2) / h0,  # x for center of C2
                   delta_b / h0,
                   r2 / h0, t_b, t_t)     # r2 and two angles
    return params_pack

def main(vol=3.0e-10,
         frames=8,
         theta_t=radians(145),
         theta_b=radians(165),
         max_strain=0.25):
    drop = Droplet(initial_volume=vol,
                   theta_t=theta_t,
                   theta_b=theta_b)
    h0 = drop.h0
    lines = []
    lines.append("#Percentage,x0,y0,r2,theta_b,theta_t\n")
    for h in numpy.linspace(h0, h0 * (1- max_strain), frames):
        params = gen_params(drop, h)
        line = ",".join(map(lambda s: "{:.3f}".format(s),
                            params)) + "\n"
        lines.append(line)
    curr_dir = os.path.dirname(abspath(__file__))
    f_name = os.path.join(curr_dir, "../results", "blender_input.csv")
    with open(f_name, "w") as f:
        f.writelines(lines)

    return


if __name__ == "__main__":
    main()
