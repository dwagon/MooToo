import unittest

from MooToo.bigbang import get_system_positions, find_home_systems, create_galaxy
from MooToo.constants import Technology, NUM_SYSTEMS, NUM_EMPIRES
from MooToo.empire import Empire
from MooToo.planet import Planet
from MooToo.ship import Ship
from MooToo.ship_design import HullType
from MooToo.system import System


#####################################################################################################
class TestBigBang(unittest.TestCase):
    def test_get_system_positions(self):
        positions = get_system_positions(5)
        self.assertEqual(len(positions), 5)

    #################################################################################################
    def test_galaxy_creation(self):
        galaxy = create_galaxy()
        self.assertEqual(len(galaxy.systems), NUM_SYSTEMS)
        self.assertEqual(len(galaxy.empires), NUM_EMPIRES)
        self.assertEqual(len(galaxy.ships), NUM_EMPIRES * 3)
        self.assertTrue(all(isinstance(_, System) for _ in galaxy.systems.values()))
        self.assertTrue(all(isinstance(_, Empire) for _ in galaxy.empires.values()))
        self.assertTrue(all(isinstance(_, Planet) for _ in galaxy.planets.values()))
        self.assertTrue(all(isinstance(_, Ship) for _ in galaxy.ships.values()))
        self.assertEqual(galaxy.turn_number, 0)

    #################################################################################################
    def test_find_home_systems(self):
        galaxy = create_galaxy()
        systems = find_home_systems(galaxy, 3)
        self.assertEqual(len(systems), 3)

    #################################################################################################
    def test_default_start(self):
        galaxy = create_galaxy("avg")
        empire_number = 1
        self.assertIn(Technology.COLONY_SHIP, galaxy.empires[empire_number].known_techs)

        player_ships = [galaxy.ships[_] for _ in galaxy.empires[empire_number].ships]
        self.assertEqual(len(player_ships), 3)
        self.assertTrue(all(_.owner == empire_number for _ in player_ships))

        empire_design_ids = galaxy.empires[empire_number].designs
        empire_designs = [galaxy.designs[_] for _ in empire_design_ids]

        # Scout Frigate
        frigate_design = [design for design in empire_designs if design.hull == HullType.Frigate][0]
        frigates = [_ for _ in player_ships if _.design_id == frigate_design.id]
        self.assertEqual(len(frigates), 2)
        design_id = frigates[0].design_id
        self.assertEqual(galaxy.designs[design_id].hull, HullType.Frigate)

        # Colony ship
        colony_design = [design for design in empire_designs if design.hull == HullType.ColonyShip][0]
        colonies = [_ for _ in player_ships if _.design_id == colony_design.id]
        self.assertEqual(len(colonies), 1)

        self.assertEqual(len(galaxy.ships), 3 * len(galaxy.empires))

    #################################################################################################
    def test_pre_start(self):
        galaxy = create_galaxy("pre")
        self.assertNotIn(Technology.COLONY_SHIP, galaxy.empires[1].known_techs)

    #################################################################################################
    def test_advanced_start(self):
        galaxy = create_galaxy("adv")
        self.assertIn(Technology.COLONY_SHIP, galaxy.empires[1].known_techs)

    #################################################################################################
    def test_planet_uniqueness(self):
        """Make sure each planet only occurs in one system"""
        galaxy = create_galaxy("pre")
        seen_planets = set()
        for system in galaxy.systems.values():
            for planet_id in system.planets:
                if planet_id in seen_planets:
                    self.fail(f"Duplicate planet: {planet_id}")
                else:
                    seen_planets.add(planet_id)

    #################################################################################################
    def test_system_planet_references(self):
        """Planets system reference points to the correct system"""
        galaxy = create_galaxy("pre")
        for system_id, system in galaxy.systems.items():
            for planet_id in system.planets:
                self.assertEqual(galaxy.planets[planet_id].system_id, system_id)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
