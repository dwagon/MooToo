from MooToo.research import Research, ResearchCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm
from MooToo.constants import Technology

RESEARCH_POINTS = 7500
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchBiomorphicFungi(Research):
    def __init__(self):
        super().__init__("Biomorphic Fungi", Technology.BIOMORPHIC_FUNGI, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGaiaTransformation(Research):
    def __init__(self):
        super().__init__("Gaia Transformation", Technology.GAIA_TRANSFORMATION, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()


#####################################################################################################
class ResearchEvolutionaryMutation(Research):
    def __init__(self):
        super().__init__("Evolutionary Mutation", Technology.EVOLUTIONARY_MUTATION, RESEARCH_POINTS, CATEGORY)
