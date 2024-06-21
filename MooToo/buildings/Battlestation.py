from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingBattlestation(PlanetBuilding):

    def __init__(self):
        super().__init__("Battlestation", Building.BATTLESTATION)
        self.maintenance = 3
        self.cost = 1000
