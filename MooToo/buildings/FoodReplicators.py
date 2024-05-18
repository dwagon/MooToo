from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingFoodReplicators(PlanetBuilding):

    def __init__(self):
        super().__init__("Food Replicators")
        self.maintenance = 10
        self.cost = 200
