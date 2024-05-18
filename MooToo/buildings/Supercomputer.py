from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingSupercomputer(PlanetBuilding):

    def __init__(self):
        super().__init__("Supercomputer")
        self.maintenance = 2
        self.cost = 150
