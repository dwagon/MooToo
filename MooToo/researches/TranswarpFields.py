from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 7500
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchDisplacementDevice(Research):
    def __init__(self):
        super().__init__("Displacement Device", Technology.DISPLACEMENT_DEVICE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSubspaceTeleporter(Research):
    def __init__(self):
        super().__init__("Subspace Teleporter", Technology.SUBSPACE_TELEPORTER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchInertialNullifier(Research):
    def __init__(self):
        super().__init__("Inertial Nullifier", Technology.INTERTIAL_NULLIFIER, RESEARCH_POINTS, CATEGORY)
