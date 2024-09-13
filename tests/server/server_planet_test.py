import unittest
from fastapi.testclient import TestClient

from MooToo.server.main import app


#####################################################################################################
class PlanetTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    #################################################################################################
    def test_can_build(self):
        response = self.client.get("/planets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["result"]["planet"]["can_build"]["building"], False)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
