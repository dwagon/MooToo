from MooToo.ui.planet_building import PlanetBuilding
from MooToo.planet import Planet
from MooToo.constants import Building


#####################################################################################################
class BuildingHydroponicFarm(PlanetBuilding):
    """The Hydroponic Farm is an automated, sealed environment in which food is grown,
    even on otherwise lifeless worlds. The Farm increases the food output of a colony by 2."""

    def __init__(self):
        super().__init__("Hydroponic Farm", Building.HYDROPONIC_FARM)
        self.maintenance = 2
        self.cost = 60

    def food_bonus(self, planet: Planet) -> int:
        return 2
