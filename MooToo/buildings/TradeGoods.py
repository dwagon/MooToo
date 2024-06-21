from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingTradeGoods(PlanetBuilding):

    def __init__(self):
        super().__init__("Trade Goods", Building.TRADE_GOODS)
        self.maintenance = 0
        self.cost = 999999999
