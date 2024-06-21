""" Buildings"""

from typing import TYPE_CHECKING
from MooToo.constants import Building

if TYPE_CHECKING:
    from MooToo.planet import Planet


#####################################################################################################
class PlanetBuilding:
    """A Building on a Planet"""

    def __init__(self, name: str, building_tag: Building):
        self.tag = building_tag
        self.name = name
        self.maintenance = 0
        self.cost = 0

    def __str__(self):
        return self.name

    def food_bonus(self, planet: "Planet") -> int:
        """Changes to absolute food production"""
        return 0

    def food_per_bonus(self, planet: "Planet") -> int:
        """Changes to per farmer productivity"""
        return 0

    def prod_bonus(self, planet: "Planet") -> int:
        return 0

    def prod_per_bonus(self, planet: "Planet") -> int:
        """Changes to per worker productivity"""
        return 0

    def research_bonus(self, planet: "Planet") -> int:
        return 0

    def research_per_bonus(self, planet: "Planet") -> int:
        """Changes to per scientist productivity"""
        return 0

    def morale_bonus(self, planet: "Planet") -> int:
        return 0

    def max_pop_bonus(self, planet: "Planet") -> int:
        return 0

    def available_to_build(self, planet: "Planet") -> bool:
        if self.tag in planet.buildings:
            return False
        return True
