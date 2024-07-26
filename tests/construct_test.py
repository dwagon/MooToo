import unittest

from MooToo.construct import Construct, ConstructType
from MooToo.constants import Building
from MooToo.ship import select_ship_type_by_name


#################################################################################################
class TestConstruct(unittest.TestCase):
    def test_creation(self):
        b = Construct(ConstructType.BUILDING, building_tag=Building.STOCK_EXCHANGE)
        self.assertIsNone(b.ship)
        ship = select_ship_type_by_name("Frigate")
        s = Construct(ConstructType.SHIP, ship=ship)
        self.assertIsNone(s.tag)
        self.assertEqual(s.ship, ship)

    def test_cost(self):
        b = Construct(ConstructType.BUILDING, building_tag=Building.STOCK_EXCHANGE)
        self.assertEqual(b.cost, 150)
        s = Construct(ConstructType.SHIP, ship=select_ship_type_by_name("Frigate"))
        self.assertEqual(s.cost, 25)


#################################################################################################
if __name__ == "__main__":
    unittest.main()
