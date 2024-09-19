import unittest
from fastapi.testclient import TestClient

from MooToo.server.main import app
from MooToo.ui.proxy.planet_proxy import PlanetProxy


#####################################################################################################
class PlanetUITest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.planet = PlanetProxy("planets/1", getter=self.client.get)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
