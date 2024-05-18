from MooToo.planetbuilding import PlanetBuilding
from MooToo.planet import Planet


#####################################################################################################
class BuildingRoboMiners(PlanetBuilding):

    def __init__(self):
        super().__init__("Robo-Miners")
        self.maintenance = 2
        self.cost = 150
