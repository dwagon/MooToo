from MooToo.planetbuilding import PlanetBuilding
from MooToo.planet import Planet


#####################################################################################################
class BuildingFighterGarrison(PlanetBuilding):

    def __init__(self):
        super().__init__("Fighter Garrison")
        self.maintenance = 2
        self.cost = 250
