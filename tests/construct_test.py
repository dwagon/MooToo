import unittest

from MooToo.construct import Construct, ConstructType
from MooToo.constants import Building
from MooToo.ship import select_ship_type_by_name
from MooToo.galaxy import Galaxy


#################################################################################################
class TestConstruct(unittest.TestCase):
    def setUp(self):
        self.galaxy = Galaxy()

    def test_creation(self):
        b = Construct(ConstructType.BUILDING, building_tag=Building.STOCK_EXCHANGE)
        self.assertIsNone(b.ship)
        ship = select_ship_type_by_name("Frigate", self.galaxy)
        s = Construct(ConstructType.SHIP, ship=ship)
        self.assertIsNone(s.tag)
        self.assertEqual(s.ship, ship)

    def test_cost(self):
        b = Construct(ConstructType.BUILDING, building_tag=Building.STOCK_EXCHANGE)
        self.assertEqual(b.cost, 150)
        s = Construct(ConstructType.SHIP, ship=select_ship_type_by_name("Frigate", self.galaxy))
        self.assertEqual(s.cost, 25)


#################################################################################################
if __name__ == "__main__":
    unittest.main()
