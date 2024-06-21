from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingCoreWasteDump(PlanetBuilding):

    def __init__(self):
        super().__init__("Core Waste Dump", Building.CORE_WASTE_DUMP)
        self.maintenance = 8
        self.cost = 200
