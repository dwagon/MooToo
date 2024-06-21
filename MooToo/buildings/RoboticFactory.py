from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import PlanetRichness, Building
from MooToo.planet import Planet


#####################################################################################################
class BuildingRoboticFactory(PlanetBuilding):
    """The Robotic Factory uses self-repairing robotic systems and generates its own replacement parts and machinery.
    The resulting efficiency boost adds to the colony’s output according to the minerals
    available: +5 on Ultra Poor worlds, +8 for Poor, +10 on Abundant planets, +15 for Rich,
    and +20 on Ultra Rich worlds.
    """

    def __init__(self):
        super().__init__("Robotic Factory", Building.ROBOTIC_FACTORY)
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
