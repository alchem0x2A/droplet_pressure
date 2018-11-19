from droplet_pressure.droplet import Droplet
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Path, PathPatch, Circle, FancyArrowPatch
from matplotlib.animation import FuncAnimation, FFMpegFileWriter, FFMpegWriter
import numpy
from numpy import pi, sin, cos, radians
from scipy.stats import linregress
import os
from os.path import abspath, dirname, join

def gen_patches(drop, h, resolution=64):
    """Generate patches for droplet at height h
    """
    # Generate arc starting form theta1 to theta2
    def gen_arc(center, r, theta1, theta2):
        t = numpy.linspace(theta1, theta2, resolution)
        vert = r * numpy.vstack((numpy.cos(t),
                                 numpy.sin(t))).T
        return vert + center
    print(h)
    drop.h = h                  # set height and update
    delta_t, delta_b = drop.get_separate_height()
    r1 = drop.r1; r2 = drop.r2
    t_t = drop.theta_t; t_b = drop.theta_b
    center_r = (r1 - r2, delta_b)
    center_l = (-(r1 - r2), delta_b)
    v_r = gen_arc(center_r, r2,
                  -(t_b - pi / 2), (t_t - pi / 2))
    v_l = gen_arc(center_l, r2,
                  pi - (t_t - pi / 2),
                  pi + (t_b - pi / 2))
    p_b = v_r[0]; p_t = v_r[-1]
    verts = numpy.concatenate((v_r, v_l, (p_b, p_b)))  # vertices for patch
    codes = [Path.MOVETO] + [Path.LINETO] * (resolution * 2) \
            + [Path.CLOSEPOLY]  # codes for path
    drop_patch = PathPatch(Path(verts, codes),
                           facecolor="#ccdfff")
    drop_patch.set_alpha(0.5)
    circle = Circle(center_r, radius=r2,
                    ls="--", fill=False,
                    linewidth=0.5,
                    edgecolor="#ffb4a5")

    arr1 = FancyArrowPatch((0, delta_b), (r1, delta_b),
                           mutation_scale=10,
                           linewidth=0,
                           facecolor="#9b9b9b")
    
    arr2 = FancyArrowPatch(center_r, p_t,
                           mutation_scale=10,
                           linewidth=0,
                           facecolor="#ffa047")

    pressure = drop.get_delta_stress()
    pr = (r1, delta_b)
    print(pr, p_t)
    return drop_patch, circle, arr1, arr2, \
           pressure, pr, p_t

def main(vol=3.0e-10,
         theta_t=radians(145),
         theta_b=radians(165),
         total_frames=50,
         final_frames=4,
         show=False):
    drop = Droplet(initial_volume=vol,
                   theta_t=theta_t,
                   theta_b=theta_b)
    h0 = drop.h0
    print(h0)
    fig = plt.figure(figsize=(6, 3))
    plt.style.use("science")
    # Setup acis
    ax1 = fig.add_subplot(121, aspect="equal")
    plt.setp(ax1.spines.values(), linewidth=0.5)
    ax2 = fig.add_subplot(122)
    ax1.set_ylim(-h0 * 0.05, h0 * 1.25)
    ax1.set_xlim(-h0 * 0.75, h0 * 0.75)
    ax1.set_xlabel("$r$"); ax1.set_ylabel("$z$")
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.axvline(x=0.0, ls="--",
                color="#e3e9f2", alpha=0.5,
                zorder=20)
    # ax1.set_axis_off()
    ax1.set_title(("Laplace Pressure $p = "
                   " \\gamma (R_{1}^{-1} + R_{2}^{-1})$"))
    ax2.set_xlim(0, 0.25)
    ax2.set_ylim(0, 300)
    ax2.set_xlabel("Strain")
    ax2.set_ylabel("Stress (Pa)")
    # access patches
    dp, c, arr1, arr2, pre, pr, pt = gen_patches(drop, h0)
    patches = [ax1.add_patch(p) for p in (dp, c, arr1, arr2)]
    line,  = ax2.plot([0], [pre], "-")
    patches.append(line)
    text1 = ax1.annotate(xy=pr, s="$R_{1}$",
                         ha="left", va="center",
                         color="#9b9b9b")
    text2 = ax1.annotate(xy=pt, s="$R_{2}$",
                         ha="left",
                         va="bottom",
                         color="#ffa047")
    patches += [text1, text2]
    # # Additional for plotting the linear regression
    reg_line, = ax2.plot([], [], "--",
                        color="#ffae51")
    text3 = ax2.annotate(xy=(0, 0), s="", color="black")
    patches += [reg_line, text3]
    print(len(patches))
    reg_xy = [None, None]
    
    # update frames
    # limit to 0.25 * h
    def update(i):
        print(i)
        if i < (total_frames - final_frames):
            # update the patches and pressure only
            h = h0 - 0.25 / (total_frames - final_frames - 1) * i * h0
            sigma = 1 - h / h0
            ax1.patches = []
            dp, c, arr1, arr2, pre, pr, pt = gen_patches(drop, h)
            patches[:4] = [ax1.add_patch(p) for p in \
                           [dp, c, arr1, arr2]]
            l = patches[4]
            x, y = l.get_data()
            l.set_data((numpy.concatenate((x, [sigma])),
                        numpy.concatenate((y, [pre]))))
            text1, text2 = patches[5:7]
            text1.set_x(pr[0]); text1.set_y(pr[1]);
            text2.set_x(pt[0]); text2.set_y(pt[1]);
        else:
            # Update the elastic modulus
            nonlocal reg_xy     # declare reg_xy not only in this scope
            if reg_xy[0] is None:
                l = patches[4]
                x, y = l.get_data()
                slope, intercept, *_ = linregress(x[:5], y[:5])
                reg_xy = [slope, intercept]
                print(reg_xy)
            i_frame = i - (total_frames - final_frames) + 1
            xx = numpy.linspace(0, 0.25, final_frames)
            yy = reg_xy[0] * xx + reg_xy[1]
            l2 = patches[7]
            l2.set_data((xx[:i_frame], yy[:i_frame]))
            # Add the fitted value to last frame
            if i == total_frames - 1:
                text3 = patches[-1]
                text3.set_x(xx[1]); text3.set_y(yy[1])
                s = "{:.1e}".format(reg_xy[0]).split("e")
                base = float(s[0]); p = int(s[1])
                text3.set_text("Elastic Modulus: {0}$\\times$10$^{{{1}}}$ Pa".format(base, p))
                text3.set_verticalalignment("top")
                text3.set_horizontalalignment("left")
        return patches

    ani = FuncAnimation(fig, update, frames=total_frames, blit=True)
    plt.tight_layout()
    if show:
        plt.show()
    else:
        curr_dir = dirname(abspath(__file__))
        print(curr_dir)
        ani.save(join(curr_dir, "../results", "anim_pres.mp4"),
                writer=FFMpegWriter(fps=12,
                                    codec="libx264",
                                    extra_args=["-pix_fmt", "yuv420p",
                                                "-crf", "20"]),
                 dpi=600,
                 savefig_kwargs={'transparent': True})

if __name__ == "__main__":
    main()
