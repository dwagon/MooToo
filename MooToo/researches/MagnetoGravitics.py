from MooToo.research import Research, ResearchCategory
from MooToo.buildings.PlanetaryRadiationShield import BuildingPlanetaryRadiationShield

RESEARCH_POINTS = 900
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassIIIShield(Research):
    def __init__(self):
        super().__init__("Class III Shield", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlanetaryRadiationShield(Research):
    def __init__(self):
        super().__init__("Planetary Radiation Shield", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPlanetaryRadiationShield()


#####################################################################################################
class ResearchWarpDissipater(Research):
    def __init__(self):
        super().__init__("Warp Dissipater", RESEARCH_POINTS, CATEGORY)
