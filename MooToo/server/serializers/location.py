from typing import Any


#####################################################################################################
def location_serializer(location: tuple[int, int]) -> dict[str, Any]:
    result = {}
    if location:
        result["x"] = location[0]
        result["y"] = location[1]
    return result
