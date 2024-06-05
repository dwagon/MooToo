from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingArtemisSystemNet(PlanetBuilding):

    def __init__(self):
        super().__init__("Artemis System Net", Building.ARTEMIS_SYSTEM_NET)
        self.maintenance = 5
        self.cost = 1000
