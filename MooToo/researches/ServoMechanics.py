from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 900
CATEGORY = TechCategory.CONSTRUCTION


#####################################################################################################
class ResearchFastMissileRacks(Research):
    def __init__(self):
        super().__init__("Fast Missile Racks", Technology.FAST_MISSILE_RACKS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAdvancedDamageControl(Research):
    def __init__(self):
        super().__init__("Advanced Damage Control", Technology.ADVANCED_DAMAGE_CONTROL, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAssaultShuttles(Research):
    def __init__(self):
        super().__init__("Assault Shuttles", Technology.ASSAULT_SHUTTLES, RESEARCH_POINTS, CATEGORY)
