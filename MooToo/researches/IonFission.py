from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 900
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchIonDrive(Research):
    def __init__(self):
        super().__init__("Ion Drive", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchIonPulseCannon(Research):
    def __init__(self):
        super().__init__("Ion Pulse Cannon", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchShieldCapacitor(Research):
    def __init__(self):
        super().__init__("Shield Capacitor", RESEARCH_POINTS, CATEGORY)
