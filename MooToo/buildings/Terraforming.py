from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingTerraforming1(PlanetBuilding):

    def __init__(self):
        super().__init__("Terraforming", Building.TERRAFORMING_1)
        self.maintenance = 0
        self.cost = 250


#####################################################################################################
class BuildingTerraforming2(PlanetBuilding):

    def __init__(self):
        super().__init__("Terraforming", Building.TERRAFORMING_2)
        self.maintenance = 0
        self.cost = 500


#####################################################################################################
class BuildingTerraforming3(PlanetBuilding):

    def __init__(self):
        super().__init__("Terraforming", Building.TERRAFORMING_3)
        self.maintenance = 0
        self.cost = 750
