""" Galaxy Creation
"""

import math
import random
from MooToo.galaxy import Galaxy
from MooToo.empire import Empire
from MooToo.ship_design import ShipDesign, HullType
from MooToo.system import System
from MooToo.planet import Planet
from MooToo.names import EMPIRE_NAMES, EMPIRE_COLOURS, ORBIT_NAMES, SYSTEM_NAMES
from MooToo.constants import (
    GalaxySize,
    GalaxySizeKeys,
    GALAXY_SIZE_DATA,
    STAR_COLOURS,
    Technology,
    Building,
    NUM_EMPIRES,
    DISPLAY_MAX_X,
    DISPLAY_MAX_Y,
    MAX_ORBITS,
    MIN_DIST,
    StarColour,
    PlanetClimate,
    PlanetSize,
    PlanetCategory,
    PlanetRichness,
    PlanetGravity,
    PopulationJobs,
)
from MooToo.utils import (
    get_distance_tuple,
    PlanetId,
    EmpireId,
    SystemId,
    get_distance,
    prob_map,
)


#################################################################################################
def create_galaxy(tech: str = "avg", size: GalaxySize = GalaxySize.LARGE) -> Galaxy:
    """Fill the galaxy with things"""
    planet_id_generator = unique_planet_id()
    galaxy = Galaxy(size)
    create_systems(galaxy, GALAXY_SIZE_DATA[size][GalaxySizeKeys.NUM_SYSTEMS])
    create_empires(galaxy, tech, planet_id_generator)
    create_planets(galaxy, planet_id_generator)
    assert min(galaxy.systems.keys()) == 1
    assert min(galaxy.empires.keys()) == 1
    assert min(galaxy.planets.keys()) == 1
    return galaxy


#####################################################################################################
def create_planets(galaxy: Galaxy, id_generator):
    for system_id in galaxy.systems.keys():
        make_orbits(galaxy, system_id, id_generator)


#####################################################################################################
def create_empires(galaxy: Galaxy, tech: str, planet_id_generator):
    names = EMPIRE_NAMES[:]
    colours = EMPIRE_COLOURS[:]
    emp_id_generator = unique_empire_id()
    for home_system in find_home_systems(galaxy, NUM_EMPIRES):
        empire_name = pick_empire_name(names)
        colour = pick_colour(colours)
        empire_id: EmpireId = next(emp_id_generator)
        make_empire(empire_name, empire_id, next(planet_id_generator), colour, home_system, galaxy)
        base_designs(galaxy, empire_id)
        match tech:
            case "pre":
                pre_start(empire_id, galaxy)
            case "avg":
                average_start(empire_id, galaxy)
            case "adv":
                advanced_start(empire_id, galaxy)


#####################################################################################################
def base_designs(galaxy: Galaxy, empire_id: EmpireId) -> None:
    """Base designs that are the same every game"""
    coloniser = ShipDesign(HullType.ColonyShip, "Colony")
    galaxy.add_design(coloniser, empire_id)
    transport = ShipDesign(HullType.Transport, "Transport")
    galaxy.add_design(transport, empire_id)


#####################################################################################################
def unique_empire_id() -> EmpireId:
    counter = 1  # Empire 0 is no empire
    while True:
        yield counter
        counter += 1


#####################################################################################################
def unique_planet_id() -> PlanetId:
    counter = 1  # Planet 0 is no planet
    while True:
        yield counter
        counter += 1


#####################################################################################################
def create_systems(galaxy: Galaxy, num_systems) -> None:
    positions = get_system_positions(num_systems)
    sys_id_generator = unique_system_id()
    for _ in range(num_systems):
        position = random.choice(positions)
        positions.remove(position)
        system_id = next(sys_id_generator)
        name = pick_system_name()
        colour = pick_star_colour()
        system = System(system_id, name, colour, position, galaxy)
        galaxy.systems[system_id] = system


#####################################################################################################
def unique_system_id() -> SystemId:
    counter = 1
    while True:
        yield counter
        counter += 1


#####################################################################################################
def find_home_systems(galaxy: Galaxy, num_empires: int) -> list[SystemId]:
    """Find suitable planets for home planets"""
    # Create an arc around the galaxy and put home planets evenly spaced around that arc
    home_systems = []
    arc_distance = 360 // num_empires
    radius = min(DISPLAY_MAX_X, DISPLAY_MAX_Y) * 0.75 / 2
    for degree in range(0, 359, arc_distance):
        angle = math.radians(degree)
        position = (
            radius * math.cos(angle) + DISPLAY_MAX_X / 2,
            radius * math.sin(angle) + DISPLAY_MAX_Y / 2,
        )
        # Find the system closest to this point
        min_dist = 999999
        min_system = None
        for system in galaxy.systems.values():
            distance = get_distance_tuple(position, system.position)
            if distance < min_dist:
                min_dist = distance
                min_system = system
        home_systems.append(min_system.id)
    return home_systems


