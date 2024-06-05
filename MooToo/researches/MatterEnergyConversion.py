from MooToo.research import Research, ResearchCategory
from MooToo.buildings.FoodReplicators import BuildingFoodReplicators
from MooToo.constants import Technology

RESEARCH_POINTS = 2750
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchTransporters(Research):
    def __init__(self):
        super().__init__("Transporters", Technology.TRANSPORTERS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchFoodReplicators(Research):
    def __init__(self):
        super().__init__("Food Replicators", Technology.FOOD_REPLICATORS, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingFoodReplicators()
