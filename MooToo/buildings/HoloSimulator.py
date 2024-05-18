from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingHoloSimulator(PlanetBuilding):

    def __init__(self):
        super().__init__("Holo Simulator")
        self.maintenance = 1
        self.cost = 120
