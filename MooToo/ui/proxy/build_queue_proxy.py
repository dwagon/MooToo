""" Act as a copy of the planet class for UI purposes"""

from typing import Any

import requests
from enum import StrEnum, auto

from MooToo.construct import ConstructType, Construct
from MooToo.ui.proxy.proxy_util import Proxy


#####################################################################################################
class CacheKeys(StrEnum):
    QUEUE = auto()
    LENGTH = auto()


#####################################################################################################
class BuildQueueProxy(Proxy):
    def __init__(self, url: str, getter=requests.get, poster=requests.post):
        super().__init__(url, getter, poster)
        self.galaxy = None

    #############################################################################################
    def toggle(self, construct: Construct) -> None:
        print(f"DBG {construct=}")
        url_extension = ""
        match construct.category:
            case ConstructType.BUILDING:
                url_extension = f"building?building_tag={construct.building_tag}"
            case ConstructType.SPY:
                url_extension = "spy"
            case ConstructType.SHIP:
                url_extension = f"ship?design_id={construct.design_id}"
            case ConstructType.FREIGHTER:
                url_extension = "freighter"
            case ConstructType.COLONY_BASE:
                url_extension = "colony_base"
            case ConstructType.TRANSPORT:
                url_extension = "transport"
            case ConstructType.COLONY_SHIP:
                url_extension = "colony_ship"
            case _:
                print(f"BuildQueueProxy.toggle({construct=}) unknown construct")
        self.post(f"{self.url}/toggle/{url_extension}")
        self.reset_cache()

    #############################################################################################
    def __bool__(self):
        return len(self) != 0

    #############################################################################################
    def __len__(self):
        return self.get_cache(CacheKeys.LENGTH, "length")["length"]

    #############################################################################################
    def __getitem__(self, item):
        try:
            ans = self.get_cache(CacheKeys.QUEUE, f"{item}")
        except requests.exceptions.HTTPError as exc:
            raise IndexError from exc
        print(f"DBG {ans=}")
        return make_construct(ans["item"])


def make_construct(in_con: dict[str, Any]) -> Construct:
    match dict["category"]:
        case "spy":
            return Construct(ConstructType.SPY)
        case "freighter":
            return Construct(ConstructType.FREIGHTER)
        case _:
            print(f"make_construct: Unhandled construct {in_con}")


# EOF
