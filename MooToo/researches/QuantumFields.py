from MooToo.research import Research, ResearchCategory
from MooToo.buildings.PlanetaryFluxShield import BuildingPlanetaryFluxShield
from MooToo.constants import Technology

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassVIIShield(Research):
    def __init__(self):
        super().__init__("Class VII Shield", Technology.CLASS_VII_SHIELD, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlanetaryFluxShield(Research):
    def __init__(self):
        super().__init__("Planetary Flux Shield", Technology.PLANETARY_FLUX_SHIELD, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPlanetaryFluxShield()


#####################################################################################################
class ResearchWideAreaJammer(Research):
    def __init__(self):
        super().__init__("Wide Area Jammer", Technology.WIDE_AREA_JAMMER, RESEARCH_POINTS, CATEGORY)
