from unittest import TestCase
from mesh_generator.rail_generator import RailMeshGenerator
from configs.mesh import RailMeshConfig
from configs.fragmentation import FragmentationConfig


class TestRailMeshGenerator(TestCase):
    def test_create_correct_points(self):
        config = RailMeshConfig()
        config.width_lines = [100, 100]
        config.height_distance = [200]
        config.length = 300

        fragmentation = FragmentationConfig()
        mesh_generator = RailMeshGenerator(config, fragmentation)
        mesh_generator.create(0)

        expected = ['(100 0 0)',
                    '(100 200 0)',
                    '(0 200 0)',
                    '(0 0 0)',
                    '(100 0 300)',
                    '(100 200 300)',
                    '(0 200 300)',
                    '(0 0 300)']
        self.assertEqual(expected, mesh_generator.points)

    def test_correct_fragmentation(self):
        config = RailMeshConfig()
        config.width_lines = [100, 100]
        config.height_distance = [200]
        config.length = 300

        fragmentation = FragmentationConfig()
        mesh_generator = RailMeshGenerator(config, fragmentation)
        mesh_generator.create(0)

        expected = "hex (0 1 2 3 4 5 6 7) (2 2 5) simpleGrading (1.0 1.0 1.0)"
        self.assertEqual(expected, mesh_generator.fragmentation_text.strip())

    def test_correct_boundary(self):
        config = RailMeshConfig()
        config.width_lines = [100, 100]
        config.height_distance = [200]
        config.length = 300

        fragmentation = FragmentationConfig()
        mesh_generator = RailMeshGenerator(config, fragmentation)
        mesh_generator.create(0)

        expected = r"""frontTractionEnd
    {
        type patch;
        faces
        (
			(0 1 2 3)
        );
    }    rearFixedEnd
    {
        type patch;
        faces
        (
			(4 5 6 7)
        );
    }    topSurface
    {
        type patch;
        faces
        (
			(1 5 6 2)
        );
    }    bottomSurface
    {
        type patch;
        faces
        (
			(0 4 7 3)
        );
    }    rightSurface
    {
        type patch;
        faces
        (
			(0 4 5 1)
        );
    }    leftSurface
    {
        type patch;
        faces
        (
			(3 2 6 7)
        );
    }"""
        self.assertEqual(expected, mesh_generator.boundaries_text.strip())
