from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingPollutionProcessor(PlanetBuilding):

    def __init__(self):
        super().__init__("Pollution Processor")
        self.maintenance = 1
        self.cost = 80
