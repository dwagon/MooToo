from MooToo.research import Research, ResearchCategory
from MooToo.buildings.ResearchLaboratory import BuildingResearchLaboratory

RESEARCH_POINTS = 150
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchResearchLaboratory(Research):
    def __init__(self):
        super().__init__("Research Laboratory", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingResearchLaboratory()


#####################################################################################################
class ResearchOptronicComputer(Research):
    def __init__(self):
        super().__init__("Optronic Computer", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchDauntlessGuidanceSystem(Research):
    def __init__(self):
        super().__init__("Dauntless Guidance System", RESEARCH_POINTS, CATEGORY)
