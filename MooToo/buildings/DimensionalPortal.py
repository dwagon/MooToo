from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingDimensionalPortal(PlanetBuilding):

    def __init__(self):
        super().__init__("Dimensional Portal", Building.DIMENSIONAL_PORTAL)
        self.maintenance = 2
        self.cost = 500
