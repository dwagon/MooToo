from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 900
CATEGORY = TechCategory.PHYSICS


#####################################################################################################
class ResearchNeutronBlaster(Research):
    def __init__(self):
        super().__init__("Neutron Blaster", Technology.NEUTRON_BLASTER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNeutronScanner(Research):
    def __init__(self):
        super().__init__("Neutron Scanner", Technology.NEUTRON_SCANNER, RESEARCH_POINTS, CATEGORY)
