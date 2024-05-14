from MooToo.planetbuilding import PlanetBuilding
from MooToo.planet import Planet


#####################################################################################################
class BuildingAutomatedFactory(PlanetBuilding):
    """Automated factories aid workers, increasing the output of each industrial unit of population by
    +1 production each turn and giving the colony +5 production."""

    def __init__(self):
        super().__init__("Automated Factory")
        self.maintenance = 2
        self.cost = 60

    def prod_bonus(self, planet: Planet) -> int:
        return planet.current_population() + 5
