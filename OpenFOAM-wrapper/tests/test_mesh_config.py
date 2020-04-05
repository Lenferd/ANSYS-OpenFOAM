import argparse
from unittest import TestCase
from configs.mesh import RailMeshConfig, RailMeshArguments


class TestRailMeshConfig(TestCase):
    def test_create_from_args(self):
        parser = argparse.ArgumentParser()
        RailMeshArguments.add_geometry_arguments(parser=parser)

        input_args = ["-wl", "20", "20"]
        input_args += ["-dh", "20"]
        input_args += ["-l 30"]
        args = parser.parse_args(args=input_args)
        config = RailMeshConfig.create_from_args(args)
        self.assertEqual([20, 20], config.width_lines)
        self.assertEqual([20], config.height_distance)
        self.assertEqual(30, config.length)
