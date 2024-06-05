from MooToo.planetbuilding import PlanetBuilding
from MooToo.planet import Planet
from MooToo.constants import Building


#####################################################################################################
class BuildingBiosphere(PlanetBuilding):

    def __init__(self):
        super().__init__("Biosphere", Building.BIOSPHERE)
        self.maintenance = 1
        self.cost = 60

    def max_pop_bonus(self, planet: Planet) -> int:
        return 2
