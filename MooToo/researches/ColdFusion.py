from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 80
CATEGORY = ResearchCategory.POWER
general = [Technology.COLONY_SHIP, Technology.OUTPOST_SHIP, Technology.TRANSPORT]


#####################################################################################################
class ResearchColonyShip(Research):
    def __init__(self):
        super().__init__("Colony Ship", Technology.COLONY_SHIP, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class ResearchOutpostShip(Research):
    def __init__(self):
        super().__init__("Outpost Ship", Technology.OUTPOST_SHIP, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class ResearchTransport(Research):
    def __init__(self):
        super().__init__("Transport", Technology.TRANSPORT, RESEARCH_POINTS, CATEGORY)
        self.general = general
