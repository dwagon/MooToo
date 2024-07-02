import argparse
import math
import random
import glob
import importlib
import os

from MooToo.constants import Building, Technology
from MooToo.planet_building import PlanetBuilding
from MooToo.research import Research

_BUILDINGS: dict["Building", "PlanetBuilding"] = {}
_RESEARCHES: dict["Technology", "Research"] = {}


#################################################################################################
def prob_map(d):
    """Given a dictionary of choice probabilities {'a': 10, 'b': 20, ...}
    return a random choice based on the probability"""
    tot_prob = sum(d.values())
    r = random.randrange(tot_prob)
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
    global _RESEARCHES
    if not _RESEARCHES:
        _RESEARCHES = load_researches()
    return _RESEARCHES[tech]


#####################################################################################################
def all_research() -> dict["Technology", "Research"]:
    global _RESEARCHES
    if not _RESEARCHES:
        _RESEARCHES = load_researches()
    return _RESEARCHES


#####################################################################################################
def get_building(building: "Building") -> "PlanetBuilding":
    global _BUILDINGS
    if not _BUILDINGS:
        _BUILDINGS = load_buildings()
    return _BUILDINGS[building]


#####################################################################################################
def get_distance_tuple(a: tuple[float, float], b: tuple[float, float]) -> float:
    return get_distance(a[0], a[1], b[0], b[1])


#####################################################################################################
def load_buildings() -> dict["Building", "PlanetBuilding"]:
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


#####################################################################################################
def arg_parse(sys_args) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tech", choices=["pre", "avg", "adv"], default="avg")
    parser.add_argument("--load", type=argparse.FileType(mode="r"))
    return parser.parse_args(sys_args)


# EOF
