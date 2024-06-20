from MooToo.research import Research, TechCategory
from MooToo.buildings.StockExchange import BuildingStockExchange
from MooToo.constants import Technology

RESEARCH_POINTS = 1150
CATEGORY = TechCategory.SOCIOLOGY


#####################################################################################################
class ResearchStockExchange(Research):
    def __init__(self):
        super().__init__("Stock Exchange", Technology.STOCK_EXCHANGE, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingStockExchange()
