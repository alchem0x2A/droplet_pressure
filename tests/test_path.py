import droplet_pressure
from droplet_pressure.droplet import hello
import unittest

class TestPath(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), 0)

if __name__ == "__main__":
    unittest.main()
