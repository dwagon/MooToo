from MooToo.research import Research, ResearchCategory
from MooToo.buildings.GravityGenerator import BuildingGravityGenerator
from MooToo.constants import Technology

RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchTractorBeam(Research):
    def __init__(self):
        super().__init__("Tractor Beam", Technology.TRACTOR_BEAM, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGravitonBeam(Research):
    def __init__(self):
        super().__init__("Graviton Beam", Technology.GRAVITON_BEAM, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGravityGenerator(Research):
    def __init__(self):
        super().__init__("Gravity Generator", Technology.GRAVITY_GENERATOR, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingGravityGenerator()
