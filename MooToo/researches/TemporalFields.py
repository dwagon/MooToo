from MooToo.research import Research, ResearchCategory
from MooToo.buildings.PlanetaryBarrierShield import BuildingPlanetaryBarrierShield

RESEARCH_POINTS = 15000
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassXShield(Research):
    def __init__(self):
        super().__init__("Class X Shield", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlanetaryBarrierShield(Research):
    def __init__(self):
        super().__init__("Planetary Barrier Shield", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPlanetaryBarrierShield()


#####################################################################################################
class ResearchPhasingCloak(Research):
    def __init__(self):
        super().__init__("Phasing Cloak", RESEARCH_POINTS, CATEGORY)
