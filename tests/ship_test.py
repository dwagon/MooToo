import unittest
from MooToo.galaxy import Galaxy
from MooToo.empire import Empire
from MooToo.system import System
from MooToo.planet import Planet
from MooToo.ship import select_ship_type_by_name
from MooToo.utils import get_distance_tuple


#####################################################################################################
class TestShip(unittest.TestCase):
    def setUp(self):
        self.galaxy = Galaxy()
        self.system = System(1, (0, 0))
        self.planet = Planet(self.system)
        self.empire = Empire("PlayerOne", self.galaxy)
        self.galaxy.empires["PlayerOne"] = self.empire
        self.planet.owner = "PlayerOne"

    def test_select_ship(self):
        ship = select_ship_type_by_name("Frigate")
        self.empire.add_ship(ship, self.system)
        self.assertEqual(ship.orbit, self.system)
        self.assertIn("Frigate", ship.name)

    def test_move_ship(self):
        destination = System(2, (4, 0))
        ship = select_ship_type_by_name("Cruiser")
        self.empire.add_ship(ship, self.system)
        ship.set_destination(destination)
        self.assertEqual(ship.destination, destination)
        distance = get_distance_tuple(ship.location, destination.position)
        self.assertEqual(distance, 4)

        # In deep space
        ship.move_towards_destination()
        distance = get_distance_tuple(ship.location, destination.position)
        self.assertIsNone(ship.orbit)
        self.assertEqual(ship.location, (2, 0))
        self.assertEqual(distance, 2)

        # Arrived
        ship.move_towards_destination()
        self.assertEqual(ship.orbit, destination)
        self.assertEqual(ship.location, destination.position)
        self.assertIsNone(ship.destination)


if __name__ == "__main__":
    unittest.main()
