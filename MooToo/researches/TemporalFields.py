from MooToo.research import Research, TechCategory
from MooToo.buildings.PlanetaryBarrierShield import BuildingPlanetaryBarrierShield
from MooToo.constants import Technology

RESEARCH_POINTS = 15000
CATEGORY = TechCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassXShield(Research):
    def __init__(self):
        super().__init__("Class X Shield", Technology.CLASS_X_SHIELD, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlanetaryBarrierShield(Research):
    def __init__(self):
        super().__init__("Planetary Barrier Shield", Technology.PLANETARY_BARRIER_SHIELD, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPlanetaryBarrierShield()


#####################################################################################################
class ResearchPhasingCloak(Research):
    def __init__(self):
        super().__init__("Phasing Cloak", Technology.PHASING_CLOAK, RESEARCH_POINTS, CATEGORY)
