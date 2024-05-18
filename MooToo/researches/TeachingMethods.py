from MooToo.research import Research, ResearchCategory
from MooToo.buildings.AstroUniversity import BuildingAstroUniversity

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchAstroUniversity(Research):
    def __init__(self):
        super().__init__("Astro University", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAstroUniversity()
