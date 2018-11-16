import droplet_pressure
from droplet_pressure.droplet import Droplet, pi, V_sym
import unittest

class TestClass(unittest.TestCase):
    def test_h0(self):
        v0 = 1.0e-10
        d = Droplet(initial_volume=v0)
        h0 = d.h0
        r0 = h0 / 2
        v_sol = (4 * pi / 3) * r0 ** 3
        self.assertAlmostEqual(v_sol, v0,
                               places=5,
                               msg="initial height is wrong!")
        self.assertAlmostEqual(d.r1, d.r2,
                               places=5,
                               msg="solution to r1 and r2 wrong!")
        
    def test_sym(self):
        r = 1.0
        v_0 = (4 * pi / 3) * r ** 3
        v_cal = V_sym(r, r, pi)
        self.assertAlmostEqual(v_cal, v_0,
                               places=5,
                               msg="Symmetric solution is wrong!")

    def test_pressure(self):
        v0 = 1.0e-10
        d = Droplet(initial_volume=v0)
        d.h = d.h0 / 2
        p1 = d.get_delta_stress()
        p2 = d.get_delta_stress(gravity=True)
        print(d.p0, p1, p2)

if __name__ == "__main__":
    unittest.main()
