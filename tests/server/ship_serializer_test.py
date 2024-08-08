import unittest

from MooToo.server.serializers import ship_reference_serializer
from MooToo.server.serializers.ship import ship_serializer
from MooToo.ship import select_ship_type_by_name
from MooToo.bigbang import create_galaxy


#####################################################################################################
class ShipSerializerTest(unittest.TestCase):
    def setUp(self):
        self.galaxy = create_galaxy()
        ship_id = select_ship_type_by_name("Frigate", self.galaxy)

        self.ship = self.galaxy.ships[ship_id]
        self.ship.name = "Nautilus"

    #################################################################################################
    def test_reference(self):
        reference = ship_reference_serializer(self.ship.id)
        self.assertEqual(reference["id"], self.ship.id)
        self.assertEqual(reference["url"], f"/ships/{self.ship.id}")

    #################################################################################################
    def test_serialize(self):
        output = ship_serializer(self.ship)
        print(f"DBG {output}")
        self.assertEqual(output["name"], "Nautilus")
        self.assertEqual(output["owner"], {"id": 0, "url": "/empires/0"})
        self.assertEqual(output["type"], "Frigate")


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
