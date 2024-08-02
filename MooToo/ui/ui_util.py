import requests
from MooToo.ui.constants import URL


#################################################################################################
def get(url, params=None):
    full_url = f"{URL}/{url}"
    result = requests.get(full_url, params=params)
    result.raise_for_status()
    return result.json()["result"]


#################################################################################################
def post(url, data=None):
    full_url = f"{URL}/{url}"
    result = requests.post(full_url, data)
    result.raise_for_status()
    return result.json()["result"]


#####################################################################################################
def get_distance_tuple(a: tuple[float, float], b: tuple[float, float]) -> float:
    return get_distance(a[0], a[1], b[0], b[1])


#####################################################################################################
def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    result = get("galaxy/get_distance", params={"x1": x1, "y1": y1, "x2": x2, "y2": y2})
    return float(result["distance"])


# EOF
