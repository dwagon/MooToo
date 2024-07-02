import unittest

from MooToo.constants import Technology
from MooToo.galaxy import Galaxy, get_system_positions


#####################################################################################################
class TestGalaxy(unittest.TestCase):
    def setUp(self):
        self.galaxy = Galaxy()

    def test_get_system_positions(self):
        positions = get_system_positions(5)
        self.assertEqual(len(positions), 5)

    def test_find_home_systems(self):
        systems = self.galaxy.find_home_systems(3)
        self.assertEqual(len(systems), 3)

    def test_default_start(self):
        self.galaxy.populate("avg")
        emp_name = list(self.galaxy.empires.keys())[0]
        self.assertIn(Technology.COLONY_SHIP, self.galaxy.empires[emp_name].known_techs)

    def test_pre_start(self):
        self.galaxy.populate("pre")
        emp_name = list(self.galaxy.empires.keys())[0]
        self.assertNotIn(Technology.COLONY_SHIP, self.galaxy.empires[emp_name].known_techs)

    def test_advanced_start(self):
        self.galaxy.populate("adv")
        emp_name = list(self.galaxy.empires.keys())[0]
        self.assertIn(Technology.COLONY_SHIP, self.galaxy.empires[emp_name].known_techs)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
