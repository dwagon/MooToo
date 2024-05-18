from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingResearchLaboratory(PlanetBuilding):

    def __init__(self):
        super().__init__("Research Laboratory")
        self.maintenance = 1
        self.cost = 60
