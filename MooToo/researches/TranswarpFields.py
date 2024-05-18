from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 7500
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchDisplacementDevice(Research):
    def __init__(self):
        super().__init__("Displacement Device", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSubspaceTeleporter(Research):
    def __init__(self):
        super().__init__("Subspace Teleporter", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchInertialNullifier(Research):
    def __init__(self):
        super().__init__("Inertial Nullifier", RESEARCH_POINTS, CATEGORY)
