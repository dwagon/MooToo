from MooToo.research import Research, ResearchCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm

RESEARCH_POINTS = 900
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchTelepathicTraining(Research):
    def __init__(self):
        super().__init__("Telepathic Training", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMicrobiotics(Research):
    def __init__(self):
        super().__init__("Microbiotics", RESEARCH_POINTS, CATEGORY)
