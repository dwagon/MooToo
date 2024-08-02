""" Act as a copy of the galaxy class for UI purposes"""

from .ui_util import get, post
from .systemui import SystemUI
from .planetui import PlanetUI
from .empireui import EmpireUI
from .shipui import ShipUI


#####################################################################################################
class GalaxyUI:
    def __init__(self):
        self.empires = {}
        self.planets = {}
        self.systems = {}
        self.ships = {}
        self.turn_number = 0
        self.init()

    #################################################################################################
    def init(self):
        data = get("/galaxy")["galaxy"]
        self.turn_number = data["turn_number"]
        for system in data["systems"]:
            self.systems[system["id"]] = SystemUI(system["url"])
        for planet in data["planets"]:
            self.planets[planet["id"]] = PlanetUI(planet["url"])
        for empire in data["empires"]:
            self.empires[empire["id"]] = EmpireUI(empire["url"])
        for ship in data["ships"]:
            self.ships[ship["id"]] = ShipUI(ship["url"])

    #################################################################################################
    def turn(self):
        post("/galaxy/turn")
