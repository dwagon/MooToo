from MooToo.research import Research, ResearchCategory
from MooToo.buildings.ResearchLaboratory import BuildingResearchLaboratory
from MooToo.constants import Technology

RESEARCH_POINTS = 150
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchResearchLaboratory(Research):
    def __init__(self):
        super().__init__("Research Laboratory", Technology.RESEARCH_LABORATORY, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingResearchLaboratory()


#####################################################################################################
class ResearchOptronicComputer(Research):
    def __init__(self):
        super().__init__("Optronic Computer", Technology.OPTRONIC_COMPUTER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchDauntlessGuidanceSystem(Research):
    def __init__(self):
        super().__init__("Dauntless Guidance System", Technology.DAUNTLESS_GUIDANCE_SYSTEM, RESEARCH_POINTS, CATEGORY)
