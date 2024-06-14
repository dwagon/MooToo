from MooToo.research import Research, TechCategory
from MooToo.buildings.AstroUniversity import BuildingAstroUniversity
from MooToo.constants import Technology

RESEARCH_POINTS = 2000
CATEGORY = TechCategory.SOCIOLOGY


#####################################################################################################
class ResearchAstroUniversity(Research):
    def __init__(self):
        super().__init__("Astro University", Technology.ASTRO_UNIVERSITY, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAstroUniversity()
