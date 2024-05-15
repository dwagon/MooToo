""" Buildings"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MooToo.planet import Planet


#####################################################################################################
class PlanetBuilding:
    """Building"""

    def __init__(self, name):
        self.name = name
        self.maintenance = 0
        self.cost = 0

    def __str__(self):
        return self.name

    def food_bonus(self, planet: "Planet") -> int:
        return 0

    def prod_bonus(self, planet: "Planet") -> int:
        return 0

    def available_to_build(self, planet: "Planet") -> bool:
        if self.name in planet.buildings:
            return False
        return True
