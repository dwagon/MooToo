from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingArmourBarracks(PlanetBuilding):

    def __init__(self):
        super().__init__("Armour Barracks", Building.ARMOUR_BARRACKS)
        self.maintenance = 2
        self.cost = 150
