from MooToo.research import Research, TechCategory
from MooToo.buildings.GalacticCybernet import BuildingGalacticCybernet
from MooToo.constants import Technology

RESEARCH_POINTS = 4500
CATEGORY = TechCategory.COMPUTERS


#####################################################################################################
class ResearchVirtualRealityNetwork(Research):
    def __init__(self):
        super().__init__("Virtual Reality Network", Technology.VIRTUAL_REALITY_NETWORKING, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGalacticCybernet(Research):
    def __init__(self):
        super().__init__("Galactic Cybernet", Technology.GALACTIC_CYBERNET, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingGalacticCybernet()
