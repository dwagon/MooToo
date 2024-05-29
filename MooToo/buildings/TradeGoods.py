from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingTradeGoods(PlanetBuilding):

    def __init__(self):
        super().__init__("Trade Goods")
        self.maintenance = 0
        self.cost = 999999999
