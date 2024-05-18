from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingGroundBatteries(PlanetBuilding):

    def __init__(self):
        super().__init__("Ground Batteries")
        self.maintenance = 2
        self.cost = 200
