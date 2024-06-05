from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 250
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchFusionDrive(Research):
    def __init__(self):
        super().__init__("Fusion Drive", Technology.FUSION_DRIVE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchFusionBomb(Research):
    def __init__(self):
        super().__init__("Fusion Bomb", Technology.FUSION_BOMB, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAugmentedEngine(Research):
    def __init__(self):
        super().__init__("Augmented Engine", Technology.AUGMENTED_ENGINE, RESEARCH_POINTS, CATEGORY)
