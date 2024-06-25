from MooToo.research import Research, TechCategory
from MooToo.constants import Technology
from MooToo.buildings.AtmosphericRenewer import BuildingAtmosphericRenewer

RESEARCH_POINTS = 1150
CATEGORY = TechCategory.CHEMISTRY


#####################################################################################################
class ResearchPulsonMissile(Research):
    def __init__(self):
        super().__init__("Pulson Missile", Technology.PULSON_MISSILE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAtmosphericRenewer(Research):
    def __init__(self):
        super().__init__("Atmospheric Renewer", Technology.ATMOSPHERIC_RENEWER, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAtmosphericRenewer()


#####################################################################################################
class ResearchIridiumFuelCells(Research):
    def __init__(self):
        super().__init__("Iridium Fuel cells", Technology.IRIDIUM_FUEL_CELLS, RESEARCH_POINTS, CATEGORY)
