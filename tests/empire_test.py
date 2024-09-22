import unittest
from MooToo.bigbang import create_galaxy
from MooToo.constants import Technology
from MooToo.research import TechCategory
from MooToo.ship_design import ShipDesign, HullType


#####################################################################################################
class TestEmpire(unittest.TestCase):

    def setUp(self):
        self.galaxy = create_galaxy("pre")
        self.empire_id = 1
        self.empire = self.galaxy.empires[self.empire_id]

    #################################################################################################
    def test_build_ship_design(self):
        home_system = list(self.empire.known_systems)[0]
        frigate_design = ShipDesign(HullType.Frigate)
        frigate_design_id = self.galaxy.add_design(frigate_design, self.empire_id)
        ship_id = self.empire.build_ship_design(frigate_design_id, home_system, "Nostromo")
        self.assertEqual(self.galaxy.ships[ship_id].name, "Nostromo")
        self.assertEqual(self.galaxy.ships[ship_id].orbit, home_system)

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
    def test_migration(self):
        pass

    #################################################################################################
    def test_colonize(self):
        target_planet = self.galaxy.planets[10].id
        home_system = list(self.empire.known_systems)[0]
        colony_design = ShipDesign(HullType.ColonyShip)
        colony_design_id = self.galaxy.add_design(colony_design, self.empire_id)
        ship_id = self.empire.build_ship_design(colony_design_id, home_system, "Nemo")
        self.empire.colonize(target_planet, ship_id)
        self.assertIn(target_planet, self.empire.owned_planets)
        self.assertEqual(self.galaxy.planets[target_planet].owner, self.empire_id)
        self.assertNotIn(ship_id, self.empire.ships)
        self.assertNotIn(ship_id, self.galaxy.ships)
        self.assertGreater(self.galaxy.planets[target_planet].current_population(), 0)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
