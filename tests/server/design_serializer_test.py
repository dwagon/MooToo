import unittest

from MooToo.bigbang import create_galaxy
from MooToo.server.serializers import design_reference_serializer
from MooToo.server.serializers.ship_design import ship_design_serializer
from MooToo.ship_design import ShipDesign, HullType


#####################################################################################################
class DesignSerializerTest(unittest.TestCase):
    def setUp(self):
        self.galaxy = create_galaxy()
        self.design = ShipDesign(HullType.ColonyShip, "Colony")
        self.galaxy.add_design(self.design, 1)

    #################################################################################################
    def test_reference(self):
        reference = design_reference_serializer(self.design.id)
        self.assertEqual(reference["id"], self.design.id)
        self.assertEqual(reference["url"], f"/design/{self.design.id}")

    #################################################################################################
    def test_serialize(self):
        output = ship_design_serializer(self.design)
        print(f"DBG {output}")
        self.assertEqual(output["name"], "Colony")
        self.assertEqual(output["hull"], HullType.ColonyShip)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
