from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingResearchLaboratory(PlanetBuilding):

    def __init__(self):
        super().__init__("Research Laboratory", Building.RESEARCH_LABORATORY)
        self.maintenance = 1
        self.cost = 60
