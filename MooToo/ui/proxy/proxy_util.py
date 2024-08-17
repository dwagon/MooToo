import math
import requests
from MooToo.ui.constants import URL


#################################################################################################
def get(url, params=None):
    full_url = f"{URL}/{url}"
    result = requests.get(full_url, params=params)
    result.raise_for_status()
    return result.json()["result"]


#################################################################################################
def post(url, data=None, params=None):
    full_url = f"{URL}/{url}"
    result = requests.post(full_url, data=data, params=params)
    result.raise_for_status()
    return result.json()["result"]


#####################################################################################################
def get_distance_tuple(a: tuple[float, float], b: tuple[float, float]) -> float:
    return get_distance(a[0], a[1], b[0], b[1])


#####################################################################################################
def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


#################################################################################################
def get_cache(obj, key, endpoint=""):
    if obj.dirty.get(key, True):
        full_url = f"{obj.url}/{endpoint}" if endpoint else obj.url
        data = get(full_url)
        obj.cache[key] = data
        obj.dirty[key] = False
    return obj.cache[key]


# EOF
