from unittest import TestCase
from mesh_generator.generator import RailMeshGenerator, Point
from configs.mesh import RailMeshConfig
from configs.fragmentation import FragmentationConfig


class TestRailMeshGenerator(TestCase):
    def test_create_correct_points(self):
        config = RailMeshConfig()
        fragmentation = FragmentationConfig()
        mesh_generator = RailMeshGenerator(config, fragmentation)
        mesh_generator.generate(0)

    def test_point_str(self):
        point = Point(6, 6, 6)
        self.assertNotEqual(-1, str(point).find("6"))
