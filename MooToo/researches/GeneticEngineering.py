from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 900
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchTelepathicTraining(Research):
    def __init__(self):
        super().__init__("Telepathic Training", Technology.TELEPATHIC_TRAINING, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMicrobiotics(Research):
    def __init__(self):
        super().__init__("Microbiotics", Technology.MICROBIOTICS, RESEARCH_POINTS, CATEGORY)
