from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingPleasureDome(PlanetBuilding):

    def __init__(self):
        super().__init__("Pleasure Dome", Building.PLEASURE_DOME)
        self.maintenance = 3
        self.cost = 250
