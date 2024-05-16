from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 650
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchAntiGravHarness(Research):
    def __init__(self):
        super().__init__("Anti-Grav Harness", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGyroStabilizer(Research):
    def __init__(self):
        super().__init__("Gyro Stabilizer", RESEARCH_POINTS, CATEGORY)
