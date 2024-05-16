from MooToo.research import Research, ResearchCategory
from MooToo.buildings.AutomatedFactory import BuildingAutomatedFactory

RESEARCH_POINTS = 150
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchAutomatedFactory(Research):
    def __init__(self):
        super().__init__("Automated Factory", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAutomatedFactory()


#####################################################################################################
class ResearchMissileBase(Research):
    def __init__(self):
        super().__init__("Missile Base", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHeavyArmour(Research):
    def __init__(self):
        super().__init__("Heavy Armour", RESEARCH_POINTS, CATEGORY)
