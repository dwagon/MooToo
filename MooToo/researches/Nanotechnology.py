from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchProtonTorpedo(Research):
    def __init__(self):
        super().__init__("Proton Torpedo", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHyperDrive(Research):
    def __init__(self):
        super().__init__("Hyper Drive", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHyperXCapacitors(Research):
    def __init__(self):
        super().__init__("Hyper-X Capacitors", RESEARCH_POINTS, CATEGORY)
