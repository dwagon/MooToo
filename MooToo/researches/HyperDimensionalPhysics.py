from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 6000
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchHyperspaceCommunications(Research):
    def __init__(self):
        super().__init__("Hyperspace Communications", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMaulerDevice(Research):
    def __init__(self):
        super().__init__("Mauler Device", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSensors(Research):
    def __init__(self):
        super().__init__("Sensors", RESEARCH_POINTS, CATEGORY)
