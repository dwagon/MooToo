import unittest

from MooToo.bigbang import create_galaxy
from MooToo.server.serializers.system import system_serializer


#####################################################################################################
class SystemSerializerTest(unittest.TestCase):
    def setUp(self):
        self.galaxy = create_galaxy()

    #################################################################################################
    def test_serialize(self):
        system_num = 1
        system = self.galaxy.systems[system_num]
        output = system_serializer(system)
        print(f"DBG {output}")
        self.assertEqual(output["name"], system.name)
        self.assertEqual(output["id"], system_num)


#####################################################################################################
if __name__ == "__main__":
    unittest.main()
