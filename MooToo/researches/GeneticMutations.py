from MooToo.research import Research, ResearchCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm

RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchTerraforming(Research):
    def __init__(self):
        super().__init__("Terraforming", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()
