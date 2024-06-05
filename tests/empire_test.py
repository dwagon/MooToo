import unittest
from MooToo.galaxy import Galaxy
from MooToo.empire import Empire
from MooToo.system import System
from MooToo.planet import Planet
from MooToo.constants import Building, Technology
from MooToo.research import ResearchCategory


#####################################################################################################
class TestEmpire(unittest.TestCase):

    def setUp(self):
        self.galaxy = Galaxy()
        self.system = System(1, (0, 0), self.galaxy)
        self.planet = Planet("test", self.system, self.galaxy)
        self.empire = Empire("PlayerOne", self.galaxy)
        self.galaxy.empires["PlayerOne"] = self.empire
        self.planet.owner = "PlayerOne"

    def test_make_home_planet(self):
        pl = self.empire.make_home_planet(self.system)
        self.assertIn(Building.MARINE_BARRACKS, pl.buildings)
        self.assertTrue(self.empire.is_known_system(self.system))

    def test_next_research(self):
        avail = self.empire.next_research(ResearchCategory.SOCIOLOGY)
        self.assertEqual(avail, [Technology.MILITARY_TACTICS])
        self.empire.learnt(Technology.MILITARY_TACTICS)
        avail = self.empire.next_research(ResearchCategory.SOCIOLOGY)
        self.assertEqual(avail, [Technology.SPACE_ACADEMY])


if __name__ == "__main__":
    unittest.main()
