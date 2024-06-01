from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchElectronicComputers(Research):
    def __init__(self):
        super().__init__("Electronic Computers", Technology.ELECTRONIC_COMPUTERS, RESEARCH_POINTS, CATEGORY)
