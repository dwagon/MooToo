from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 250
CATEGORY = TechCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassIShield(Research):
    def __init__(self):
        super().__init__("Class I Shield", Technology.CLASS_I_SHIELD, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMassDriver(Research):
    def __init__(self):
        super().__init__("Mass Driver", Technology.MASS_DRIVER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchECMJammer(Research):
    def __init__(self):
        super().__init__("ECM Jammer", Technology.ECM_JAMMER, RESEARCH_POINTS, CATEGORY)
