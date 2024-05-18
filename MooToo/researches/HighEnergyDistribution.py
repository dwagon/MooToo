from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 3500
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchHighEnergyFocus(Research):
    def __init__(self):
        super().__init__("High Energy Focus", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchEnergyAbsorber(Research):
    def __init__(self):
        super().__init__("Energy Absorber", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMegafluxers(Research):
    def __init__(self):
        super().__init__("Megafluxers", RESEARCH_POINTS, CATEGORY)
