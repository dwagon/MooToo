from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchAntiMatterDrive(Research):
    def __init__(self):
        super().__init__("Anti-Matter Drive", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAntiMatterTorpedoes(Research):
    def __init__(self):
        super().__init__("Anti-Matter Torpedoes", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAntiMatterBomb(Research):
    def __init__(self):
        super().__init__("Anti-Matter Bomb", RESEARCH_POINTS, CATEGORY)
