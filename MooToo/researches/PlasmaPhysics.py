from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 3000
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchPlasmaCannon(Research):
    def __init__(self):
        super().__init__("Plasma Cannon", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlasmaRifle(Research):
    def __init__(self):
        super().__init__("Plasma Rifle", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlasmaWeb(Research):
    def __init__(self):
        super().__init__("Plasma Web", RESEARCH_POINTS, CATEGORY)
