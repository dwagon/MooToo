from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchNanoDissasemblers(Research):
    def __init__(self):
        super().__init__("Nano Disassemblers", Technology.NANO_DISASSEMBLERS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchicroliteConstruction(Research):
    def __init__(self):
        super().__init__("Microlite Construction", Technology.MICROLITE_CONSTRUCTION, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchZortriumArmor(Research):
    def __init__(self):
        super().__init__("Zortrium Armor", Technology.ZORTRIUM_ARMOR, RESEARCH_POINTS, CATEGORY)
