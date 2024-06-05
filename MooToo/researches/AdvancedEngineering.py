from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 80
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class AntiMissileRockets(Research):
    def __init__(self):
        super().__init__("Anti-Missile Rockets", Technology.ANTI_MISSILE_ROCKETS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class FighterBays(Research):
    def __init__(self):
        super().__init__("Fighter Bays", Technology.FIGHTER_BAYS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ReinforcedHull(Research):
    def __init__(self):
        super().__init__("Reinforced Hull", Technology.REINFORCED_HULL, RESEARCH_POINTS, CATEGORY)
