""" Relating to player's empires"""

from collections import defaultdict, namedtuple
from typing import TYPE_CHECKING, Optional
from MooToo.constants import Technology, PopulationJobs
from MooToo.research import TechCategory
from MooToo.ship import Ship
from MooToo.utils import (
    all_research,
    get_research,
    get_distance_tuple,
    EmpireId,
    SystemId,
    PlanetId,
    ShipId,
    DesignId,
)
from MooToo.planet_science import science_surplus
from MooToo.planet_money import money_surplus
from MooToo.planet_food import food_surplus


if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy

#####################################################################################################
Migration = namedtuple("Migration", "dst_planet dst_job arrival_time")


#####################################################################################################
#####################################################################################################
class Empire:
    def __init__(self, empire_id: EmpireId, name: str, colour: str, galaxy: "Galaxy"):
        self.id = empire_id
        self.name = name
        self.colour = colour
        self.galaxy = galaxy
        self.government = "Feudal"  # Fix me
        self.money: int = 100
        self.income: int = 0
        self.designs: set[DesignId] = set()
        self.known_systems: set[SystemId] = set()
        self.owned_planets: set[PlanetId] = set()
        self.ships: set[ShipId] = set()
        self.researching: Technology | None = None
        self.research_spent = 0
        self.freighters = 0
        self.researched: dict[TechCategory, int] = {
            TechCategory.FORCE_FIELDS: 0,
            TechCategory.BIOLOGY: 0,
            TechCategory.POWER: 0,
            TechCategory.PHYSICS: 0,
            TechCategory.COMPUTERS: 0,
            TechCategory.SOCIOLOGY: 0,
            TechCategory.CONSTRUCTION: 0,
            TechCategory.CHEMISTRY: 0,
        }  # What category / price has been researched
        self.known_techs: set[Technology] = set()
        self.migrations: list[Migration] = []

    #####################################################################################################
    def __repr__(self):
        return f"<Empire {self.id} {self.name}>"

    #####################################################################################################
    def freighters_used(self) -> int:
        need_food = 0
        have_food = 0
        for planet_id in self.owned_planets:
            surplus = food_surplus(self.galaxy.planets[planet_id])
            if surplus < 0:
                need_food += surplus
            elif surplus > 0:
                have_food += surplus
        freighters_needed = len(self.migrations) * 5
        freighters_needed -= min(have_food, need_food)

        return min(freighters_needed, self.freighters)

    #####################################################################################################
    def migrate(
        self,
        num: int,
        src_planet_id: PlanetId,
        src_job: PopulationJobs,
        dst_planet_id: PlanetId,
        dst_job: PopulationJobs,
    ):
        """Migrate population around the empire"""
        src_planet = self.galaxy.planets[src_planet_id]
        dst_planet = self.galaxy.planets[dst_planet_id]

        # Same system is instantaneous
        if src_planet_id == dst_planet_id:
            src_planet.remove_workers(num, src_job)
            dst_planet.add_workers(num, dst_job)
            return

        print(f"DBG Migrating {num} {src_job} from {src_planet_id} to {dst_job} at {dst_planet_id}")
        src_system = self.galaxy.systems[src_planet.system_id]
        dst_system = self.galaxy.systems[dst_planet.system_id]
        distance = get_distance_tuple(src_system.position, dst_system.position)
        arrival_time = self.galaxy.turn_number + distance // 5  # 5 = speed of freighter
        for _ in range(num):
            src_planet.remove_workers(num, src_job)
            self.migrations.append(Migration(dst_job=dst_job, dst_planet=dst_planet_id, arrival_time=arrival_time))

    #####################################################################################################
    def own_planet(self, planet_id: PlanetId):
        self.owned_planets.add(planet_id)

    #####################################################################################################
    def colonize(self, planet_id: PlanetId, colonizer: ShipId) -> None:
        """Colonize the planet"""
        planet = self.galaxy.planets[planet_id]
        planet.colonize(self.id)
        self.own_planet(planet_id)
        self.delete_ship(colonizer)

    #####################################################################################################
    def in_range(self, destination_id: SystemId, ship_id: ShipId) -> bool:
        _range = self.galaxy.ships[ship_id].range
        for planet_id in self.owned_planets:
            dist = self.galaxy.get_system_distance(destination_id, self.galaxy.planets[planet_id].system_id)
            if dist <= _range:
                return True
        return False

    #####################################################################################################
    def build_ship_design(self, design_id: DesignId, system_id: SystemId, name: str = "") -> ShipId:
        if not name:
            name = self.galaxy.designs[design_id].name
        ship = Ship(name, design_id, self.galaxy)
        self._add_ship(ship, system_id)
        return ship.id

    #####################################################################################################
    def _add_ship(self, ship: Ship, system_id: SystemId):
        assert isinstance(system_id, SystemId)
        self.ships.add(ship.id)
        self.galaxy.ships[ship.id] = ship
        system = self.galaxy.systems[system_id]
        ship.orbit = system_id
        ship.location = system.position
        ship.owner = self.id

    #####################################################################################################
    def delete_ship(self, ship_id: ShipId):
        self.ships.remove(ship_id)
        del self.galaxy.ships[ship_id]

    #####################################################################################################
    def turn(self):
        """Have a turn"""
        self.research_spent += self.get_research_points()
        if self.researching and self.research_spent > get_research(self.researching).cost:
            self.research_spent -= get_research(self.researching).cost
            self.learnt(self.researching)
            self.researching = None
        income = 0
        for planet_id in self.owned_planets:
            planet = self.galaxy.planets[planet_id]
            planet.turn()
            income += money_surplus(planet)
        for ship_id in list(self.ships)[:]:
            ship = self.galaxy.ships[ship_id]
            ship.turn()
            if ship.orbit is not None:
                self.know_system(ship.orbit)
        for migration in self.migrations[:]:
            if migration.arrival_time >= self.galaxy.turn_number:
                migration.dst_planet.add_workers(1, migration.dst_job)
                self.migrations.remove(migration)
        income -= self.freighters_used() // 2
        self.income = income
        self.money += self.income

    #####################################################################################################
    def send_coloniser(self, dest_planet_id: PlanetId) -> Optional[ShipId]:
        """Send a colony ship to the planet"""
        for ship_id in self.ships:
            ship = self.galaxy.ships[ship_id]
            if not ship.coloniser:
                continue
            if not ship.destination:
                ship.set_destination_planet(dest_planet_id)
                return ship_id
        # Make smarter - pick closest coloniser to dest_planet

    #####################################################################################################
    def start_researching(self, to_research: Technology) -> None:
        self.researching = to_research

    #####################################################################################################
    def learnt(self, tech: Technology) -> None:
        """We have researched {tech}"""
        self.known_techs.add(tech)
        research = get_research(tech)
        if research.general:
            for gen_tech in research.general:
                self.known_techs.add(gen_tech)
        self.researched[research.category] = research.cost

    #####################################################################################################
    def next_research(self, category: "TechCategory") -> list[Technology]:
        """What are the next techs that can be researched"""
        available: dict[int, list[Technology]] = defaultdict(list)

        for tech, research in all_research().items():
            if research.category != category:
                continue
            if tech in self.known_techs:
                continue
            if research.cost <= self.researched[category]:
                continue

            available[research.cost].append(tech)
        if not available:
            return []
        next_batch_cost = min(list(available.keys()))

        return available[next_batch_cost]

    #####################################################################################################
    def get_research_points(self) -> int:
        rp = 0
        for planet_id in self.owned_planets:
            planet = self.galaxy.planets[planet_id]
            rp += science_surplus(planet)
        return rp

    #####################################################################################################
    def has_interest_in(self, system_id: SystemId) -> bool:
        assert isinstance(system_id, SystemId)
        for planet_id in self.galaxy.systems[system_id].planets:
            planet = self.galaxy.planets[planet_id]
            if planet and planet.owner == self.id:
                return True
        return False

    #####################################################################################################
    def know_system(self, system_id: SystemId) -> None:
        assert isinstance(system_id, SystemId), f"{system_id=}"
        self.known_systems.add(system_id)

    #####################################################################################################
    def is_known_system(self, system_id: SystemId) -> bool:
        """Is the system known to this empire"""
        assert isinstance(system_id, SystemId)
        return system_id in self.known_systems
