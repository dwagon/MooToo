import unittest

from MooToo.construct import Construct, ConstructType
from MooToo.constants import Building
from MooToo.galaxy import Galaxy
from MooToo.ship_design import ShipDesign, HullType


#################################################################################################
class TestConstruct(unittest.TestCase):
    def setUp(self):
        self.galaxy = Galaxy()
        frigate_design = ShipDesign(HullType.Frigate)
        self.frigate_design_id = self.galaxy.add_design(frigate_design)

    def test_creation(self):
        b = Construct(ConstructType.BUILDING, self.galaxy, building_tag=Building.STOCK_EXCHANGE)
        self.assertIsNone(b.design_id)
        s = Construct(ConstructType.SHIP, self.galaxy, design_id=self.frigate_design_id)
        self.assertIsNone(s.tag)
        self.assertEqual(s.design_id, self.frigate_design_id)

    def test_cost(self):
        b = Construct(ConstructType.BUILDING, self.galaxy, building_tag=Building.STOCK_EXCHANGE)
        self.assertEqual(b.cost, 150)
        s = Construct(ConstructType.SPY, self.galaxy)
        self.assertEqual(s.cost, 100)


#################################################################################################
if __name__ == "__main__":
    unittest.main()
