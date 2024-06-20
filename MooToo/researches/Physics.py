from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 50
CATEGORY = TechCategory.PHYSICS
general = [Technology.LASER_CANNON, Technology.LASER_RIFLE, Technology.SPACE_SCANNER]


#####################################################################################################
class ResearchLaserCannon(Research):
    def __init__(self):
        super().__init__("Laser Cannon", Technology.LASER_CANNON, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class ResearchLaserRifle(Research):
    def __init__(self):
        super().__init__("Laser Rifle", Technology.LASER_RIFLE, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class ResearchSpaceScanner(Research):
    def __init__(self):
        super().__init__("Space Scanner", Technology.SPACE_SCANNER, RESEARCH_POINTS, CATEGORY)
        self.general = general
