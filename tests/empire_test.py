import unittest
from MooToo.bigbang import create_galaxy
from MooToo.constants import Technology, StarColour, GalaxySize, GALAXY_SIZE_DATA, GalaxySizeKeys
from MooToo.planet import Planet
from MooToo.research import TechCategory
from MooToo.ship_design import ShipDesign, HullType
from MooToo.system import System
from MooToo.utils import ShipId


#####################################################################################################
class TestEmpire(unittest.TestCase):

    def setUp(self):
        """Create simple galaxy"""
        self.galaxy = create_galaxy("pre", size=GalaxySize.TEST)
        self.empire_id = 1
        self.empire = self.galaxy.empires[self.empire_id]
        self.home_system = 1
        self.galaxy.systems = {}
        self.galaxy.planets = {}
        self.galaxy.systems[self.home_system] = System(self.home_system, "Home", StarColour.WHITE, (0, 0), self.galaxy)
        self.galaxy.systems[2] = System(2, "Two", StarColour.WHITE, (4, 0), self.galaxy)
        self.galaxy.planets[1] = Planet(1, 1, self.galaxy)
        self.galaxy.planets[2] = Planet(2, 2, self.galaxy)
        self.empire.owned_planets = {1}

    #################################################################################################
    def build_frigate(self, name: str) -> ShipId:
        frigate_design = ShipDesign(HullType.Frigate)
        frigate_design_id = self.galaxy.add_design(frigate_design, self.empire_id)
        return self.empire.build_ship_design(frigate_design_id, self.home_system, name)

    #################################################################################################
    def test_build_ship_design(self):
        ship_name = "Nostromo"
        ship_id = self.build_frigate(ship_name)
        self.assertEqual(self.galaxy.ships[ship_id].name, ship_name)
        self.assertEqual(self.galaxy.ships[ship_id].orbit, self.home_system)

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
    def test_ship_speed(self):
        destroyer_design = ShipDesign(HullType.Destroyer)
        destroyer_design_id = self.galaxy.add_design(destroyer_design, self.empire_id)
        ship_id = self.empire.build_ship_design(destroyer_design_id, 1, "Fireball")
        empire = self.galaxy.empires[self.empire_id]
        empire.learnt(Technology.NUCLEAR_DRIVE)
        self.assertEqual(empire.ship_speed, 2)
        self.assertEqual(
            self.galaxy.ships[ship_id].speed(), 2 * GALAXY_SIZE_DATA[self.galaxy.size][GalaxySizeKeys.SCALE]
        )

    #################################################################################################
    def test_ship_range(self):
        empire = self.galaxy.empires[self.empire_id]
        self.assertEqual(empire.ship_range, 4)
        empire.learnt(Technology.DEUTERIUM_FUEL_CELLS)
        self.assertEqual(empire.ship_range, 6)

    #################################################################################################
    def test_eta(self):
        ship_id = self.build_frigate("Dog Star")
        self.empire.learnt(Technology.NUCLEAR_DRIVE)
        eta = self.empire.eta(1, 2)
        self.assertEqual(eta, 2)
        ship = self.galaxy.ships[ship_id]
        ship.set_destination(2)
        ship.move_towards_destination()
        self.assertIsNone(ship.orbit)
        ship.move_towards_destination()
        self.assertEqual(ship.orbit, 2)

    #################################################################################################
    def test_in_range(self):
        self.galaxy.systems[3] = System(3, "Three", StarColour.WHITE, (8, 0), self.galaxy)
        ship_id = self.build_frigate("Dog Star")

        self.assertTrue(self.empire.in_range(2, ship_id))
        self.assertFalse(self.empire.in_range(3, ship_id))

        # System 3 should be in range now that we own system 2
        self.empire.owned_planets.add(2)
        self.assertTrue(self.empire.in_range(2, ship_id))
        self.assertTrue(self.empire.in_range(3, ship_id))

    #################################################################################################
    def test_colonize(self):
        target_planet = self.galaxy.planets[2].id
        colony_design = ShipDesign(HullType.ColonyShip)
        colony_design_id = self.galaxy.add_design(colony_design, self.empire_id)
        ship_id = self.empire.build_ship_design(colony_design_id, self.home_system, "Nemo")
        self.empire.colonize(target_planet, ship_id)
        self.assertIn(target_planet, self.empire.owned_planets)
        self.assertEqual(self.galaxy.planets[target_planet].owner, self.empire_id)
        self.assertNotIn(ship_id, self.empire.ships)
        self.assertNotIn(ship_id, self.galaxy.ships)
        self.assertGreater(self.galaxy.planets[target_planet].current_population(), 0)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
