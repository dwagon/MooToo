from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
#####################################################################################################
class Research:
    def __init__(self, name: str, cost: int):
        self.name: str = name
        self.cost: int = cost
        self.enabled_building: PlanetBuilding | None = None
