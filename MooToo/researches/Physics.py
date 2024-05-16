from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchLaserCannon(Research):
    def __init__(self):
        super().__init__("Laser Cannon", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchLaserRifle(Research):
    def __init__(self):
        super().__init__("Laser Rifle", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSpaceScanner(Research):
    def __init__(self):
        super().__init__("Space Scanner", RESEARCH_POINTS, CATEGORY)
