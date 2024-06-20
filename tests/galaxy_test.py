import unittest
from MooToo.galaxy import make_empire, Galaxy, get_system_positions
from MooToo.system import System


#####################################################################################################
class TestGalaxy(unittest.TestCase):
    def setUp(self):
        self.galaxy = Galaxy()

    def test_get_system_positions(self):
        positions = get_system_positions(5)
        self.assertEqual(len(positions), 5)

    def test_find_home_systems(self):
        systems = self.galaxy.find_home_systems(3)
        self.assertEqual(len(systems), 3)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
