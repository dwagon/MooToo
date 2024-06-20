from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 900
CATEGORY = TechCategory.POWER


#####################################################################################################
class ResearchIonDrive(Research):
    def __init__(self):
        super().__init__("Ion Drive", Technology.ION_DRIVE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchIonPulseCannon(Research):
    def __init__(self):
        super().__init__("Ion Pulse Cannon", Technology.ION_PULSE_CANNON, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchShieldCapacitor(Research):
    def __init__(self):
        super().__init__("Shield Capacitor", Technology.SHIELD_CAPACITOR, RESEARCH_POINTS, CATEGORY)
