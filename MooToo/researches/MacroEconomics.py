from MooToo.research import Research, ResearchCategory
from MooToo.buildings.StockExchange import BuildingStockExchange
from MooToo.constants import Technology

RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchStockExchange(Research):
    def __init__(self):
        super().__init__("Stock Exchange", Technology.STOCK_EXCHANGE, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingStockExchange()
