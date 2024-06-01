from MooToo.research import Research, ResearchCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm
from MooToo.constants import Technology

RESEARCH_POINTS = 80
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchHydroponicFarm(Research):
    def __init__(self):
        super().__init__("Hydroponic Farm", Technology.HYDROPONIC_FARM, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()


#####################################################################################################
class ResearchBiosphere(Research):
    def __init__(self):
        super().__init__("Biosphere", Technology.BIOSPHERE, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()
