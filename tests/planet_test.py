import unittest
from MooToo.constants import (
    Building,
    PopulationJobs,
    Technology,
    PlanetSize,
    PlanetClimate,
    PlanetRichness,
    PlanetGravity,
)
from MooToo.ship import ShipType, select_ship_type_by_name
from MooToo.bigbang import create_galaxy
from MooToo.system import System
from MooToo.construct import Construct, ConstructType
from MooToo.planet import Planet
from MooToo.planet_work import work_surplus


#####################################################################################################
class TestPlanet(unittest.TestCase):
    def setUp(self):
        self.galaxy = create_galaxy("pre")
        self.empire = self.galaxy.empires[1]
        self.system = System(99, "test", "purple", (0, 0), self.galaxy)

    #################################################################################################
    def test_colonize(self):
        new_planet = Planet(99, self.system, self.galaxy, climate=PlanetClimate.TERRAN)
        new_planet.colonize(1)
        self.assertEqual(new_planet.current_population(), 1)
        self.assertEqual(new_planet.jobs[PopulationJobs.FARMERS], 1)
        self.assertEqual(new_planet.jobs[PopulationJobs.WORKERS], 0)
        self.assertIn(new_planet, self.empire.owned_planets)

        new_planet = Planet(100, self.system, self.galaxy, climate=PlanetClimate.BARREN)
        new_planet.colonize(1)
        self.assertEqual(new_planet.jobs[PopulationJobs.FARMERS], 0)
        self.assertEqual(new_planet.jobs[PopulationJobs.WORKERS], 1)

    #################################################################################################
    def test_max_population(self):
        planet = Planet(99, self.system, self.galaxy)
        planet.size = PlanetSize.MEDIUM
        planet.climate = PlanetClimate.TERRAN
        self.assertEqual(planet.max_population(), 16)

    #################################################################################################
    def test_finish_construction(self):
        planet = Planet(99, self.system, self.galaxy)
        con = Construct(ConstructType.BUILDING, building_tag=Building.MARINE_BARRACKS)
        self.assertNotIn(Building.MARINE_BARRACKS, planet.buildings)
        planet.finish_construction(con)
        self.assertIn(Building.MARINE_BARRACKS, planet.buildings)

    #################################################################################################
    def test_building_production(self):
        """Test finishing a building"""
        planet = Planet(99, self.system, self.galaxy)
        planet.build_queue.add(Building.MARINE_BARRACKS)
        planet.construction_spent = 59
        planet.jobs[PopulationJobs.WORKERS] = 5
        planet.building_production()
        self.assertIn(Building.MARINE_BARRACKS, planet.buildings)
        self.assertLess(planet.construction_spent, 59)
        self.assertNotIn(Building.MARINE_BARRACKS, planet.build_queue)

    #################################################################################################
    def test_available_to_build(self):
        planet = Planet(99, self.system, self.galaxy)
        planet.owner = self.empire.id
        self.assertIn(Building.HOUSING, planet.available_to_build())
        self.assertIn(Building.MARINE_BARRACKS, planet.available_to_build())
        planet.buildings.add(Building.MARINE_BARRACKS)
        self.assertNotIn(Building.MARINE_BARRACKS, planet.available_to_build())

    #################################################################################################
    def test_can_build_ship(self):
        planet = Planet(101, self.system, self.galaxy)
        planet.owner = self.empire.id
        self.assertFalse(planet.can_build_ship(ShipType.Frigate))
        self.empire.learnt(Technology.NUCLEAR_DRIVE)
        self.assertFalse(planet.can_build_ship(ShipType.Frigate))
        self.empire.learnt(Technology.STANDARD_FUEL_CELLS)
        self.assertTrue(planet.can_build_ship(ShipType.Frigate))
        self.assertFalse(planet.can_build_ship(ShipType.Battleship))
        planet.buildings.add(Building.STAR_BASE)
        self.assertTrue(planet.can_build_ship(ShipType.Battleship))

    #################################################################################################
    def test_turns_to_build(self):
        planet = Planet(
            102,
            self.system,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            gravity=PlanetGravity.NORMAL,
            richness=PlanetRichness.ABUNDANT,
        )
        ship = select_ship_type_by_name("Battleship", self.galaxy)
        planet.build_queue.add(ship)
        planet.jobs[PopulationJobs.WORKERS] = 5  # Work Prod = 11 (15 prod -4 poll)
        planet.construction_spent = 200
        self.assertEqual(work_surplus(planet), 11)
        self.assertEqual(planet.turns_to_build(), int((725 - 200) / 11))

        planet.build_queue.pop()  # Remove existing
        planet.build_queue.add(Building.TRADE_GOODS)
        self.assertEqual(planet.turns_to_build(), 0)

    #################################################################################################
    def test_buy_cost(self):
        planet = Planet(103, self.system, self.galaxy)
        ship = select_ship_type_by_name("Battleship", self.galaxy)  # Cost 725
        planet.build_queue.add(ship)
        self.assertEqual(planet.buy_cost(), 2900)
        planet.construction_spent = 725
        self.assertEqual(planet.buy_cost(), 0)
        planet.construction_spent = 700
        self.assertEqual(planet.buy_cost(), 50)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
