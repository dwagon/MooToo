import unittest

from MooToo.planet import Planet
from MooToo.system import System
from MooToo.galaxy import Galaxy
from MooToo.constants import PlanetSize, PlanetClimate, PlanetGravity, PopulationJobs, Building
from MooToo.planet_food import food_cost, food_production, food_surplus, food_per


#####################################################################################################
class TestPlanetFood(unittest.TestCase):
    #################################################################################################
    def setUp(self):
        self.galaxy = Galaxy()
        self.system = System(99, "Test", "white", (0, 0), self.galaxy)

    #################################################################################################
    def test_consumption(self):
        """Test Consumption"""
        planet = Planet(
            99,
            self.system,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            gravity=PlanetGravity.NORMAL,
            climate=PlanetClimate.TERRAN,
        )
        planet.jobs[PopulationJobs.FARMERS] = 4
        planet.jobs[PopulationJobs.WORKERS] = 1
        planet._population = 5.2e6

        self.assertEqual(food_cost(planet), 5)

    def test_production(self):
        planet = Planet(
            99,
            self.system,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            gravity=PlanetGravity.NORMAL,
            climate=PlanetClimate.TERRAN,
        )
        planet.jobs[PopulationJobs.FARMERS] = 5
        planet.jobs[PopulationJobs.WORKERS] = 2
        planet._population = 7.5e6

        planet.buildings.add(Building.HYDROPONIC_FARM)

        self.assertEqual(food_production(planet), 5 * 2 + 2)
        self.assertEqual(food_cost(planet), 7)
        self.assertEqual(food_surplus(planet), 5 * 2 + 2 - 7)

    def test_per(self):
        planet = Planet(
            99,
            self.system,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            gravity=PlanetGravity.NORMAL,
            climate=PlanetClimate.TERRAN,
        )
        self.assertEqual(food_per(planet), 2)


if __name__ == "__main__":
    unittest.main()
