from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchElectronicComputers(Research):
    def __init__(self):
        super().__init__("Electronic Computers", RESEARCH_POINTS, CATEGORY)
