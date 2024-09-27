import unittest
from fastapi.testclient import TestClient
from MooToo.server.main import app


#####################################################################################################
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    #################################################################################################
    def test_ship_list(self):
        response = self.client.get("/ships")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["result"]["ships"][0], {"id": 1, "url": "/ships/1"})

    #################################################################################################
    def test_ship_get(self):
        response = self.client.get("/ships/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "OK")

    #################################################################################################
    def Xtest_set_destination(self):  # Need to make sure dest is in range first
        self.client.post("/ships/1/set_destination", params={"destination_id": "3"})
        response = self.client.get("/ships/1").json()
        self.assertEqual(response["result"]["ship"]["destination"], 3)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
