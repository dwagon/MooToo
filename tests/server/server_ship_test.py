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
        self.assertEqual(data["result"]["ships"][0], {"id": 0, "url": "/ships/0"})


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
