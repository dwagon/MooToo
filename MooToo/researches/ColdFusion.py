from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 80
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchColonyShip(Research):
    def __init__(self):
        super().__init__("Colony Ship", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchOutpostShip(Research):
    def __init__(self):
        super().__init__("Outpost Ship", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchTransport(Research):
    def __init__(self):
        super().__init__("Transport", RESEARCH_POINTS, CATEGORY)
