import unittest
from MooToo.galaxy import Galaxy
from MooToo.empire import make_empire
from MooToo.system import System
from MooToo.planet import Planet
from MooToo.constants import Building, Technology
from MooToo.research import TechCategory


#####################################################################################################
class TestEmpire(unittest.TestCase):

    def setUp(self):
        self.galaxy = Galaxy()
        self.galaxy.populate("pre")
        self.system = System(1, (0, 0), self.galaxy)
        self.empire = self.galaxy.empires[1]

    #################################################################################################
    def test_next_research(self):
        avail = self.galaxy.empires[1].next_research(TechCategory.SOCIOLOGY)
        self.assertEqual(avail, [Technology.MILITARY_TACTICS])
        self.empire.learnt(Technology.MILITARY_TACTICS)
        avail = self.empire.next_research(TechCategory.SOCIOLOGY)
        self.assertEqual(avail, [Technology.SPACE_ACADEMY])

    #################################################################################################
    def test_learn_tech(self):
        """Learn a new technology"""
        self.assertFalse(Technology.FREIGHTERS in self.empire.known_techs)
        self.empire.learnt(Technology.FREIGHTERS)
        self.assertTrue(Technology.FREIGHTERS in self.empire.known_techs)
        self.assertTrue(Technology.NUCLEAR_DRIVE in self.empire.known_techs)

    #################################################################################################
    def test_set_home_planet(self):
        """Set the home planet of the empire"""
        planet = Planet(self.system, self.galaxy)
        self.galaxy.empires[1].set_home_planet(planet)
        self.assertIn(Building.MARINE_BARRACKS, planet.buildings)
        self.assertIn(planet.system.id, self.empire.known_systems)

    #################################################################################################
    def test_make_empire(self):
        system = System(0, (0, 0), self.galaxy)
        empire = make_empire("fred", "red", system, self.galaxy)
        self.assertEqual(empire.name, "fred")

    #################################################################################################
    def test_migration(self):
        pass


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
