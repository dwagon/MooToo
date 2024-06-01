from MooToo.research import Research, ResearchCategory
from MooToo.buildings.Recyclotron import BuildingRecyclotron
from MooToo.constants import Technology

RESEARCH_POINTS = 1500
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchRecyclotron(Research):
    def __init__(self):
        super().__init__("Recyclotron", Technology.RECYCLOTRON, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingRecyclotron()


#####################################################################################################
class ResearchAutomatedRepairUnit(Research):
    def __init__(self):
        super().__init__("Automated Repair Unit", Technology.AUTOMATED_REPAIR_UNIT, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchArtificialPlanetConstruction(Research):
    def __init__(self):
        super().__init__("Artificial Planet", Technology.ARTIFICIAL_PLANET, RESEARCH_POINTS, CATEGORY)
