import unittest
from main import Entity, Transform
from panda3d.core import Vec3

class TestEngine(unittest.TestCase):
    def test_entity_component(self):
        e = Entity("Test")
        t = e.add_component(Transform)
        self.assertEqual(t.position, Vec3(0,0,0))

if __name__ == "__main__":
    unittest.main()
