import unittest
from MooToo.empire import Empire
from MooToo.galaxy import Galaxy
from MooToo.system import System
from MooToo.planet import Planet
from MooToo.ship import select_ship_type_by_name
from MooToo.utils import get_distance_tuple


#####################################################################################################
class TestShip(unittest.TestCase):
    def setUp(self):
        self.galaxy = Galaxy()
        self.system = System(1, (0, 0), self.galaxy)
        self.planet = Planet(self.system)
        self.empire = Empire("PlayerOne")
        self.galaxy.empires["PlayerOne"] = self.empire
        self.planet.owner = "PlayerOne"

    def test_select_ship(self):
        ship = select_ship_type_by_name("Frigate")
        self.empire.add_ship(ship, self.system)
        self.assertEqual(ship.orbit, self.system)
        self.assertIn("Frigate", ship.name)

    def test_move_ship(self):
        destination = System(2, (20, 0), self.galaxy)
        ship = select_ship_type_by_name("Cruiser")
        self.empire.add_ship(ship, self.system)
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
        system2 = System(2, (4, 0), self.galaxy)

        ship = select_ship_type_by_name("DoomStar")
        ship.orbit = self.system

        ship.set_destination(self.system)
        self.assertIsNone(ship.destination)

        ship.set_destination(system2)
        self.assertEqual(ship.destination, system2)


if __name__ == "__main__":
    unittest.main()
