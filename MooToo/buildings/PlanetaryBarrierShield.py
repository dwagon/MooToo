from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingPlanetaryBarrierShield(PlanetBuilding):

    def __init__(self):
        super().__init__("Planetary Barrier Shield")
        self.maintenance = 5
        self.cost = 500
