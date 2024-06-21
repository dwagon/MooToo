from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingStockExchange(PlanetBuilding):

    def __init__(self):
        super().__init__("Stock Exchange", Building.STOCK_EXCHANGE)
        self.maintenance = 2
        self.cost = 150
