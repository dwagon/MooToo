from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingArtemisSystemNet(PlanetBuilding):

    def __init__(self):
        super().__init__("Artemis System Net")
        self.maintenance = 5
        self.cost = 1000
