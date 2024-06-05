from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingDeepCoreMine(PlanetBuilding):

    def __init__(self):
        super().__init__("Deep Core Mine", Building.DEEP_CORE_MINE)
        self.maintenance = 3
        self.cost = 250
