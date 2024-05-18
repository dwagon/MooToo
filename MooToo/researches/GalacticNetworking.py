from MooToo.research import Research, ResearchCategory
from MooToo.buildings.GalacticCybernet import BuildingGalacticCybernet

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchVirtualRealityNetwork(Research):
    def __init__(self):
        super().__init__("Virtual Reality Network", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGalacticCybernet(Research):
    def __init__(self):
        super().__init__("Galactic Cybernet", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingGalacticCybernet()
