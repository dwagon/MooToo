from MooToo.research import Research, ResearchCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm
from MooToo.constants import Technology

RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchTerraforming(Research):
    def __init__(self):
        super().__init__("Terraforming", Technology.TERRAFORMING, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()
