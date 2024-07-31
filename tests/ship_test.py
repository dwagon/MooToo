import unittest
from MooToo.bigbang import create_galaxy
from MooToo.system import System
from MooToo.ship import select_ship_type_by_name
from MooToo.utils import get_distance_tuple


#####################################################################################################
class TestShip(unittest.TestCase):
    def setUp(self):
        self.galaxy = create_galaxy()
        self.empire = self.galaxy.empires[1]
        self.system = self.galaxy.systems[1]

    def test_select_ship(self):
        ship = select_ship_type_by_name("Frigate", self.galaxy)
        self.empire.add_ship(ship, self.system)
        self.assertEqual(ship.orbit, self.system)
        self.assertIn("Frigate", ship.name)

    def test_move_ship(self):
        source = System(98, "Source", "Purple", (0, 0), self.galaxy)
        destination = System(99, "Target", "Purple", (20, 0), self.galaxy)
        ship = select_ship_type_by_name("Cruiser", self.galaxy)
        self.empire.add_ship(ship, source)
        ship.set_destination(destination)
        self.assertEqual(ship.destination, destination)
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

    def test_set_destination(self):
        system2 = System(99, "test", "white", (4, 0), self.galaxy)

        ship = select_ship_type_by_name("DoomStar", self.galaxy)
        ship.orbit = self.system

        ship.set_destination(self.system)
        self.assertIsNone(ship.destination)

        ship.set_destination(system2)
        self.assertEqual(ship.destination, system2)


if __name__ == "__main__":
    unittest.main()
