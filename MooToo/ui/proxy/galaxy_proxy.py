""" Act as a copy of the galaxy class for UI purposes"""

from MooToo.ui.proxy.proxy_util import get, post
from MooToo.ui.proxy.system_proxy import SystemProxy
from MooToo.ui.proxy.planet_proxy import PlanetProxy
from MooToo.ui.proxy.empire_proxy import EmpireProxy
from MooToo.ui.proxy.ship_proxy import ShipProxy


#####################################################################################################
class GalaxyProxy:
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
            self.systems[system["id"]] = SystemProxy(system["url"])
        for planet in data["planets"]:
            self.planets[planet["id"]] = PlanetProxy(planet["url"])
        for empire in data["empires"]:
            self.empires[empire["id"]] = EmpireProxy(empire["url"])
        for ship in data["ships"]:
            self.ships[ship["id"]] = ShipProxy(ship["url"])

    #################################################################################################
    def turn(self):
        post("/galaxy/turn")
        self.init()