#####################################################################################################
def make_orbits(galaxy: Galaxy, system_id: SystemId, id_generator):
    system = galaxy.systems[system_id]
    for _ in range(MAX_ORBITS - len(system.orbits)):
        pct = random.randint(0, 100)
        if pct <= STAR_COLOURS[system.colour]["prob_orbit"]:
            planet_id = next(id_generator)
            make_planet(galaxy, planet_id, system_id, system)
        else:
            system.add_planet(None)

    # Name the planets
    random.shuffle(system.orbits)
    for name_index, planet_id in enumerate(system.planets):
        planet = galaxy.planets[planet_id]
        if not planet.name:
            planet.name = f"{system.name} {ORBIT_NAMES[name_index]}"


#####################################################################################################
def make_planet(galaxy: Galaxy, planet_id: PlanetId, system_id: SystemId, system: System):
    size = pick_planet_size()
    richness = pick_planet_richness(STAR_COLOURS[system.colour]["richness"])
    planet = Planet(
        planet_id,
        system_id,
        galaxy,
        category=pick_planet_category(),
        size=size,
        richness=richness,
        climate=pick_planet_climate(STAR_COLOURS[system.colour]["climate"]),
        gravity=pick_planet_gravity(size, richness),
    )

    system.add_planet(planet.id)
    galaxy.planets[planet.id] = planet


#####################################################################################################
def make_empire(
    empire_name: str,
    empire_id: EmpireId,
    planet_id: PlanetId,
    empire_colour: str,
    home_system_id: SystemId,
    galaxy: Galaxy,
) -> Empire:
    """ """
    home_system = galaxy.systems[home_system_id]
    home_system.colour = StarColour.YELLOW
    empire = Empire(empire_id, empire_name, empire_colour, galaxy)
    galaxy.empires[empire.id] = empire
    home_planet_id = make_home_planet(home_system.id, planet_id, galaxy)
    set_home_planet(galaxy, empire_id, home_planet_id)
    home_system.orbits.append(home_planet_id)
    return empire


#####################################################################################################
def make_home_planet(system_id: SystemId, planet_id: PlanetId, galaxy: "Galaxy") -> PlanetId:
    """Return a suitable home planet in {system}"""
    p = Planet(
        planet_id,
        system_id,
        galaxy,
        category=PlanetCategory.PLANET,
        climate=PlanetClimate.TERRAN,
        size=PlanetSize.LARGE,
        richness=PlanetRichness.ABUNDANT,
        gravity=PlanetGravity.NORMAL,
    )
    galaxy.planets[p.id] = p
    p.climate_image = p.gen_climate_image()
    return p.id


#####################################################################################################
def set_home_planet(galaxy: Galaxy, empire_id: EmpireId, planet_id: PlanetId):
    """Make planet the home planet of the empire"""
    planet = galaxy.planets[planet_id]
    empire = galaxy.empires[empire_id]
    planet.name = f"{empire.name} Home"
    planet.owner = empire.id
    planet.raw_population = 8e6
    planet.jobs[PopulationJobs.FARMERS] = 4
    planet.jobs[PopulationJobs.WORKERS] = 2
    planet.jobs[PopulationJobs.SCIENTISTS] = 2
    planet.buildings.add(Building.MARINE_BARRACKS)
    planet.buildings.add(Building.STAR_BASE)
    empire.owned_planets.add(planet_id)
    empire.know_system(planet.system_id)


#####################################################################################################
def get_system_positions(num_systems: int) -> list[tuple[int, int]]:
    """Return suitable positions"""
    positions = []
    for _ in range(num_systems):
        while True:
            x = random.randrange(MIN_DIST, DISPLAY_MAX_X - MIN_DIST)
            y = random.randrange(MIN_DIST, DISPLAY_MAX_Y - MIN_DIST)
            for a, b in positions:  # Find a spot not too close to existing positions
                if get_distance(x, y, a, b) < MIN_DIST:
                    break
            else:
                positions.append((x, y))
                break
    return positions


#####################################################################################################
def pick_empire_name(names: list[str]):
    name = random.choice(names)
    names.remove(name)
    return name


#####################################################################################################
def pick_colour(colours: list[str]):
    colour = random.choice(colours)
    colours.remove(colour)

    return colour


#####################################################################################################
def pre_start(empire_id: EmpireId, galaxy: Galaxy) -> None:
    """Start with pre-tech"""
    empire = galaxy.empires[empire_id]
    home_planet_id = list(empire.owned_planets)[0]
    home_planet = galaxy.planets[home_planet_id]
    home_planet.buildings.add(Building.MARINE_BARRACKS)
    home_planet.buildings.add(Building.STAR_BASE)
    empire.learnt(Technology.STAR_BASE)
    empire.learnt(Technology.MARINE_BARRACKS)
    empire.learnt(Technology.COLONY_BASE)


