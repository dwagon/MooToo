from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 3500
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchHighEnergyFocus(Research):
    def __init__(self):
        super().__init__("High Energy Focus", Technology.HIGH_ENERGY_FOCUS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchEnergyAbsorber(Research):
    def __init__(self):
        super().__init__("Energy Absorber", Technology.ENERGY_ABSORBER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMegafluxers(Research):
    def __init__(self):
        super().__init__("Megafluxers", Technology.MEGAFLUXERS, RESEARCH_POINTS, CATEGORY)
