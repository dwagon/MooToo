from MooToo.research import Research, ResearchCategory
from MooToo.buildings.GravityGenerator import BuildingGravityGenerator

RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchTractorBeam(Research):
    def __init__(self):
        super().__init__("Tractor Beam", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGravitonBeam(Research):
    def __init__(self):
        super().__init__("Graviton Beam", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGravityGenerator(Research):
    def __init__(self):
        super().__init__("Gravity Generator", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingGravityGenerator()
