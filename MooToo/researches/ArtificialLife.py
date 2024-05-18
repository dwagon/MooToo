from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchBioTerminator(Research):
    def __init__(self):
        super().__init__("Bio Terminator", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchUniversalAntidote(Research):
    def __init__(self):
        super().__init__("Universal Antidote", RESEARCH_POINTS, CATEGORY)
