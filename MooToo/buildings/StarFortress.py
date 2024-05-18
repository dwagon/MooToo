from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingStarFortress(PlanetBuilding):

    def __init__(self):
        super().__init__("Star Fortress")
        self.maintenance = 4
        self.cost = 2500
