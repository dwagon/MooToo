from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 250
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchFusionDrive(Research):
    def __init__(self):
        super().__init__("Fusion Drive", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchFusionBomb(Research):
    def __init__(self):
        super().__init__("Fusion Bomb", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAugmentedEngine(Research):
    def __init__(self):
        super().__init__("Augmented Engine", RESEARCH_POINTS, CATEGORY)
