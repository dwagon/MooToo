from MooToo.planetbuilding import PlanetBuilding
from MooToo.planet import Planet


#####################################################################################################
class BuildingArmourBarracks(PlanetBuilding):

    def __init__(self):
        super().__init__("Armour Barracks")
        self.maintenance = 2
        self.cost = 150
