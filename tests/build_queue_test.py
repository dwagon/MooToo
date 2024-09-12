import unittest

from MooToo.build_queue import BuildQueue
from MooToo.bigbang import create_galaxy
from MooToo.constants import Building, StarColour
from MooToo.construct import Construct, ConstructType
from MooToo.system import System
from MooToo.planet import Planet
from MooToo.empire import Empire


#################################################################################################
class TestBuildQueue(unittest.TestCase):
    def setUp(self):
        self.galaxy = create_galaxy()
        system = System(99, "test", StarColour.WHITE, (0, 0), self.galaxy)
        self.galaxy.systems[system.id] = system
        planet = Planet(99, system.id, self.galaxy)
        self.galaxy.planets[planet.id] = planet
        self.empire = Empire(99, "Foo", "purple", self.galaxy)
        planet.owner = self.empire
        self.q = BuildQueue(planet)

    #############################################################################################
    def test_add(self):
        self.q.add(Building.MARINE_BARRACKS)
        self.assertEqual(type(self.q._queue[0]), Construct)
        self.assertEqual(self.q._queue[0].building_tag, Building.MARINE_BARRACKS)

        self.q.add(ConstructType.SPY)
        self.assertEqual(type(self.q._queue[1]), Construct)
        self.assertEqual(len(self.q), 2)

    #############################################################################################
    def test_cost(self):
        self.q.add(ConstructType.SPY)
        self.assertEqual(self.q.cost, 100)

    #############################################################################################
    def test_is_building(self):
        self.q.add(Building.MARINE_BARRACKS)
        self.assertTrue(self.q.is_building(Building.MARINE_BARRACKS))
        self.assertFalse(self.q.is_building(Building.STAR_BASE))

    #################################################################################################
    def test_in(self):
        self.q.add(Building.MARINE_BARRACKS)
        self.q.add(Building.BATTLESTATION)
        self.assertIn(Building.BATTLESTATION, self.q)
        self.assertNotIn(Building.TRADE_GOODS, self.q)
        con = Construct(ConstructType.BUILDING, building_tag=Building.MARINE_BARRACKS)
        self.assertIn(con, self.q)

    #################################################################################################
    def test_toggle_build_queue(self):
        self.q.toggle(Building.MARINE_BARRACKS)
        self.assertIn(Building.MARINE_BARRACKS, self.q)
        self.q.toggle(Building.MARINE_BARRACKS)
        self.assertNotIn(Building.MARINE_BARRACKS, self.q)


#################################################################################################
if __name__ == "__main__":
    unittest.main()

# EOF
