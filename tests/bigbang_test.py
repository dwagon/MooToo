import unittest

from MooToo.bigbang import get_system_positions, find_home_systems, create_galaxy
from MooToo.constants import Technology


#####################################################################################################
class TestBigBang(unittest.TestCase):
    def test_get_system_positions(self):
        positions = get_system_positions(5)
        self.assertEqual(len(positions), 5)

    #################################################################################################
    def test_find_home_systems(self):
        galaxy = create_galaxy()
        systems = find_home_systems(galaxy, 3)
        self.assertEqual(len(systems), 3)

    #################################################################################################
    def test_default_start(self):
        galaxy = create_galaxy("avg")
        self.assertIn(Technology.COLONY_SHIP, galaxy.empires[1].known_techs)

    #################################################################################################
    def test_pre_start(self):
        galaxy = create_galaxy("pre")
        self.assertNotIn(Technology.COLONY_SHIP, galaxy.empires[1].known_techs)

    #################################################################################################
    def test_advanced_start(self):
        galaxy = create_galaxy("adv")
        self.assertIn(Technology.COLONY_SHIP, galaxy.empires[1].known_techs)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
