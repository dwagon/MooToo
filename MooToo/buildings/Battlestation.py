from MooToo.planetbuilding import PlanetBuilding
from MooToo.planet import Planet


#####################################################################################################
class BuildingBattlestation(PlanetBuilding):

    def __init__(self):
        super().__init__("Battlestation")
        self.maintenance = 3
        self.cost = 1000
