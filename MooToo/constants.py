from enum import Enum, StrEnum, auto

MOO_PATH = "/Applications/Master of Orion 2.app/Contents/Resources/game"


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
    FARMER = "F"
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
