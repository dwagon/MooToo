from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingTerraforming1(PlanetBuilding):

    def __init__(self):
        super().__init__("Terraforming")
        self.maintenance = 0
        self.cost = 250


#####################################################################################################
class BuildingTerraforming2(PlanetBuilding):

    def __init__(self):
        super().__init__("Terraforming")
        self.maintenance = 0
        self.cost = 500


#####################################################################################################
class BuildingTerraforming3(PlanetBuilding):

    def __init__(self):
        super().__init__("Terraforming")
        self.maintenance = 0
        self.cost = 750
