from MooToo.research import Research, ResearchCategory
from MooToo.buildings.DeepCoreMine import BuildingDeepCoreMine
from MooToo.buildings.CoreWasteDump import BuildingCoreWasteDump
from MooToo.constants import Technology

RESEARCH_POINTS = 3500
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchDeepCoreMine(Research):
    def __init__(self):
        super().__init__("Deep Core Mine", Technology.DEEP_CORE_MINE, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingDeepCoreMine()


#####################################################################################################
class ResearchCoreWasteDump(Research):
    def __init__(self):
        super().__init__("Core Waste Dump", Technology.CORE_WASTE_DUMP, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingCoreWasteDump()
