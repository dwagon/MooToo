from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 250
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchTachyonCommunications(Research):
    def __init__(self):
        super().__init__("Tachyon Communications", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchTachyonScanner(Research):
    def __init__(self):
        super().__init__("Tachyon Scanner", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchBattleScanner(Research):
    def __init__(self):
        super().__init__("Battle Scanner", RESEARCH_POINTS, CATEGORY)
