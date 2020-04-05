from unittest.case import TestCase

from mesh_generator.point import Point


class TestPoint(TestCase):
    def test_point_str(self):
        point = Point(6, 6, 6)
        self.assertNotEqual(-1, str(point).find("6"))
