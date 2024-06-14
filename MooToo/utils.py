import math
import random
import glob
import importlib
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MooToo import Research, PlanetBuilding, Building, Technology


#################################################################################################
def prob_map(d):
    """Given a dictionary of choice probabilities {'a': 10, 'b': 20, ...}
    return a random choice based on the probability"""
    totprob = sum(d.values())
    r = random.randrange(totprob)
    for k, v in d.items():
        if r < v:
            return k
        r -= v
    return None


#####################################################################################################
def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


#####################################################################################################
def get_research(tech: "Technology") -> "Research":
    pass
    # TODO


#####################################################################################################
def get_building(building: "Building") -> "PlanetBuilding":
    from MooToo import _buildings

    return _buildings[building]


#####################################################################################################
def get_distance_tuple(a: tuple[float, float], b: tuple[float, float]) -> float:
    return get_distance(a[0], a[1], b[0], b[1])


#####################################################################################################
def load_buildings() -> dict["Building", "PlanetBuilding"]:
    print("Loading buildings")
    path = "MooToo/buildings"
    mapping: dict["Building", "PlanetBuilding"] = {}
    files = glob.glob(f"{path}/*.py")
    for file_name in [os.path.basename(_) for _ in files]:
        file_name = file_name.replace(".py", "")
        mod = importlib.import_module(f"{path.replace('/', '.')}.{file_name}")
        classes = dir(mod)
        for kls in classes:
            if kls.startswith("Building") and kls != "Building":
                klass = getattr(mod, kls)
                mapping[klass().tag] = klass()
                break
    return mapping


#####################################################################################################
def load_researches() -> dict["Technology", "Research"]:
    path = "MooToo/researches"
    mapping: dict["Technology", "Research"] = {}
    files = glob.glob(f"{path}/*.py")
    for file_name in [os.path.basename(_) for _ in files]:
        file_name = file_name.replace(".py", "")
        mod = importlib.import_module(f"{path.replace('/', '.')}.{file_name}")
        classes = dir(mod)
        for kls in classes:
            if kls.startswith("Research") and kls != "Research":
                klass = getattr(mod, kls)
                mapping[klass().tag] = klass()
    return mapping


# EOF
