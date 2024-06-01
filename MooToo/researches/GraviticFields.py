from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 650
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchAntiGravHarness(Research):
    def __init__(self):
        super().__init__("Anti-Grav Harness", Technology.ANTI_GRAV_HARNESS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGyroStabilizer(Research):
    def __init__(self):
        super().__init__("Gyro Stabilizer", Technology.GYRO_STABILIZER, RESEARCH_POINTS, CATEGORY)
