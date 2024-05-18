from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 900
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchNeutronBlaster(Research):
    def __init__(self):
        super().__init__("Neutron Blaster", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNeutronScanner(Research):
    def __init__(self):
        super().__init__("Neutron Scanner", RESEARCH_POINTS, CATEGORY)
