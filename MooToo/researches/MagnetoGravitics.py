from MooToo.research import Research, TechCategory
from MooToo.buildings.PlanetaryRadiationShield import BuildingPlanetaryRadiationShield
from MooToo.constants import Technology

RESEARCH_POINTS = 900
CATEGORY = TechCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassIIIShield(Research):
    def __init__(self):
        super().__init__("Class III Shield", Technology.CLASS_III_SHIELD, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlanetaryRadiationShield(Research):
    def __init__(self):
        super().__init__("Planetary Radiation Shield", Technology.PLANETARY_RADIATION_SHIELD, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPlanetaryRadiationShield()


#####################################################################################################
class ResearchWarpDissipater(Research):
    def __init__(self):
        super().__init__("Warp Dissipater", Technology.WARP_DISSIPATER, RESEARCH_POINTS, CATEGORY)
