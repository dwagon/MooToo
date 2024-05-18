from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingPlanetaryFluxShield(PlanetBuilding):

    def __init__(self):
        super().__init__("Planetary Flux Shield")
        self.maintenance = 3
        self.cost = 200
