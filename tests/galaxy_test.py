import unittest
from MooToo.galaxy import make_empire, EMPIRES, get_system_positions, find_home_systems
from MooToo.system import System


#####################################################################################################
class TestGalaxy(unittest.TestCase):
    def setUp(self):
        pass

    def test_make_empire(self):
        system = System(0, (0, 0))
        make_empire("fred", system)
        self.assertIn(0, EMPIRES["fred"].known_systems)

    def test_get_system_positions(self):
        positions = get_system_positions(5)
        self.assertEqual(len(positions), 5)

    def test_find_home_systems(self):
        systems = find_home_systems(3)
        self.assertEqual(len(systems), 3)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
