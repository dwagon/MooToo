import unittest
from MooToo.constants import Building, PopulationJobs, Technology
from MooToo.galaxy import Galaxy, NUM_SYSTEMS, NUM_EMPIRES, load_researches
from MooToo.system import System
from MooToo.planet import Planet, PlanetSize, PlanetClimate


#####################################################################################################
class TestGalaxy(unittest.TestCase):
    def setUp(self):
        self.galaxy = Galaxy()

    def test_make_home_planet(self):
        system = System(0, (0, 0))
        pl = self.galaxy.make_home_planet(system)
        self.assertEqual(pl.climate, PlanetClimate.TERRAN)

    def test_make_empire(self):
        system = System(0, (0, 0))
        self.galaxy.make_empire("fred", system)
        self.assertIn(0, self.galaxy.empires["fred"].known_systems)

    def test_get_system_positions(self):
        positions = self.galaxy.get_system_positions()
        self.assertEqual(len(positions), NUM_SYSTEMS)

    def test_find_home_systems(self):
        systems = self.galaxy.find_home_systems()
        self.assertEqual(len(systems), NUM_EMPIRES)

    def test_load_researches(self):
        mapping = load_researches()
        self.assertIn(Technology.FREIGHTERS, mapping)
        self.assertIn(Technology.STANDARD_FUEL_CELLS, mapping)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
