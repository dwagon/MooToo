from MooToo.research import Research, ResearchCategory
from MooToo.buildings.Recyclotron import BuildingRecyclotron

RESEARCH_POINTS = 1500
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchRecyclotron(Research):
    def __init__(self):
        super().__init__("Recyclotron", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingRecyclotron()


#####################################################################################################
class ResearchAutomatedRepairUnit(Research):
    def __init__(self):
        super().__init__("Automated Repair Unit", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchArtificialPlanetConstruction(Research):
    def __init__(self):
        super().__init__("Artificial Planet", RESEARCH_POINTS, CATEGORY)
