from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingPollutionProcessor(PlanetBuilding):

    def __init__(self):
        super().__init__("Pollution Processor", Building.POLLUTION_PROCESSOR)
        self.maintenance = 1
        self.cost = 80
