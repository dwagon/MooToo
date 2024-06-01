from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 900
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchNeutronBlaster(Research):
    def __init__(self):
        super().__init__("Neutron Blaster", Technology.NEUTRON_BLASTER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNeutronScanner(Research):
    def __init__(self):
        super().__init__("Neutron Scanner", Technology.NEUTRON_SCANNER, RESEARCH_POINTS, CATEGORY)
