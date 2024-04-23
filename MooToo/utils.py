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


# EOF
