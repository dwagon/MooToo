import math
from typing import Any

import requests
from MooToo.ui.constants import URL


#################################################################################################
class Proxy:
    def __init__(self, url: str, getter=requests.get, poster=requests.post):
        self.url = url
        self.getter = getter
        self.poster = poster
        self.cache: dict["CacheKeys", Any] = {}
        self.dirty: dict["CacheKeys", bool] = {}

    #################################################################################################
    def reset_cache(self):
        self.cache = {}
        self.dirty = {}

    #################################################################################################
    def get(self, url, params=None):
        full_url = f"{URL}/{url}"
        result = self.getter(full_url, params=params)
        result.raise_for_status()
        return result.json()["result"]

    #################################################################################################
    def post(self, url, data=None, params=None) -> dict[str, Any]:
        full_url = f"{URL}/{url}"
        result = self.poster(full_url, data=data, params=params)
        result.raise_for_status()
        return result.json()["result"]

    #################################################################################################
    def get_cache(self, key, endpoint=""):
        if self.dirty.get(key, True):
            full_url = f"{self.url}/{endpoint}" if endpoint else self.url
            data = self.get(full_url)
            self.cache[key] = data
            self.dirty[key] = False
        return self.cache[key]


#####################################################################################################
def get_distance_tuple(a: tuple[float, float], b: tuple[float, float]) -> float:
    return get_distance(a[0], a[1], b[0], b[1])


#####################################################################################################
def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# EOF
