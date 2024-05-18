from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchPulsonMissile(Research):
    def __init__(self):
        super().__init__("Pulson Missile", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAtmosphericRenewer(Research):
    def __init__(self):
        super().__init__("Atmospheric Renewer", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchIridiumFuelCells(Research):
    def __init__(self):
        super().__init__("Iridium Fuel cells", RESEARCH_POINTS, CATEGORY)
