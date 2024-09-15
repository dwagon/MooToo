import unittest

from MooToo.bigbang import create_galaxy
from MooToo.construct import Construct, ConstructType
from MooToo.constants import Building
from MooToo.ship_design import ShipDesign, HullType


#################################################################################################
class TestConstruct(unittest.TestCase):
    def setUp(self):
        self.galaxy = create_galaxy()
        self.empire_id = 1
        frigate_design = ShipDesign(HullType.Frigate)
        self.frigate_design_id = self.galaxy.add_design(frigate_design, self.empire_id)

    def test_creation(self):
        b = Construct(ConstructType.BUILDING, building_tag=Building.STOCK_EXCHANGE)
        self.assertIsNone(b.design_id)
        s = Construct(ConstructType.SHIP, design_id=self.frigate_design_id)
        self.assertIsNone(s.building_tag)
        self.assertEqual(s.design_id, self.frigate_design_id)

    def test_cost(self):
        b = Construct(ConstructType.BUILDING, building_tag=Building.STOCK_EXCHANGE)
        self.assertEqual(b.cost(self.galaxy), 150)
        s = Construct(ConstructType.SPY)
        self.assertEqual(s.cost(self.galaxy), 100)


#################################################################################################
if __name__ == "__main__":
    unittest.main()
