from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 6000
CATEGORY = TechCategory.SOCIOLOGY


#####################################################################################################
class ResearchGalacticCurrencyExchange(Research):
    def __init__(self):
        super().__init__("Galactic Currency Exchange", Technology.GALACTIC_CURRENCY_EXCHANGE, RESEARCH_POINTS, CATEGORY)
