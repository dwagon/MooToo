from MooToo.research import Research, ResearchCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm

RESEARCH_POINTS = 400
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchCloningCenter(Research):
    def __init__(self):
        super().__init__("Cloning Center", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()


#####################################################################################################
class ResearchSoilEnrichment(Research):
    def __init__(self):
        super().__init__("Soil Enrichment", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()


#####################################################################################################
class ResearchDeathSpores(Research):
    def __init__(self):
        super().__init__("Death Spores", RESEARCH_POINTS, CATEGORY)
