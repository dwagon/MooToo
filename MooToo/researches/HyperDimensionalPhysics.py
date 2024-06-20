from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 6000
CATEGORY = TechCategory.PHYSICS


#####################################################################################################
class ResearchHyperspaceCommunications(Research):
    def __init__(self):
        super().__init__("Hyperspace Communications", Technology.HYPERSPACE_COMMUNICATIONS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMaulerDevice(Research):
    def __init__(self):
        super().__init__("Mauler Device", Technology.MAULER_DEVICE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSensors(Research):
    def __init__(self):
        super().__init__("Sensors", Technology.SENSORS, RESEARCH_POINTS, CATEGORY)
