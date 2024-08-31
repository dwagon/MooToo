import unittest
from fastapi.testclient import TestClient

from MooToo.construct import ConstructType
from MooToo.server.main import app
from MooToo.ui.proxy.planet_proxy import PlanetProxy
from MooToo.server.server_utils import get_galaxy


#####################################################################################################
class PlanetUITest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.planet = PlanetProxy("planets/1", getter=self.client.get)

    #################################################################################################
    def test_can_build(self):
        self.assertFalse(self.planet.can_build(ConstructType.BUILDING))
        gal = next(get_galaxy())
        planet = gal.planets[1]
        print(planet)
        print(self.planet)
        self.assertEqual(self.planet.name, planet.name)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
