from MooToo.research import Research, ResearchCategory
from MooToo.buildings.Supercomputer import BuildingSupercomputer
from MooToo.buildings.HoloSimulator import BuildingHoloSimulator
from MooToo.constants import Technology

RESEARCH_POINTS = 900
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchPositronicComputer(Research):
    def __init__(self):
        super().__init__("Positronic Computer", Technology.POSITRONIC_COMPUTER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSupercomputer(Research):
    def __init__(self):
        super().__init__("Supercomputer", Technology.SUPERCOMPUTER, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingSupercomputer()


#####################################################################################################
class ResearchHoloSimulator(Research):
    def __init__(self):
        super().__init__("Holo Simulator", Technology.HOLO_SIMULATOR, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHoloSimulator()
