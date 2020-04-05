from argparse import ArgumentParser


class MeshConfig:
    def __init__(self, width_mm=100, height_mm=100, length_mm=1000):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.length_mm = length_mm

    @staticmethod
    def create_from_args(args):
        mesh_conf = MeshConfig()
        mesh_conf.width_mm = args.geom_width
        mesh_conf.height_mm = args.geom_height
        mesh_conf.length_mm = args.geom_length
        return mesh_conf


class MeshArguments:
    @staticmethod
    def add_geometry_arguments(parser: ArgumentParser):
        parser.add_argument("-gw", "--geom_width", type=int, help="Geometry object width in mm. default=100", default=100)
        parser.add_argument("-gh", "--geom_height", type=int, help="Geometry object height in mm. default=100", default=100)
        parser.add_argument("-gl", "--geom_length", type=int, help="Geometry object length in mm. default=1000", default=1000)

        parser.add_argument("-go", "--geometry_output", type=str, help="Save geometry description to specified file")

    @staticmethod
    def add_geometry_argument_iter(parser: ArgumentParser):
        parser.add_argument("-gws", "--geom_width_start", type=int, default=40,
                            help="Geometry object width in mm lowest value. default=40")
        parser.add_argument("-ghs", "--geom_height_start", type=int, default=40,
                            help="Geometry object height in mm lowest value. default=40")
        parser.add_argument("-gls", "--geom_length_start", type=int, default=1000,
                            help="Geometry object length in mm lowest value. default=1000")

        parser.add_argument("-gwe", "--geom_width_end", type=int, default=100,
                            help="Geometry object width in mm lowest value. default=100")
        parser.add_argument("-ghe", "--geom_height_end", type=int, default=100,
                            help="Geometry object height in mm lowest value. default=100")
        parser.add_argument("-gle", "--geom_length_end", type=int, default=1000,
                            help="Geometry object length in mm lowest value. default=1000")

        parser.add_argument("-gwd", "--geom_width_diff", type=int, default=10,
                            help="Geometry object width step. default=10")
        parser.add_argument("-ghd", "--geom_height_diff", type=int,  default=10,
                            help="Geometry object height step. default=10")
        parser.add_argument("-gld", "--geom_length_diff", type=int, default=10,
                            help="Geometry object length step. default=10")

        parser.add_argument("-go", "--geometry_output", type=str, help="Save geometry description to specified file")


# Lines from bottom
class RailMeshConfig(MeshConfig):
    def __init__(self, first_line=300, second_line=100, third_line=100, fourth_line=300,
                 height_first=100, height_second=100, height_third=100, length=1000):
        self.first_line = first_line
        self.second_line = second_line
        self.third_line = third_line
        self.fourth_line = fourth_line
        self.height_first = height_first
        self.height_second = height_second
        self.height_third = height_third
        self.length = length

    @staticmethod
    def create_from_args(args):
        mesh_conf = RailMeshConfig()
        mesh_conf.first_line = args.first_line
        mesh_conf.second_line = args.second_line
        mesh_conf.third_line = args.third_line
        mesh_conf.fourth_line = args.fourth_line
        mesh_conf.height_first = args.height_first
        mesh_conf.height_second = args.height_second
        mesh_conf.height_third = args.height_third
        mesh_conf.length = args.length
        return mesh_conf
