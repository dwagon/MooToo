import unittest

from MooToo.bigbang import get_system_positions, find_home_systems, create_galaxy
from MooToo.constants import Technology, NUM_SYSTEMS, NUM_EMPIRES
from MooToo.empire import Empire
from MooToo.planet import Planet
from MooToo.ship import Ship
from MooToo.system import System


#####################################################################################################
class TestBigBang(unittest.TestCase):
    def test_get_system_positions(self):
        positions = get_system_positions(5)
        self.assertEqual(len(positions), 5)

    #################################################################################################
    def test_galaxy_creation(self):
        galaxy = create_galaxy()
        self.assertEqual(len(galaxy.systems), NUM_SYSTEMS)
        self.assertEqual(len(galaxy.empires), NUM_EMPIRES)
        self.assertEqual(len(galaxy.ships), NUM_EMPIRES * 3)
        self.assertTrue(all(isinstance(_, System) for _ in galaxy.systems.values()))
        self.assertTrue(all(isinstance(_, Empire) for _ in galaxy.empires.values()))
        self.assertTrue(all(isinstance(_, Planet) for _ in galaxy.planets.values()))
        self.assertTrue(all(isinstance(_, Ship) for _ in galaxy.ships.values()))
        self.assertEqual(galaxy.turn_number, 0)

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
