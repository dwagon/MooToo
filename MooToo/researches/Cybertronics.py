from MooToo.research import Research, ResearchCategory
from MooToo.buildings.Autolab import BuildingAutolab

RESEARCH_POINTS = 2750
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchCybertronicComputer(Research):
    def __init__(self):
        super().__init__("Cybertronic Computer", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAutolab(Research):
    def __init__(self):
        super().__init__("Autolab", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAutolab()


#####################################################################################################
class ResearchStructuralAnalyzer(Research):
    def __init__(self):
        super().__init__("Structural Analyzer", RESEARCH_POINTS, CATEGORY)
