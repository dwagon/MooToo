from MooToo.research import Research, ResearchCategory
from MooToo.buildings.PleasureDome import BuildingPleasureDome

RESEARCH_POINTS = 6000
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchPleasureDome(Research):
    def __init__(self):
        super().__init__("Pleasure Dome", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPleasureDome()


#####################################################################################################
class ResearchMoleculartronicComputer(Research):
    def __init__(self):
        super().__init__("Moleculartronic Computer", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAchillesTargetingUnit(Research):
    def __init__(self):
        super().__init__("Achilles Targeting Unit", RESEARCH_POINTS, CATEGORY)
