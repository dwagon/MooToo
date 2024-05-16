from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 250
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassIShield(Research):
    def __init__(self):
        super().__init__("Class I Shield", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMassDriver(Research):
    def __init__(self):
        super().__init__("Mass Driver", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchECMJammer(Research):
    def __init__(self):
        super().__init__("ECM Jammer", RESEARCH_POINTS, CATEGORY)
