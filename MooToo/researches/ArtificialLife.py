from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchBioTerminator(Research):
    def __init__(self):
        super().__init__("Bio Terminator", Technology.BIO_TERMINATOR, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchUniversalAntidote(Research):
    def __init__(self):
        super().__init__("Universal Antidote", Technology.UNIVERSAL_ANTIDOTE, RESEARCH_POINTS, CATEGORY)
