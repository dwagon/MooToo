import unittest
from MooToo.constants import (
    Building,
    PopulationJobs,
    Technology,
    PlanetSize,
    PlanetClimate,
    PlanetRichness,
    PlanetGravity,
    StarColour,
)
from MooToo.ship_design import HullType
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
        self.system = System(99, "test", StarColour.WHITE, (0, 0), self.galaxy)
        self.galaxy.systems[self.system.id] = self.system

    #################################################################################################
    def test_colonize(self):
        new_planet = Planet(99, self.system.id, self.galaxy, climate=PlanetClimate.TERRAN)
        self.galaxy.planets[new_planet.id] = new_planet
        new_planet.colonize(self.empire.id)
        self.assertEqual(new_planet.current_population(), 1)
        self.assertEqual(new_planet.jobs[PopulationJobs.FARMERS], 1)
        self.assertEqual(new_planet.jobs[PopulationJobs.WORKERS], 0)
        self.assertIn(new_planet.id, self.empire.owned_planets)

        new_planet = Planet(100, self.system.id, self.galaxy, climate=PlanetClimate.BARREN)
        self.galaxy.planets[new_planet.id] = new_planet
        new_planet.colonize(self.empire.id)
        self.assertEqual(new_planet.jobs[PopulationJobs.FARMERS], 0)
        self.assertEqual(new_planet.jobs[PopulationJobs.WORKERS], 1)

    #################################################################################################
    def test_max_population(self):
        planet = Planet(99, self.system.id, self.galaxy)
        planet.size = PlanetSize.MEDIUM
        planet.climate = PlanetClimate.TERRAN
        self.assertEqual(planet.max_population(), 16)

    #################################################################################################
    def test_finish_construction(self):
        planet = Planet(99, self.system.id, self.galaxy)
        con = Construct(ConstructType.BUILDING, building_tag=Building.MARINE_BARRACKS)
        self.assertNotIn(Building.MARINE_BARRACKS, planet.buildings)
        planet._finish_construction(con)
        self.assertIn(Building.MARINE_BARRACKS, planet.buildings)

    #################################################################################################
    def test_building_production(self):
        """Test finishing a building"""
        planet = Planet(99, self.system.id, self.galaxy)
        planet.build_queue.add(Building.MARINE_BARRACKS)
        planet.construction_spent = 59
        planet.jobs[PopulationJobs.WORKERS] = 5
        planet._building_production()
        self.assertIn(Building.MARINE_BARRACKS, planet.buildings)
        self.assertLess(planet.construction_spent, 59)
        self.assertNotIn(Building.MARINE_BARRACKS, planet.build_queue)

    #################################################################################################
    def test_available_to_build(self):
        planet = Planet(99, self.system.id, self.galaxy)
        planet.owner = self.empire.id
        self.assertIn(Building.HOUSING, planet.available_to_build())
        self.assertIn(Building.MARINE_BARRACKS, planet.available_to_build())
        planet.buildings.add(Building.MARINE_BARRACKS)
        self.assertNotIn(Building.MARINE_BARRACKS, planet.available_to_build())

    #################################################################################################
    def test_can_build_ship(self):
        planet = Planet(101, self.system.id, self.galaxy)
        planet.owner = self.empire.id
        self.assertFalse(planet.can_build_ship(HullType.Frigate))
        self.empire.learnt(Technology.NUCLEAR_DRIVE)
        self.assertFalse(planet.can_build_ship(HullType.Frigate))
        self.empire.learnt(Technology.STANDARD_FUEL_CELLS)
        self.assertTrue(planet.can_build_ship(HullType.Frigate))
        self.assertFalse(planet.can_build_ship(HullType.Battleship))
        planet.buildings.add(Building.STAR_BASE)
        self.assertTrue(planet.can_build_ship(HullType.Battleship))

    #################################################################################################
    def test_turns_to_build(self):
        planet = Planet(
            102,
            self.system.id,
            self.galaxy,
            size=PlanetSize.MEDIUM,
            gravity=PlanetGravity.NORMAL,
            richness=PlanetRichness.ABUNDANT,
        )
        planet.build_queue.add(Building.AUTOMATED_FACTORY)
        planet.jobs[PopulationJobs.WORKERS] = 5  # Work Prod = 11 (15 prod -4 poll)
        planet.construction_spent = 20
        self.assertEqual(work_surplus(planet), 11)
        self.assertEqual(planet.turns_to_build(), int((60 - 20) / 11))

        planet.build_queue.pop()  # Remove existing
        planet.build_queue.add(Building.TRADE_GOODS)
        self.assertEqual(planet.turns_to_build(), 0)

    #################################################################################################
    def test_buy_cost(self):
        planet = Planet(103, self.system.id, self.galaxy)
        planet.build_queue.add(Building.AUTOMATED_FACTORY)
        self.assertEqual(planet.buy_cost(), 60 * 4)
        planet.construction_spent = 60
        self.assertEqual(planet.buy_cost(), 0)
        planet.construction_spent = 30
        self.assertEqual(planet.buy_cost(), (60 - 30) * 2)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
