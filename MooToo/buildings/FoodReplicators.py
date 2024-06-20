from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingFoodReplicators(PlanetBuilding):

    def __init__(self):
        super().__init__("Food Replicators", Building.FOOD_REPLICATORS)
        self.maintenance = 10
        self.cost = 200
