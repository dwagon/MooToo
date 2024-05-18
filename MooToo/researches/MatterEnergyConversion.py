from MooToo.research import Research, ResearchCategory
from MooToo.buildings.FoodReplicators import BuildingFoodReplicators

RESEARCH_POINTS = 2750
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchTransporters(Research):
    def __init__(self):
        super().__init__("Transporters", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchFoodReplicators(Research):
    def __init__(self):
        super().__init__("Food Replicators", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingFoodReplicators()
