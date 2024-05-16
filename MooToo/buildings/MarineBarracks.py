from MooToo.planetbuilding import PlanetBuilding
from MooToo.planet import Planet


#####################################################################################################
class BuildingMarineBarracks(PlanetBuilding):

    def __init__(self):
        super().__init__("Marine Barracks")
        self.maintenance = 1
        self.cost = 60

    def morale_bonus(self, planet: Planet) -> int:
        return 1
