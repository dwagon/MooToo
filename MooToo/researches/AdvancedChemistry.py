from MooToo.research import Research, ResearchCategory
from MooToo.buildings.PollutionProcessor import BuildingPollutionProcessor
from MooToo.constants import Technology

RESEARCH_POINTS = 650
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchMerculiteMissile(Research):
    def __init__(self):
        super().__init__("Merculite Missile", Technology.MERCULITE_MISSILE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPollutionProcessor(Research):
    def __init__(self):
        super().__init__("PollutionProcessor", Technology.POLLUTION_PROCESSOR, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPollutionProcessor()
