from MooToo.ui.planet_building import PlanetBuilding
from MooToo.planet import Planet
from MooToo.constants import Building


#####################################################################################################
class BuildingMarineBarracks(PlanetBuilding):

    def __init__(self):
        super().__init__("Marine Barracks", Building.MARINE_BARRACKS)
        self.maintenance = 1
        self.cost = 60

    def morale_bonus(self, planet: Planet) -> int:
        return 1
