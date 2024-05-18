from MooToo.research import Research, ResearchCategory
from MooToo.buildings.StockExchange import BuildingStockExchange

RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchStockExchange(Research):
    def __init__(self):
        super().__init__("Stock Exchange", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingStockExchange()
