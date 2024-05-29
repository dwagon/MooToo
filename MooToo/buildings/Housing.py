from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingHousing(PlanetBuilding):

    def __init__(self):
        super().__init__("Housing")
        self.maintenance = 0
        self.cost = 99999999
