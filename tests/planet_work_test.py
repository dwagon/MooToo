import unittest
from MooToo.planet import Planet
from MooToo.system import System
from MooToo.galaxy import Galaxy
from MooToo.constants import PlanetSize, PlanetRichness, PlanetGravity, PopulationJobs, Building
from MooToo.planet_work import work_cost, work_production, work_surplus


#####################################################################################################
class TestPlanetWork(unittest.TestCase):
    #################################################################################################
    def setUp(self):
        self.galaxy = Galaxy()
        self.system = System(99, "test", "white", (0, 0), self.galaxy)

    #################################################################################################
    def test_pollution(self):
        """Test Pollution"""
        planet = Planet(
            99,
            self.system,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            richness=PlanetRichness.ABUNDANT,
            gravity=PlanetGravity.NORMAL,
        )
        planet.jobs[PopulationJobs.WORKERS] = 4
        planet.buildings.add(Building.AUTOMATED_FACTORY)
        self.assertEqual(work_cost(planet), 5)

    #################################################################################################
    def test_work(self):
        planet = Planet(
            99,
            self.system,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            gravity=PlanetGravity.NORMAL,
            richness=PlanetRichness.ABUNDANT,
        )
        planet.jobs[PopulationJobs.WORKERS] = 5

        self.assertEqual(work_production(planet), 15)
        self.assertEqual(work_cost(planet), 4)
        self.assertEqual(work_surplus(planet), 11)


#################################################################################################
if __name__ == "__main__":
    unittest.main()
