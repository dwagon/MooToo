import unittest
from fastapi.testclient import TestClient
from MooToo.server.main import app
from MooToo.bigbang import create_galaxy


#####################################################################################################
class GalaxyTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.galaxy = create_galaxy()

    #################################################################################################
    def test_get_research(self):
        response = self.client.get("/galaxy/research/battleoids")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["result"]["research"]["name"], "Battleoids")
        self.assertEqual(data["result"]["research"]["cost"], 1150)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
