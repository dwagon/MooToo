from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingPlanetaryRadiationShield(PlanetBuilding):

    def __init__(self):
        super().__init__("Planetary Radiation Shield")
        self.maintenance = 1
        self.cost = 80
