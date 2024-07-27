import unittest
from MooToo.constants import PopulationJobs, PlanetSize, PlanetRichness, PlanetGravity
from MooToo.planet import Planet
from MooToo.system import System
from MooToo.galaxy import Galaxy
from MooToo.planet_science import science_surplus


#####################################################################################################
class TestPlanetScience(unittest.TestCase):
    #################################################################################################
    def setUp(self):
        self.galaxy = Galaxy()
        self.system = System((0, 0), self.galaxy)
        self.planet = Planet(
            self.system,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            richness=PlanetRichness.ABUNDANT,
            gravity=PlanetGravity.NORMAL,
        )

    #################################################################################################
    def test_get_research_points(self):
        self.planet.jobs[PopulationJobs.SCIENTISTS] = 1
        self.assertEqual(science_surplus(self.planet), 1)


if __name__ == "__main__":
    unittest.main()
