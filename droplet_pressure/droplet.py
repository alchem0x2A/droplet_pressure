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
        self.h0 = self.__solve_initial_height()
        self.h = self.h0
        self.p0 = self.get_curve_pressure(gravity=False)
        self.p0_gravity = self.get_curve_pressure(gravity=True)

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
        # Update the calculated values of r1, r2 upon assign to h
        self.__cal_r1()
        self.__cal_r2()

    def get_curve_pressure(self, gravity=False):
        p = self.gamma * (1 / self.r1 + 1 / self.r2)
        if gravity:
            p += rho * self.h * g
        return p

    def get_delta_stress(self, gravity=False):
        p = self.get_curve_pressure(gravity=gravity)
        # delta to initial state
        if gravity is True:
            return p - self.p0_gravity
        else:
            return p - self.p0

    def __cal_r1(self):
        """calculate r1 using fsolve
        Required ingredients:
        v, h, theta_t, theta_b
        """
        delta_t, delta_b = self.__split_h()
        def _target(R):
            V1 = V_sym(R, delta_t, self.theta_t)
            V2 = V_sym(R, delta_b, self.theta_b)
            return (V1 + V2) / 2 - self.v0
        R_solution,  = fsolve(_target, x0=self.h)
        # a1 = R_solution + delta * (1 - sin(theta1)) / (cos(theta1) + cos(theta2))
        # a2 = R_solution + delta * (1 - sin(theta2)) / (cos(theta1) + cos(theta2))
        # r = -delta / (cos(theta1) + cos(theta2))
        self.__r1 = R_solution

    def __cal_r2(self):
        """calculate r2
        Required ingredients:
        h, theta_t, theta_b
        """
        self.__r2 = -self.h / (cos(self.theta_t) + cos(self.theta_b))

    def __solve_initial_height(self):
        """Solve the h0 value
        """
        def func_g(theta):
            A = ((1 + cos(theta)) / 2) ** 2
            B = 2 - cos(theta)
            return A * B
        h0 = (3 * self.v0 / 4 / pi) ** (1 / 3)
        # Only the purely real values
        h0 *= ((cos(self.theta_t) + cos(self.theta_b)) ** 3
               / (func_g(self.theta_t) + func_g(self.theta_b) - 1)) ** (1 / 3)
        return h0
    
    def __split_h(self):
        """Split the height into delta_t and delta_b
        """
        base = cos(self.theta_t) + cos(self.theta_b)
        delta_t = self.h * cos(self.theta_t) / base
        delta_b = self.h * cos(self.theta_b) / base
        return delta_t, delta_b


##########################
# Useful functions below #
##########################

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
    r = -delta / cos(theta)
    a = R + delta * (1 - sin(theta)) / cos(theta)
    a_ = R - r + r * sin(theta)
    V = 2 * pi * a ** 2 * delta \
        + 2 * pi * (delta / cos(theta)) ** 2 \
        * (a * f1(theta) + delta * f2(theta))
    return V



####################################
# Dummy function only for test use #
####################################

def hello():
    print("Hello!")
    return 0
