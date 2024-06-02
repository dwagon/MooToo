from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingPlanetaryBarrierShield(PlanetBuilding):

    def __init__(self):
        super().__init__("Planetary Barrier Shield", Building.PLANETARY_BARRIER_SHIELD)
        self.maintenance = 5
        self.cost = 500
