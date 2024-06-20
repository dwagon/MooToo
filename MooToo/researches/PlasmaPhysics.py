from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 3000
CATEGORY = TechCategory.PHYSICS


#####################################################################################################
class ResearchPlasmaCannon(Research):
    def __init__(self):
        super().__init__("Plasma Cannon", Technology.PLASMA_CANNON, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlasmaRifle(Research):
    def __init__(self):
        super().__init__("Plasma Rifle", Technology.PLASMA_RIFLE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlasmaWeb(Research):
    def __init__(self):
        super().__init__("Plasma Web", Technology.PLASMA_WEB, RESEARCH_POINTS, CATEGORY)
