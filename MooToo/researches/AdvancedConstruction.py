from MooToo.research import Research, TechCategory
from MooToo.buildings.AutomatedFactory import BuildingAutomatedFactory
from MooToo.constants import Technology

RESEARCH_POINTS = 150
CATEGORY = TechCategory.CONSTRUCTION


#####################################################################################################
class ResearchAutomatedFactory(Research):
    def __init__(self):
        super().__init__("Automated Factory", Technology.AUTOMATED_FACTORY, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAutomatedFactory()


#####################################################################################################
class ResearchMissileBase(Research):
    def __init__(self):
        super().__init__("Missile Base", Technology.MISSILE_BASE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHeavyArmour(Research):
    def __init__(self):
        super().__init__("Heavy Armour", Technology.HEAVY_ARMOUR, RESEARCH_POINTS, CATEGORY)
