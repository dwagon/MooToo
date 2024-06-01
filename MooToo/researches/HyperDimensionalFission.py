from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchProtonTorpedo(Research):
    def __init__(self):
        super().__init__("Proton Torpedo", Technology.PROTON_TORPEDO, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHyperDrive(Research):
    def __init__(self):
        super().__init__("Hyper Drive", Technology.HYPER_DRIVE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHyperXCapacitors(Research):
    def __init__(self):
        super().__init__("Hyper-X Capacitors", Technology.HYPER_X_CAPACITORS, RESEARCH_POINTS, CATEGORY)
