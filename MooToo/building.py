""" Buildings"""

from MooToo.planet import Planet
from MooToo.constants import PlanetRichness


#####################################################################################################
class Building:
    """Building"""

    def __init__(self, name):
        self.name = name
        self.maintenance = 0
        self.cost = 0

    def __str__(self):
        return self.name

    def food_bonus(self, planet: Planet) -> int:
        return 0

    def prod_bonus(self, planet: Planet) -> int:
        return 0


#####################################################################################################
class HydroponicFarm(Building):
    """The Hydroponic Farm is an automated, sealed environment in which food is grown,
    even on otherwise lifeless worlds. The Farm increases the food output of a colony by 2."""

    def __init__(self):
        super().__init__("Hydroponic Farm")
        self.maintenance = 2
        self.cost = 60

    def food_bonus(self, planet: Planet) -> int:
        return 2


#####################################################################################################
class AutomatedFactory(Building):
    """Automated factories aid workers, increasing the output of each industrial unit of population by
    +1 production each turn and giving the colony +5 production."""

    def __init__(self):
        super().__init__("Automated Factory")
        self.maintenance = 2
        self.cost = 60

    def prod_bonus(self, planet: Planet) -> int:
        return planet.current_population() + 5


#####################################################################################################
class RoboticFactory(Building):
    """The Robotic Factory uses self-repairing robotic systems and generates its own replacement parts and machinery.
    The resulting efficiency boost adds to the colony’s output according to the minerals
    available: +5 on Ultra Poor worlds, +8 for Poor, +10 on Abundant planets, +15 for Rich,
    and +20 on Ultra Rich worlds.
    """

    def __init__(self):
        super().__init__("Robotic Factory")
        self.maintenance = 3
        self.cost = 200

    def prod_bonus(self, planet: Planet) -> int:
        """ """
        match planet.richness:
            case PlanetRichness.ULTRA_POOR:
                return 5
            case PlanetRichness.POOR:
                return 8
            case PlanetRichness.ABUNDANT:
                return 10
            case PlanetRichness.RICH:
                return 15
            case PlanetRichness.ULTRA_RICH:
                return 20
