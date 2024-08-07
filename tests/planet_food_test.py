import unittest

from MooToo.planet import Planet
from MooToo.system import System
from MooToo.galaxy import Galaxy
from MooToo.constants import PlanetSize, PlanetClimate, PlanetGravity, PopulationJobs, Building, StarColour
from MooToo.planet_food import food_cost, food_production, food_surplus, food_per


#####################################################################################################
class TestPlanetFood(unittest.TestCase):
    #################################################################################################
    def setUp(self):
        self.galaxy = Galaxy()
        self.system = System(99, "Test", StarColour.WHITE, (0, 0), self.galaxy)
        self.galaxy.systems[self.system.id] = self.system
        self.planet = Planet(
            99,
            self.system.id,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            gravity=PlanetGravity.NORMAL,
            climate=PlanetClimate.TERRAN,
        )

    #################################################################################################
    def test_consumption(self):
        """Test Consumption"""
        self.planet.jobs[PopulationJobs.FARMERS] = 4
        self.planet.jobs[PopulationJobs.WORKERS] = 1
        self.planet._population = 5.2e6

        self.assertEqual(food_cost(self.planet), 5)

    def test_production(self):
        self.planet.jobs[PopulationJobs.FARMERS] = 5
        self.planet.jobs[PopulationJobs.WORKERS] = 2
        self.planet._population = 7.5e6

        self.planet.buildings.add(Building.HYDROPONIC_FARM)

        self.assertEqual(food_production(self.planet), 5 * 2 + 2)
        self.assertEqual(food_cost(self.planet), 7)
        self.assertEqual(food_surplus(self.planet), 5 * 2 + 2 - 7)

    def test_per(self):
        planet = Planet(
            99,
            self.system.id,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            gravity=PlanetGravity.NORMAL,
            climate=PlanetClimate.TERRAN,
        )
        self.assertEqual(food_per(planet), 2)


if __name__ == "__main__":
    unittest.main()
