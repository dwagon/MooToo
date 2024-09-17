""" Act as a copy of the galaxy class for UI purposes"""

import requests

from MooToo.constants import Technology
from MooToo.ui.proxy.proxy_util import Proxy
from MooToo.ui.proxy.system_proxy import SystemProxy
from MooToo.ui.proxy.planet_proxy import PlanetProxy
from MooToo.ui.proxy.empire_proxy import EmpireProxy
from MooToo.ui.proxy.ship_proxy import ShipProxy
from MooToo.ui.proxy.research_proxy import ResearchProxy
from MooToo.ui.proxy.design_proxy import ShipDesignProxy


#####################################################################################################
class GalaxyProxy(Proxy):
    def __init__(self, getter=requests.get, poster=requests.post):
        self.url = "/galaxy"
        super().__init__(self.url, getter, poster)
        self.empires = {}
        self.planets = {}
        self.systems = {}
        self.ships = {}
        self.designs = {}
        self.turn_number = 0
        self.init()
        self.research_cache: dict[Technology:ResearchProxy] = {}

    #################################################################################################
    def init(self):
        self.reset_cache()
        data = self.get("/galaxy")["galaxy"]
        self.turn_number = data["turn_number"]
        for system in data["systems"]:
            self.systems[system["id"]] = SystemProxy(system["url"])
        for planet in data["planets"]:
            self.planets[planet["id"]] = PlanetProxy(planet["url"])
        for empire in data["empires"]:
            self.empires[empire["id"]] = EmpireProxy(empire["url"])
        for ship in data["ships"]:
            self.ships[ship["id"]] = ShipProxy(ship["url"], self)
        for design in data["designs"]:
            self.designs[design["id"]] = ShipDesignProxy(design["url"])

    #################################################################################################
    def turn(self):
        self.post("/galaxy/turn")
        self.init()

    #################################################################################################
    def get_research(self, tech: "Technology") -> "ResearchProxy":
        if tech not in self.research_cache:
            self.research_cache[tech] = ResearchProxy(f"/galaxy/research/{tech}")
        return self.research_cache[tech]
