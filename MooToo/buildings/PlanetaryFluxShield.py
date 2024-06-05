from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingPlanetaryFluxShield(PlanetBuilding):

    def __init__(self):
        super().__init__("Planetary Flux Shield", Building.PLANETARY_FLUX_SHIELD)
        self.maintenance = 3
        self.cost = 200
