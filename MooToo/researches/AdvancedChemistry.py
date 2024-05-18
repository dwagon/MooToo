from MooToo.research import Research, ResearchCategory
from MooToo.buildings.PollutionProcessor import BuildingPollutionProcessor

RESEARCH_POINTS = 650
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchMerculiteMissile(Research):
    def __init__(self):
        super().__init__("Merculite Missile", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPollutionProcessor(Research):
    def __init__(self):
        super().__init__("PollutionProcessor", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPollutionProcessor()
