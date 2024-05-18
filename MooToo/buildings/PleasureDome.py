from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingPleasureDome(PlanetBuilding):

    def __init__(self):
        super().__init__("Pleasure Dome")
        self.maintenance = 3
        self.cost = 250
