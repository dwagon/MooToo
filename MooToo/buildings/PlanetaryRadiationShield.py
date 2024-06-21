from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingPlanetaryRadiationShield(PlanetBuilding):

    def __init__(self):
        super().__init__("Planetary Radiation Shield", Building.PLANETARY_RADIATION_SHIELD)
        self.maintenance = 1
        self.cost = 80
