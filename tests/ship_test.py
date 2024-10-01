import unittest
from MooToo.bigbang import create_galaxy
from MooToo.constants import StarColour, Technology, GalaxySize
from MooToo.ship_design import ShipDesign, HullType
from MooToo.system import System
from MooToo.utils import get_distance_tuple


#####################################################################################################
class TestShip(unittest.TestCase):
    def setUp(self):
        self.empire_id = 1
        self.galaxy = create_galaxy(size=GalaxySize.TEST)
        self.empire = self.galaxy.empires[self.empire_id]
        self.system = self.galaxy.systems[1]
        frigate_design = ShipDesign(HullType.Frigate)
        self.frigate_design_id = self.galaxy.add_design(frigate_design, self.empire_id)
        colony_design = ShipDesign(HullType.ColonyShip)
        self.colony_design_id = self.galaxy.add_design(colony_design, self.empire_id)

    #####################################################################################################
    def test_coloniser(self):
        frigate_id = self.empire.build_ship_design(self.frigate_design_id, self.system.id)
        frigate = self.galaxy.ships[frigate_id]
        self.assertFalse(frigate.coloniser)

    #####################################################################################################
    def test_move_ship(self):
        source = System(98, "Source", StarColour.WHITE, (0, 0), self.galaxy)
        destination = System(99, "Target", StarColour.WHITE, (4, 0), self.galaxy)
        self.galaxy.systems[98] = source
        self.galaxy.systems[99] = destination
        ship_id = self.empire.build_ship_design(self.frigate_design_id, source.id)
        ship = self.galaxy.ships[ship_id]

        ship.set_destination(destination.id)
        self.assertIsNone(ship.destination)  # Not in range

        self.empire.learnt(Technology.THORIUM_FUEL_CELLS)  # Make lots of range
        ship.set_destination(destination.id)
        self.assertEqual(ship.destination, destination.id)
        distance = int(get_distance_tuple(ship.location, destination.position))
        self.assertEqual(distance, 4)

        self.assertEqual(self.empire.ship_speed, 2)

        # In deep space
        ship.move_towards_destination()
        distance = get_distance_tuple(ship.location, destination.position)
        self.assertIsNone(ship.orbit)
        self.assertEqual(ship.location, (2, 0))
        self.assertEqual(distance, 2)

        # Arrived
        ship.move_towards_destination()
        self.assertEqual(ship.orbit, destination.id)
        self.assertEqual(ship.location, destination.position)
        self.assertIsNone(ship.destination)

    #####################################################################################################
    def test_range(self):
        system = System(98, "Source", StarColour.WHITE, (0, 0), self.galaxy)
        self.galaxy.systems[98] = system
        frigate_id = self.empire.build_ship_design(self.frigate_design_id, system.id)
        colony_id = self.empire.build_ship_design(self.colony_design_id, system.id)
        self.assertEqual(self.galaxy.ships[frigate_id].range, 4)
        self.assertEqual(self.galaxy.ships[colony_id].range, 8)

        self.empire.learnt(Technology.URIDIUM_FUEL_CELLS)
        self.assertEqual(self.galaxy.ships[frigate_id].range, 12)

    #####################################################################################################
    def test_set_destination(self):
        source = System(98, "Source", StarColour.WHITE, (0, 0), self.galaxy)
        self.galaxy.systems[98] = source
        dest = System(99, "test", StarColour.WHITE, (8, 0), self.galaxy)
        self.galaxy.systems[99] = dest

        ship_id = 1
        ship = self.galaxy.ships[ship_id]
        ship.orbit = source.id

        ship.set_destination(dest.id)
        self.assertIsNone(ship.destination)

        ship.set_destination(dest.id)
        self.assertIsNone(ship.destination)

        self.empire.learnt(Technology.THORIUM_FUEL_CELLS)
        ship.set_destination(dest.id)
        self.assertEqual(ship.destination, dest.id)


#########################################################################################################
if __name__ == "__main__":
    unittest.main()
