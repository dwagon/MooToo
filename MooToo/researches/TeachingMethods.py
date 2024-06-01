from MooToo.research import Research, ResearchCategory
from MooToo.buildings.AstroUniversity import BuildingAstroUniversity
from MooToo.constants import Technology

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchAstroUniversity(Research):
    def __init__(self):
        super().__init__("Astro University", Technology.ASTRO_UNIVERSITY, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAstroUniversity()
