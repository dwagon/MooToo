from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 80
CATEGORY = TechCategory.CONSTRUCTION


#####################################################################################################
class ResearchAntiMissileRockets(Research):
    def __init__(self):
        super().__init__("Anti-Missile Rockets", Technology.ANTI_MISSILE_ROCKETS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchFighterBays(Research):
    def __init__(self):
        super().__init__("Fighter Bays", Technology.FIGHTER_BAYS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchReinforcedHull(Research):
    def __init__(self):
        super().__init__("Reinforced Hull", Technology.REINFORCED_HULL, RESEARCH_POINTS, CATEGORY)
