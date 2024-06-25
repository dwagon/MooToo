from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingAtmosphericRenewer(PlanetBuilding):

    def __init__(self):
        super().__init__("Atmospheric Renewer", Building.ATMOSPHERIC_RENEWER)
        self.maintenance = 3
        self.cost = 150

    def pollution_divisor(self, planet: "Planet") -> int:
        return 4
