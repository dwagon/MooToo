import unittest
from MooToo.bigbang import create_galaxy
from MooToo.constants import StarColour
from MooToo.system import System
from MooToo.ship import select_ship_type_by_name
from MooToo.utils import get_distance_tuple


#####################################################################################################
class TestShip(unittest.TestCase):
    def setUp(self):
        self.galaxy = create_galaxy()
        self.empire = self.galaxy.empires[1]
        self.system = self.galaxy.systems[1]

    #################################################################################################
    def test_select_ship(self):
        ship_id = select_ship_type_by_name("Frigate", self.galaxy)
        self.empire.add_ship(ship_id, self.system.id)
        ship = self.galaxy.ships[ship_id]
        self.assertEqual(ship.orbit, self.system.id)
        self.assertIn("Frigate", ship.name)

    #####################################################################################################
    def test_move_ship(self):
        source = System(98, "Source", StarColour.WHITE, (0, 0), self.galaxy)
        destination = System(99, "Target", StarColour.WHITE, (20, 0), self.galaxy)
        self.galaxy.systems[98] = source
        self.galaxy.systems[99] = destination
        ship_id = select_ship_type_by_name("Cruiser", self.galaxy)
        ship = self.galaxy.ships[ship_id]
        self.empire.add_ship(ship_id, source.id)
        ship.set_destination(destination.id)
        self.assertEqual(ship.destination, destination.id)
        distance = get_distance_tuple(ship.location, destination.position)
        self.assertEqual(distance, 20)

        # In deep space
        ship.move_towards_destination()
        distance = get_distance_tuple(ship.location, destination.position)
        self.assertIsNone(ship.orbit)
        self.assertEqual(ship.location, (10, 0))
        self.assertEqual(distance, 10)

        # Arrived
        ship.move_towards_destination()
        self.assertEqual(ship.orbit, destination)
        self.assertEqual(ship.location, destination.position)
        self.assertIsNone(ship.destination)

    #####################################################################################################
    def test_set_destination(self):
        system2 = System(99, "test", StarColour.WHITE, (4, 0), self.galaxy)

        ship_id = select_ship_type_by_name("DoomStar", self.galaxy)
        ship = self.galaxy.ships[ship_id]
        ship.orbit = self.system.id

        ship.set_destination(self.system.id)
        self.assertIsNone(ship.destination)

        ship.set_destination(system2.id)
        self.assertEqual(ship.destination, system2.id)


#########################################################################################################
if __name__ == "__main__":
    unittest.main()
