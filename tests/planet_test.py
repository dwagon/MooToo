import unittest
from MooToo.constants import Building, PopulationJobs, Technology
from MooToo.ship import ShipType
from MooToo.galaxy import Galaxy
from MooToo.system import System
from MooToo.empire import Empire
from MooToo.planet import Planet, PlanetSize, PlanetClimate


#####################################################################################################
class TestPlanet(unittest.TestCase):
    def setUp(self):
        self.galaxy = Galaxy()
        self.system = System(1, (0, 0), self.galaxy)
        self.planet = Planet(self.system, self.galaxy)
        self.empire = Empire("PlayerOne", self.galaxy)
        self.galaxy.empires["PlayerOne"] = self.empire
        self.planet.owner = "PlayerOne"

    #################################################################################################
    def test_max_population(self):
        self.planet.size = PlanetSize.MEDIUM
        self.planet.climate = PlanetClimate.TERRAN
        self.assertEqual(self.planet.max_population(), 16)

    #################################################################################################
    def test_add_to_build_queue(self):
        """Test add_to_build_queue()"""
        bld = Building.MARINE_BARRACKS
        self.planet.add_to_build_queue(bld)
        self.assertEqual(self.planet.build_queue[0], Building.MARINE_BARRACKS)

    #################################################################################################
    def test_toggle_build_queue(self):
        self.planet.toggle_build_queue_item(Building.MARINE_BARRACKS)
        self.assertIn(Building.MARINE_BARRACKS, self.planet.build_queue)
        self.planet.toggle_build_queue_item(Building.MARINE_BARRACKS)
        self.assertNotIn(Building.MARINE_BARRACKS, self.planet.build_queue)

    #################################################################################################
    def test_finish_construction(self):
        self.assertNotIn(Building.MARINE_BARRACKS, self.planet.buildings)
        self.planet.finish_construction(Building.MARINE_BARRACKS)
        self.assertIn(Building.MARINE_BARRACKS, self.planet.buildings)

    #################################################################################################
    def test_building_production(self):
        """Test finishing a building"""
        self.planet.add_to_build_queue(Building.MARINE_BARRACKS)
        self.planet.construction_spent = 59
        self.planet.jobs[PopulationJobs.WORKERS] = 5
        self.planet.building_production()
        self.assertIn(Building.MARINE_BARRACKS, self.planet.buildings)
        self.assertLess(self.planet.construction_spent, 59)
        self.assertNotIn(Building.MARINE_BARRACKS, self.planet.build_queue)

    #################################################################################################
    def test_available_to_build(self):
        self.assertIn(Building.HOUSING, self.planet.available_to_build())
        self.assertIn(Building.MARINE_BARRACKS, self.planet.available_to_build())
        self.planet.buildings.add(Building.MARINE_BARRACKS)
        self.assertNotIn(Building.MARINE_BARRACKS, self.planet.available_to_build())

    #################################################################################################
    def test_get_research_points(self):
        self.planet.jobs[PopulationJobs.SCIENTISTS] = 1
        self.assertEqual(self.planet.get_research_points(), 1)

    #################################################################################################
    def test_can_build_ship(self):
        planet = Planet(self.system, self.galaxy)
        planet.owner = self.empire.name
        self.assertFalse(planet.can_build_ship(ShipType.Frigate))
        self.empire.learnt(Technology.NUCLEAR_DRIVE)
        self.assertFalse(planet.can_build_ship(ShipType.Frigate))
        self.empire.learnt(Technology.STANDARD_FUEL_CELLS)
        self.assertTrue(planet.can_build_ship(ShipType.Frigate))
        self.assertFalse(planet.can_build_ship(ShipType.Battleship))
        planet.buildings.add(Building.STAR_BASE)
        self.assertTrue(planet.can_build_ship(ShipType.Battleship))


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
