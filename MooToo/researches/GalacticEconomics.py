from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 6000
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchGalacticCurrencyExchange(Research):
    def __init__(self):
        super().__init__("Galactic Currency Exchange", RESEARCH_POINTS, CATEGORY)
