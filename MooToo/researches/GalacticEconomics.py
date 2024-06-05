from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 6000
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchGalacticCurrencyExchange(Research):
    def __init__(self):
        super().__init__("Galactic Currency Exchange", Technology.GALACTIC_CURRENCY_EXCHANGE, RESEARCH_POINTS, CATEGORY)
