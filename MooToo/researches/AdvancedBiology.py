from MooToo.research import Research, TechCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm
from MooToo.constants import Technology

RESEARCH_POINTS = 400
CATEGORY = TechCategory.BIOLOGY


#####################################################################################################
class ResearchCloningCenter(Research):
    def __init__(self):
        super().__init__("Cloning Center", Technology.CLONING_CENTER, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()


#####################################################################################################
class ResearchSoilEnrichment(Research):
    def __init__(self):
        super().__init__("Soil Enrichment", Technology.SOIL_ENRICHMENT, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()


#####################################################################################################
class ResearchDeathSpores(Research):
    def __init__(self):
        super().__init__("Death Spores", Technology.DEATH_SPORES, RESEARCH_POINTS, CATEGORY)
