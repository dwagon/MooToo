from enum import Enum, StrEnum, auto

MOO_PATH = "/Applications/Master of Orion 2.app/Contents/Resources/game"

MAX_ORBITS = 5
NUM_EMPIRES = 4
DISPLAY_MAX_X = 530
DISPLAY_MAX_Y = 420
MIN_DIST = 40  # Distance between systems


#####################################################################################################
class GalaxySize(StrEnum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    HUGE = auto()


#####################################################################################################
class GalaxySizeKeys(StrEnum):
    NUM_SYSTEMS = auto()
    WIDTH = auto()
    HEIGHT = auto()
    SCALE = auto()


#####################################################################################################
GALAXY_SIZE_DATA: dict[GalaxySize, dict[GalaxySizeKeys, int]] = {
    GalaxySize.SMALL: {
        GalaxySizeKeys.NUM_SYSTEMS: 20,
        GalaxySizeKeys.WIDTH: 25,
        GalaxySizeKeys.HEIGHT: 15,
        GalaxySizeKeys.SCALE: 21,
    },
    GalaxySize.MEDIUM: {
        GalaxySizeKeys.NUM_SYSTEMS: 36,
        GalaxySizeKeys.WIDTH: 25,
        GalaxySizeKeys.HEIGHT: 15,
        GalaxySizeKeys.SCALE: 21,
    },
    GalaxySize.LARGE: {
        GalaxySizeKeys.NUM_SYSTEMS: 54,
        GalaxySizeKeys.WIDTH: 30,
        GalaxySizeKeys.HEIGHT: 25,
        GalaxySizeKeys.SCALE: 16,
    },
    GalaxySize.HUGE: {
        GalaxySizeKeys.NUM_SYSTEMS: 72,
        GalaxySizeKeys.WIDTH: 40,
        GalaxySizeKeys.HEIGHT: 25,
        GalaxySizeKeys.SCALE: 13,
    },
}


#####################################################################################################
class PlanetCategory(Enum):
    ASTEROID = auto()
    PLANET = auto()
    GAS_GIANT = auto()


#####################################################################################################
class PlanetSize(StrEnum):
    TINY = "Tiny"
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    HUGE = "Huge"


#####################################################################################################
class PlanetGravity(StrEnum):
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"


#####################################################################################################
class PlanetRichness(StrEnum):
    ULTRA_POOR = "Ultra Poor"
    POOR = "Poor"
    ABUNDANT = "Abundant"
    RICH = "Rich"
    ULTRA_RICH = "Ultra Rich"


#####################################################################################################
class PlanetClimate(StrEnum):
    TOXIC = "Toxic"
    RADIATED = "Radiated"
    BARREN = "Barren"
    DESERT = "Desert"
    TUNDRA = "Tundra"
    OCEAN = "Ocean"
    SWAMP = "Swamp"
    ARID = "Arid"
    TERRAN = "Terran"
    GAIA = "Gaia"


#####################################################################################################
class PopulationJobs(StrEnum):
    FARMERS = "F"
    WORKERS = "W"
    SCIENTISTS = "S"


#####################################################################################################
class StarColour(StrEnum):
    BLUE = "blue"
    WHITE = "white"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"
    BROWN = "brown"


#####################################################################################################
class Building(StrEnum):
    """Names of buildings"""

    ALIEN_MANAGEMENT_CENTER = auto()
    ARMOUR_BARRACKS = auto()
    ARTEMIS_SYSTEM_NET = auto()
    ASTRO_UNIVERSITY = auto()
    ATMOSPHERIC_RENEWER = auto()
    AUTOLAB = auto()
    AUTOMATED_FACTORY = auto()
    BATTLESTATION = auto()
    BIOSPHERE = auto()
    CLONING_CENTER = auto()
    COLONY_BASE = auto()
    CORE_WASTE_DUMP = auto()
    DEEP_CORE_MINE = auto()
    DIMENSIONAL_PORTAL = auto()
    FIGHTER_GARRISON = auto()
    FOOD_REPLICATORS = auto()
    GAIA_TRANSFORMATION = auto()
    GALACTIC_CYBERNET = auto()
    GRAVITY_GENERATOR = auto()
    GROUND_BATTERIES = auto()
    HOLO_SIMULATOR = auto()
    HOUSING = auto()
    HYDROPONIC_FARM = auto()
    MARINE_BARRACKS = auto()
    PLANETARY_BARRIER_SHIELD = auto()
    PLANETARY_FLUX_SHIELD = auto()
    PLANETARY_RADIATION_SHIELD = auto()
    PLEASURE_DOME = auto()
    POLLUTION_PROCESSOR = auto()
    RECYCLOTRON = auto()
    RESEARCH_LABORATORY = auto()
    ROBOTIC_FACTORY = auto()
    ROBO_MINERS = auto()
    SOIL_ENRICHMENT = auto()
    SPACE_ACADEMY = auto()
    SPACE_PORT = auto()
    STAR_BASE = auto()
    STAR_FORTRESS = auto()
    STELLAR_CONVERTER = auto()
    STOCK_EXCHANGE = auto()
    SUBTERRANEAN_FARM = auto()
    SUPERCOMPUTER = auto()
    TERRAFORMING_1 = auto()
    TERRAFORMING_2 = auto()
    TERRAFORMING_3 = auto()
    TRADE_GOODS = auto()
    WARP_INTERDICTOR = auto()
    WEATHER_CONTROLLER = auto()


#####################################################################################################
class Technology(StrEnum):
    """Names of specific technologies that can be individually researched"""

    ACHILLES_TARGETING_UNIT = auto()
    ADAMANTIUM_ARMOUR = auto()
    ADVANCED_CITY_PLANNING = auto()
    ADVANCED_DAMAGE_CONTROL = auto()
    ADVANCED_GOVERNMENT = auto()
    ALIEN_MANAGEMENT_CENTER = auto()
    ANDROID_FARMERS = auto()
    ANDROID_SCIENTISTS = auto()
    ANDROID_WORKERS = auto()
    ANTI_GRAV_HARNESS = auto()
    ANTI_MATTER_BOMB = auto()
    ANTI_MATTER_DRIVE = auto()
    ANTI_MATTER_TORPEDOES = auto()
    ANTI_MISSILE_ROCKETS = auto()
    ARMOUR_BARRACKS = auto()
    ARTEMIS_SYSTEM_NET = auto()
    ARTIFICIAL_PLANET = auto()
    ASSAULT_SHUTTLES = auto()
    ASTRO_UNIVERSITY = auto()
    ATMOSPHERIC_RENEWER = auto()
    AUGMENTED_ENGINE = auto()
    AUTOLOAB = auto()
    AUTOMATED_FACTORY = auto()
    AUTOMATED_REPAIR_UNIT = auto()
    BATTLEOIDS = auto()
    BATTLESTATION = auto()
    BATTLE_PODS = auto()
    BATTLE_SCANNER = auto()
    BIOMORPHIC_FUNGI = auto()
    BIOSPHERE = auto()
    BIO_TERMINATOR = auto()
    BOMBER_BAYS = auto()
    CLASS_III_SHIELD = auto()
    CLASS_I_SHIELD = auto()
    CLASS_VII_SHIELD = auto()
    CLASS_V_SHIELD = auto()
    CLASS_X_SHIELD = auto()
    CLOAKING_DEVICE = auto()
    CLONING_CENTER = auto()
    COLONY_BASE = auto()
    COLONY_SHIP = auto()
    CORE_WASTE_DUMP = auto()
    CYBERTRONIC_COMPUTER = auto()
    CYBER_SECURITY_LINK = auto()
    DAUNTLESS_GUIDANCE_SYSTEM = auto()
    DEATH_SPORES = auto()
    DEEP_CORE_MINE = auto()
    DEUTERIUM_FUEL_CELLS = auto()
    DIMENSIONAL_PORTAL = auto()
    DISPLACEMENT_DEVICE = auto()
    DISRUPTOR_CANNON = auto()
    DOOM_STAR_CONSTRUCTION = auto()
    ECM_JAMMER = auto()
    ELECTRONIC_COMPUTERS = auto()
    EMISSIONS_GUIDANCE_SYSTEM = auto()
    ENERGY_ABSORBER = auto()
    EVOLUTIONARY_MUTATION = auto()
    EXTENDED_FUEL_TANKS = auto()
    FAST_MISSILE_RACKS = auto()
    FIGHTER_BAYS = auto()
    FIGHTER_GARRISON = auto()
    FOOD_REPLICATORS = auto()
    FREIGHTERS = auto()
    FUSION_BEAM = auto()
    FUSION_BOMB = auto()
    FUSION_DRIVE = auto()
    FUSION_RIFLE = auto()
    GAIA_TRANSFORMATION = auto()
    GALACTIC_CURRENCY_EXCHANGE = auto()
    GALACTIC_CYBERNET = auto()
    GAUSS_CANNON = auto()
    GRAVITON_BEAM = auto()
    GRAVITY_GENERATOR = auto()
    GROUND_BATTERIES = auto()
    GYRO_STABILIZER = auto()
    HARD_SHIELDS = auto()
    HEAVY_ARMOUR = auto()
    HEAVY_FIGHTERS = auto()
    HEIGHTENED_INTELLIGENCE = auto()
    HIGH_ENERGY_FOCUS = auto()
    HOLO_SIMULATOR = auto()
    HYDROPONIC_FARM = auto()
    HYPERSPACE_COMMUNICATIONS = auto()
    HYPER_DRIVE = auto()
    HYPER_X_CAPACITORS = auto()
    INTERPHASED_DRIVE = auto()
    INTERTIAL_NULLIFIER = auto()
    ION_DRIVE = auto()
    ION_PULSE_CANNON = auto()
    IRIDIUM_FUEL_CELLS = auto()
    JUMP_GATE = auto()
    LASER_CANNON = auto()
    LASER_RIFLE = auto()
    LIGHTNING_FIELD = auto()
    MARINE_BARRACKS = auto()
    MASS_DRIVER = auto()
    MAULER_DEVICE = auto()
    MEGAFLUXERS = auto()
    MERCULITE_MISSILE = auto()
    MICROBIOTICS = auto()
    MICROLITE_CONSTRUCTION = auto()
    MILITARY_TACTICS = auto()
    MISSILE_BASE = auto()
    MOLECULARTRONIC_COMPUTER = auto()
    MULTI_PHASED_SHIELDS = auto()
    MULTI_WAVE_ECM_JAMMER = auto()
    NANO_DISASSEMBLERS = auto()
    NEUTRONIUM_ARMOUR = auto()
    NEUTRONIUM_BOMB = auto()
    NEUTRON_BLASTER = auto()
    NEUTRON_SCANNER = auto()
    NUCLEAR_BOMB = auto()
    NUCLEAR_DRIVE = auto()
    NUCLEAR_MISSILE = auto()
    OPTRONIC_COMPUTER = auto()
    OUTPOST_SHIP = auto()
    PERSONAL_SHIELD = auto()
    PHASING_CLOAK = auto()
    PHASORS = auto()
    PHASOR_RIFLE = auto()
    PLANETARY_BARRIER_SHIELD = auto()
    PLANETARY_FLUX_SHIELD = auto()
    PLANETARY_RADIATION_SHIELD = auto()
    PLASMA_CANNON = auto()
    PLASMA_RIFLE = auto()
    PLASMA_TORPEDO = auto()
    PLASMA_WEB = auto()
    PLEASURE_DOME = auto()
    POLLUTION_PROCESSOR = auto()
    POSITRONIC_COMPUTER = auto()
    POWERED_ARMOUR = auto()
    PROTON_TORPEDO = auto()
    PSIONICS = auto()
    PULSAR = auto()
    PULSON_MISSILE = auto()
    RANGEMASTER_TARGETING_UNIT = auto()
    RECYCLOTRON = auto()
    REINFORCED_HULL = auto()
    RESEARCH_LABORATORY = auto()
    ROBOTIC_FACTORY = auto()
    ROBO_MINERS = auto()
    SENSORS = auto()
    SHIELD_CAPACITOR = auto()
    SOIL_ENRICHMENT = auto()
    SPACE_ACADEMY = auto()
    SPACE_PORT = auto()
    SPACE_SCANNER = auto()
    STANDARD_FUEL_CELLS = auto()
    STAR_BASE = auto()
    STAR_FORTRESS = auto()
    STAR_GATE = auto()
    STASIS_FIELD = auto()
    STEALTH_FIELD = auto()
    STEALTH_SUIT = auto()
    STELLAR_CONVERTER = auto()
    STOCK_EXCHANGE = auto()
    STRUCTURAL_ANALYZER = auto()
    SUBSPACE_COMMUNICATIONS = auto()
    SUBSPACE_TELEPORTER = auto()
    SUBTERRANEAN_FARMS = auto()
    SUPERCOMPUTER = auto()
    SURVIVAL_PODS = auto()
    TACHYON_COMMUNICATIONS = auto()
    TACHYON_SCANNER = auto()
    TELEPATHIC_TRAINING = auto()
    TERRAFORMING = auto()
    THORIUM_FUEL_CELLS = auto()
    TIME_WARP_FACILITATOR = auto()
    TITANIUM_ARMOUR = auto()
    TITAN_CONSTRUCTION = auto()
    TRACTOR_BEAM = auto()
    TRANSPORT = auto()
    TRANSPORTERS = auto()
    TRITANIUM_ARMOUR = auto()
    TROOP_PODS = auto()
    UNIVERSAL_ANTIDOTE = auto()
    URIDIUM_FUEL_CELLS = auto()
    VIRTUAL_REALITY_NETWORKING = auto()
    WARP_DISSIPATER = auto()
    WARP_INTERDICTOR = auto()
    WEATHER_CONTROLLER = auto()
    WIDE_AREA_JAMMER = auto()
    XENO_PSYCHOLOGY = auto()
    ZEON_MISSILE = auto()
    ZORTRIUM_ARMOR = auto()


#####################################################################################################
STAR_COLOURS = {
    StarColour.BLUE: {
        "climate": {
            "Toxic": 16,
            "Radiated": 50,
            "Barren": 27,
            "Desert": 7,
            "Tundra": 0,
            "Ocean": 0,
            "Swamp": 0,
            "Arid": 0,
            "Terran": 0,
            "Gaia": 0,
        },
        "richness": {"Ultra Poor": 0, "Poor": 0, "Abundant": 40, "Rich": 20, "Ultra Rich": 20},
        "probability": 2,
        "prob_orbit": 40,
    },
    StarColour.WHITE: {
        "climate": {
            "Toxic": 16,
            "Radiated": 37,
            "Barren": 27,
            "Desert": 6,
            "Tundra": 4,
            "Ocean": 2,
            "Swamp": 1,
            "Arid": 3,
            "Terran": 3,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 0, "Poor": 20, "Abundant": 40, "Rich": 30, "Ultra Rich": 10},
        "probability": 3,
        "prob_orbit": 35,
    },
    StarColour.YELLOW: {
        "climate": {
            "Toxic": 12,
            "Radiated": 27,
            "Barren": 30,
            "Desert": 6,
            "Tundra": 8,
            "Ocean": 5,
            "Swamp": 4,
            "Arid": 3,
            "Terran": 4,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 0, "Poor": 30, "Abundant": 40, "Rich": 20, "Ultra Rich": 10},
        "probability": 10,
        "prob_orbit": 45,
    },
    StarColour.ORANGE: {
        "climate": {
            "Toxic": 16,
            "Radiated": 17,
            "Barren": 23,
            "Desert": 8,
            "Tundra": 7,
            "Ocean": 6,
            "Swamp": 7,
            "Arid": 6,
            "Terran": 7,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 10, "Poor": 40, "Abundant": 40, "Rich": 10, "Ultra Rich": 0},
        "probability": 12,
        "prob_orbit": 45,
    },
    StarColour.RED: {
        "climate": {
            "Toxic": 16,
            "Radiated": 13,
            "Barren": 50,
            "Desert": 3,
            "Tundra": 7,
            "Ocean": 2,
            "Swamp": 2,
            "Arid": 2,
            "Terran": 4,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 20, "Poor": 40, "Abundant": 40, "Rich": 0, "Ultra Rich": 0},
        "probability": 68,
        "prob_orbit": 35,
    },
    StarColour.BROWN: {
        "climate": {
            "Toxic": 20,
            "Radiated": 30,
            "Barren": 10,
            "Desert": 20,
            "Tundra": 10,
            "Ocean": 2,
            "Swamp": 2,
            "Arid": 2,
            "Terran": 3,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 5, "Poor": 10, "Abundant": 60, "Rich": 20, "Ultra Rich": 5},
        "probability": 5,
        "prob_orbit": 25,
    },
}
GRAVITY_MAP: dict[PlanetGravity, float] = {
    PlanetGravity.LOW: 0.75,
    PlanetGravity.NORMAL: 1.0,
    PlanetGravity.HIGH: 0.5,
}

POP_SIZE_MAP: dict[PlanetSize, int] = {
    PlanetSize.TINY: 1,
    PlanetSize.SMALL: 2,
    PlanetSize.MEDIUM: 4,
    PlanetSize.LARGE: 5,
    PlanetSize.HUGE: 6,
}
POP_CLIMATE_MAP: dict[PlanetClimate, int] = {
    PlanetClimate.RADIATED: 1,
    PlanetClimate.TOXIC: 1,
    PlanetClimate.BARREN: 2,
    PlanetClimate.DESERT: 2,
    PlanetClimate.TUNDRA: 2,
    PlanetClimate.OCEAN: 3,
    PlanetClimate.SWAMP: 3,
    PlanetClimate.ARID: 3,
    PlanetClimate.TERRAN: 4,
    PlanetClimate.GAIA: 5,
}

FOOD_CLIMATE_MAP: dict[PlanetClimate:int] = {
    PlanetClimate.RADIATED: 0,
    PlanetClimate.TOXIC: 0,
    PlanetClimate.BARREN: 0,
    PlanetClimate.DESERT: 1,
    PlanetClimate.TUNDRA: 1,
    PlanetClimate.OCEAN: 2,
    PlanetClimate.SWAMP: 2,
    PlanetClimate.ARID: 1,
    PlanetClimate.TERRAN: 2,
    PlanetClimate.GAIA: 3,
}

PROD_RICHNESS_MAP: dict[PlanetRichness:int] = {
    PlanetRichness.ULTRA_POOR: 1,
    PlanetRichness.POOR: 2,
    PlanetRichness.ABUNDANT: 3,
    PlanetRichness.RICH: 5,
    PlanetRichness.ULTRA_RICH: 8,
}

# EOF
