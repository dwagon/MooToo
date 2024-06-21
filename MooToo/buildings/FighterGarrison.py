from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingFighterGarrison(PlanetBuilding):

    def __init__(self):
        super().__init__("Fighter Garrison", Building.FIGHTER_GARRISON)
        self.maintenance = 2
        self.cost = 250
