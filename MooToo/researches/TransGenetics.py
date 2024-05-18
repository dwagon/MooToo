from MooToo.research import Research, ResearchCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm

RESEARCH_POINTS = 7500
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchBiomorphicFungi(Research):
    def __init__(self):
        super().__init__("Biomorphic Fungi", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGaiaTransformation(Research):
    def __init__(self):
        super().__init__("Gaia Transformation", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()


#####################################################################################################
class ResearchEvolutionaryMutation(Research):
    def __init__(self):
        super().__init__("Evolutionary Mutation", RESEARCH_POINTS, CATEGORY)
