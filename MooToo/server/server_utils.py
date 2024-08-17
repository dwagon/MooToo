from MooToo.bigbang import create_galaxy


URL_PREFIX_SHIPS = "/ships"
URL_PREFIX_SYSTEMS = "/systems"
URL_PREFIX_PLANETS = "/planets"
URL_PREFIX_EMPIRES = "/empires"
URL_PREFIX_GALAXY = "/galaxy"

GALAXY = None


#####################################################################################################
def get_galaxy():
    global GALAXY
    if not GALAXY:
        print("Creating galaxy")
        GALAXY = create_galaxy()
    yield GALAXY


# EOF
