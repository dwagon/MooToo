from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 80
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class AntiMissileRockets(Research):
    def __init__(self):
        super().__init__("Colony Base", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class FighterBays(Research):
    def __init__(self):
        super().__init__("Colony Base", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ReinforcedHull(Research):
    def __init__(self):
        super().__init__("Colony Base", RESEARCH_POINTS, CATEGORY)
