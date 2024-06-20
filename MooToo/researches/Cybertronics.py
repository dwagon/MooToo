from MooToo.research import Research, TechCategory
from MooToo.buildings.Autolab import BuildingAutolab
from MooToo.constants import Technology

RESEARCH_POINTS = 2750
CATEGORY = TechCategory.COMPUTERS


#####################################################################################################
class ResearchCybertronicComputer(Research):
    def __init__(self):
        super().__init__("Cybertronic Computer", Technology.CYBERTRONIC_COMPUTER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAutolab(Research):
    def __init__(self):
        super().__init__("Autolab", Technology.AUTOLOAB, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAutolab()


#####################################################################################################
class ResearchStructuralAnalyzer(Research):
    def __init__(self):
        super().__init__("Structural Analyzer", Technology.STRUCTURAL_ANALYZER, RESEARCH_POINTS, CATEGORY)
