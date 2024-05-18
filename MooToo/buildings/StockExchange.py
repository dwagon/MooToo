from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingStockExchange(PlanetBuilding):

    def __init__(self):
        super().__init__("Stock Exchange")
        self.maintenance = 2
        self.cost = 150
