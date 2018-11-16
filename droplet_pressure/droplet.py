from __future__ import print_function
import numpy
from numpy import sin, cos, tan, pi
from numpy import radians
from scipy.optimize import fsolve
from scipy.constants import g

gamma_0 = 485e-3                # mercury



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
        self.volume = initial_volume
        self.theta_t = theta_t
        self.theta_b = theta_b
        self.gamma = gamma
        self._init_params()
    
    def _init_params(self):
        self.h0 = solve_initial_height(self.v0,
                                       self.theta_t,
                                       self.theta_b)
        
        
    
"""Solve the h0 value
"""
def solve_initial_height(v0, theta_t, theta_b):
    def func_g(theta):
        A = ((1 + cos(theta)) / 2) ** 2
        B = 2 - cos(theta)
        return A * B
    h0 = (3 * v0 / 4 / pi) ** (1 / 3)
    h0 *= ((cos(theta_t) + cos(theta_b)) ** 3 \
          / (func_g(theta_t) + func_g(theta_b) -1)) ** (1 / 3)
    return h0
    

"""Dummy function only for test purpose
"""
def hello():
    print("Hello!")
    return 0
