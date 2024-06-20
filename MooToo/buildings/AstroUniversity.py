from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingAstroUniversity(PlanetBuilding):

    def __init__(self):
        super().__init__("Astro University", Building.ASTRO_UNIVERSITY)
        self.maintenance = 4
        self.cost = 200
