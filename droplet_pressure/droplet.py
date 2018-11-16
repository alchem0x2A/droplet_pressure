from __future__ import print_function
import numpy
from numpy import sin, cos, tan, pi
from numpy import radians
from scipy.optimize import fsolve
from scipy.constants import g

gamma_0 = 485e-3                # mercury surface tension
rho = 13.6e-3                   # mercury density


"""Class for droplet
The droplet is determined by 4 parameters:
h, volume, theta_t, theta_b
"""


class Droplet(object):
    """Parameters
    initial_volume: V_0
    theta_t, theta_b: contact angles in radians
    gamma: surface tension (SI unit)
    """

    def __init__(self,
                 initial_volume,
                 theta_t=pi,
                 theta_b=pi,
                 gamma=gamma_0):
        self.v0 = initial_volume
        self.theta_t = theta_t
        self.theta_b = theta_b
        self.gamma = gamma
        self.__init_params()

    def __init_params(self):
        self.h0 = solve_initial_height(self.v0,
                                       self.theta_t,
                                       self.theta_b)
        self.__h = self.h0
        self.__r1 = cal_r1(v=self.v0,
                           h=self.h0,
                           theta_t=self.theta_t,
                           theta_b=self.theta_b)
        self.__r2 = cal_r2(h=self.h0,
                           theta_t=self.theta_t,
                           theta_b=self.theta_b)

    @property
    def r1(self):
        return self.__r1

    @property
    def r2(self):
        return self.__r2

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, h):
        self.__h = h

def solve_initial_height(v0, theta_t, theta_b):
    """Solve the h0 value
    """
    def func_g(theta):
        A = ((1 + cos(theta)) / 2) ** 2
        B = 2 - cos(theta)
        return A * B
    h0 = (3 * v0 / 4 / pi) ** (1 / 3)
    h0 *= ((cos(theta_t) + cos(theta_b)) ** 3
           / (func_g(theta_t) + func_g(theta_b) - 1)) ** (1 / 3)
    return h0


def split_h(h, theta_t, theta_b):
    """Split the height into delta_t and delta_b
    """
    base = cos(theta_t) + cos(theta_b)
    delta_t = h * cos(theta_t) / base
    delta_b = h * cos(theta_b) / base
    return delta_t, delta_b


def f1(theta):
    res = theta - pi / 2 + sin(2 * theta - pi) / 2 + \
        2 * sin(theta) * cos(theta)
    return res


def f2(theta):
    # assert pi/2 < theta < pi
    res = tan(theta) * \
        (theta - pi / 2 + sin(2 * theta - pi) / 2 + 2 * cos(theta)) \
        - 1 / 3 * (cos(theta)) ** 2 + (1 - sin(theta)) ** 2 
    return res


def V_sym(R, delta, theta):
    """
    Symmetric case
    """
    # _, _, r = split_h(2 * delta, theta, theta)  # H = 2 * delta
    r = cal_r2(2 * delta, theta, theta)
    a = R + delta * (1 - sin(theta)) / cos(theta)
    a_ = R - r + r * sin(theta)
    V = 2 * pi * a ** 2 * delta \
        + 2 * pi * (delta / cos(theta)) ** 2 \
        * (a * f1(theta) + delta * f2(theta))
    return V


def cal_r1(v, h, theta_t, theta_b):
    """calculate r1 using fsolve
    """
    return None


def cal_r2(h, theta_t, theta_b):
    """calculate r2
    """
    return -h / (cos(theta_t) + cos(theta_b))


"""Dummy function only for test purpose
"""


def hello():
    print("Hello!")
    return 0
