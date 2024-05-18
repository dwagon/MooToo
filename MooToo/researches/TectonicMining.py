from MooToo.research import Research, ResearchCategory
from MooToo.buildings.DeepCoreMine import BuildingDeepCoreMine
from MooToo.buildings.CoreWasteDump import BuildingCoreWasteDump

RESEARCH_POINTS = 3500
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchDeepCoreMine(Research):
    def __init__(self):
        super().__init__("Deep Core Mine", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingDeepCoreMine()


#####################################################################################################
class ResearchCoreWasteDump(Research):
    def __init__(self):
        super().__init__("Core Waste Dump", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingCoreWasteDump()
