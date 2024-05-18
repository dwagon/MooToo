from MooToo.research import Research, ResearchCategory


RESEARCH_POINTS = 900
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchFastMissileRacks(Research):
    def __init__(self):
        super().__init__("Fast Missile Racks", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAdvancedDamageControl(Research):
    def __init__(self):
        super().__init__("Advanced Damage Control", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAssaultShuttles(Research):
    def __init__(self):
        super().__init__("Assault Shuttles", RESEARCH_POINTS, CATEGORY)
