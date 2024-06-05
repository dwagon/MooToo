from MooToo.research import Research, ResearchCategory
from MooToo.buildings.PleasureDome import BuildingPleasureDome
from MooToo.constants import Technology

RESEARCH_POINTS = 6000
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchPleasureDome(Research):
    def __init__(self):
        super().__init__("Pleasure Dome", Technology.PLEASURE_DOME, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingPleasureDome()


#####################################################################################################
class ResearchMoleculartronicComputer(Research):
    def __init__(self):
        super().__init__("Moleculartronic Computer", Technology.MOLECULARTRONIC_COMPUTER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAchillesTargetingUnit(Research):
    def __init__(self):
        super().__init__("Achilles Targeting Unit", Technology.ACHILLES_TARGETING_UNIT, RESEARCH_POINTS, CATEGORY)
