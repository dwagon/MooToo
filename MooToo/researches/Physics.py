from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchLaserCannon(Research):
    def __init__(self):
        super().__init__("Laser Cannon", Technology.LASER_CANNON, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchLaserRifle(Research):
    def __init__(self):
        super().__init__("Laser Rifle", Technology.LASER_RIFLE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSpaceScanner(Research):
    def __init__(self):
        super().__init__("Space Scanner", Technology.SPACE_SCANNER, RESEARCH_POINTS, CATEGORY)
