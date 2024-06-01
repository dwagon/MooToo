from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 250
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchTachyonCommunications(Research):
    def __init__(self):
        super().__init__("Tachyon Communications", Technology.TACHYON_COMMUNICATIONS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchTachyonScanner(Research):
    def __init__(self):
        super().__init__("Tachyon Scanner", Technology.TACHYON_SCANNER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchBattleScanner(Research):
    def __init__(self):
        super().__init__("Battle Scanner", Technology.BATTLE_SCANNER, RESEARCH_POINTS, CATEGORY)
