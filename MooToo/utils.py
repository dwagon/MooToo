import math
import random


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
    else:
        return None


#####################################################################################################
def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def get_distance_tuple(a: tuple[float, float], b: tuple[float, float]) -> float:
    return get_distance(a[0], a[1], b[0], b[1])


# EOF
