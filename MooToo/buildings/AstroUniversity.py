from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingAstroUniversity(PlanetBuilding):

    def __init__(self):
        super().__init__("Astro University")
        self.maintenance = 4
        self.cost = 200
