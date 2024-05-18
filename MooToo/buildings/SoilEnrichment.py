from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingSoilEnrichment(PlanetBuilding):

    def __init__(self):
        super().__init__("Soil Enrichment")
        self.maintenance = 0
        self.cost = 120