#####################################################################################################
def average_start(empire_id: EmpireId, galaxy: Galaxy) -> None:
    """Start with average tech"""
    empire = galaxy.empires[empire_id]
    home_system_id = list(empire.known_systems)[0]
    pre_start(empire_id, galaxy)
    empire.learnt(Technology.STANDARD_FUEL_CELLS)
    empire.learnt(Technology.NUCLEAR_DRIVE)
    empire.learnt(Technology.COLONY_SHIP)
    empire.learnt(Technology.OUTPOST_SHIP)
    empire.learnt(Technology.TRANSPORT)

    frigate_design = ShipDesign(HullType.Frigate, "Scout")
    frigate_design_id = galaxy.add_design(frigate_design, empire_id)

    colony_design_id = [num for num, _ in galaxy.designs.items() if _.hull == HullType.ColonyShip][0]
    empire.build_ship_design(frigate_design_id, home_system_id)
    empire.build_ship_design(frigate_design_id, home_system_id)
    empire.build_ship_design(colony_design_id, home_system_id)


#####################################################################################################
def advanced_start(empire_id: EmpireId, galaxy: Galaxy) -> None:
    """Start with advanced tech"""
    average_start(empire_id, galaxy)
    # Do more stuff


#####################################################################################################
def pick_planet_climate(config: dict[str, int]) -> PlanetClimate:
    """Climate of the planet depends on the star colour"""
    climate = prob_map(config)
    return PlanetClimate(climate)


#####################################################################################################
def pick_planet_richness(config: dict[str, int]) -> PlanetRichness:
    richness = prob_map(config)
    return PlanetRichness(richness)


#####################################################################################################
def pick_planet_gravity(size: PlanetSize, richness: PlanetRichness) -> PlanetGravity:
    """The bigger and richer the planet the higher the gravity"""
    grav_map = {
        PlanetSize.TINY: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.LOW,
            PlanetRichness.POOR: PlanetGravity.LOW,
            PlanetRichness.ABUNDANT: PlanetGravity.LOW,
            PlanetRichness.RICH: PlanetGravity.NORMAL,
            PlanetRichness.ULTRA_RICH: PlanetGravity.NORMAL,
        },
        PlanetSize.SMALL: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.LOW,
            PlanetRichness.POOR: PlanetGravity.LOW,
            PlanetRichness.ABUNDANT: PlanetGravity.NORMAL,
            PlanetRichness.RICH: PlanetGravity.NORMAL,
            PlanetRichness.ULTRA_RICH: PlanetGravity.NORMAL,
        },
        PlanetSize.MEDIUM: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.LOW,
            PlanetRichness.POOR: PlanetGravity.NORMAL,
            PlanetRichness.ABUNDANT: PlanetGravity.NORMAL,
            PlanetRichness.RICH: PlanetGravity.NORMAL,
            PlanetRichness.ULTRA_RICH: PlanetGravity.HIGH,
        },
        PlanetSize.LARGE: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.NORMAL,
            PlanetRichness.POOR: PlanetGravity.NORMAL,
            PlanetRichness.ABUNDANT: PlanetGravity.NORMAL,
            PlanetRichness.RICH: PlanetGravity.HIGH,
            PlanetRichness.ULTRA_RICH: PlanetGravity.HIGH,
        },
        PlanetSize.HUGE: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.NORMAL,
            PlanetRichness.POOR: PlanetGravity.NORMAL,
            PlanetRichness.ABUNDANT: PlanetGravity.HIGH,
            PlanetRichness.RICH: PlanetGravity.HIGH,
            PlanetRichness.ULTRA_RICH: PlanetGravity.HIGH,
        },
    }
    return grav_map[size][richness]


#####################################################################################################
def pick_planet_size() -> PlanetSize:
    pct = random.randrange(1, 100)
    if pct < 10:
        return PlanetSize.TINY
    elif pct < 30:
        return PlanetSize.SMALL
    elif pct < 70:
        return PlanetSize.MEDIUM
    elif pct < 90:
        return PlanetSize.LARGE
    return PlanetSize.HUGE


#####################################################################################################
def pick_planet_category() -> PlanetCategory:
    """What sort of planet is this?"""
    pct = random.randrange(1, 100)
    if pct < 20:
        return PlanetCategory.ASTEROID
    elif pct < 40:
        return PlanetCategory.GAS_GIANT
    return PlanetCategory.PLANET


#####################################################################################################
def pick_system_name() -> str:
    """Pick a system name"""
    name = random.choice(SYSTEM_NAMES)
    SYSTEM_NAMES.remove(name)
    return name


#####################################################################################################
def pick_star_colour() -> StarColour:
    while True:
        pct = random.randint(0, 100)
        prev = 0
        for colour, details in STAR_COLOURS.items():
            if pct <= prev + details["probability"]:
                return StarColour(colour)
            else:
                prev += details["probability"]
