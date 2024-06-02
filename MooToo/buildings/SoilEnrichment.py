from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingSoilEnrichment(PlanetBuilding):

    def __init__(self):
        super().__init__("Soil Enrichment", Building.SOIL_ENRICHMENT)
        self.maintenance = 0
        self.cost = 120
