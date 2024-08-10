import unittest
from fastapi.testclient import TestClient
from MooToo.server.main import app
from MooToo.bigbang import create_galaxy


#####################################################################################################
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.galaxy = create_galaxy()

    #################################################################################################
    def test_ship_list(self):
        response = self.client.get("/ships")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["result"]["ships"][0], {"id": 0, "url": "/ships/0"})

    #################################################################################################
    def test_ship_get(self):
        response = self.client.get("/ships/0")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["result"]["ship"]["type"], "Frigate")

    #################################################################################################
    def test_set_destination(self):
        self.client.post("/ships/1/set_destination", params={"destination_id": "3"})
        response = self.client.get("/ships/1").json()
        self.assertEqual(response["result"]["ship"]["destination"]["id"], 3)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
