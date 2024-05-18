from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingGalacticCybernet(PlanetBuilding):

    def __init__(self):
        super().__init__("Galactic Cybernet")
        self.maintenance = 3
        self.cost = 250
