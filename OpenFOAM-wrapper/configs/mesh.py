from argparse import ArgumentParser


def add_mesh_switch_arguments(parser: ArgumentParser):
    parser.add_argument("-mc", "--mesh_config", type=str,
                        choices=["SimpleBlockMeshConfig", "RailMeshConfig"],
                        help="Which config to use to specify geometry", default="SimpleBlockMeshConfig")


class SimpleBlockMeshConfig:
    def __init__(self, width_mm=100, height_mm=100, length_mm=1000):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.length_mm = length_mm

    @staticmethod
    def create_from_args(args):
        mesh_conf = SimpleBlockMeshConfig()
        mesh_conf.width_mm = args.geom_width
        mesh_conf.height_mm = args.geom_height
        mesh_conf.length_mm = args.geom_length
        return mesh_conf


class SimpleBlockMeshArguments:
    @staticmethod
    def add_geometry_arguments(parser: ArgumentParser):
        parser.add_argument("-gw", "--geom_width", type=int, help="Geometry object width in mm. default=100",
                            default=100)
        parser.add_argument("-gh", "--geom_height", type=int, help="Geometry object height in mm. default=100",
                            default=100)
        parser.add_argument("-gl", "--geom_length", type=int, help="Geometry object length in mm. default=1000",
                            default=1000)

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
        parser.add_argument("-ghd", "--geom_height_diff", type=int, default=10,
                            help="Geometry object height step. default=10")
        parser.add_argument("-gld", "--geom_length_diff", type=int, default=10,
                            help="Geometry object length step. default=10")


# Lines from bottom
class RailMeshConfig:
    def __init__(self, width_lines=[300, 100, 100, 300],
                 height_distance=[100, 100, 100],
                 length=1000):
        self.width_lines = width_lines
        self.height_distance = height_distance
        self.length = length

    @staticmethod
    def create_from_args(args):
        mesh_conf = RailMeshConfig()
        mesh_conf.width_lines = args.width_lines
        mesh_conf.height_distance = args.height_distance
        mesh_conf.length = args.length
        amount_width = len(mesh_conf.width_lines)
        amount_height = len(mesh_conf.height_distance)
        if amount_width < 2:
            print("Amount of width lines should be >= 2. Now {}".format(amount_width))
            assert (amount_width >= 2)
        if amount_height != amount_width - 1:
            print("Amount of height values should be == width values - 1. Now {} != {} - 1".format(amount_height,
                                                                                                   amount_width))
            assert (amount_height == amount_width - 1)

        return mesh_conf


class RailMeshArguments:
    @staticmethod
    def add_geometry_arguments(parser: ArgumentParser):
        parser.add_argument('-wl', '--width_lines', metavar='Width, mm', type=int, nargs='+', required=True,
                            help=r"""
        Width lines 1
         .<------------->. 
         /\
         || Height distance
         \/
         ,<------------->. 
           Width line 0
         Example: -wl 20 20 -ddh 10 -l 30 -> cube 20 x 10 x 30 (x, y, z)
                                    """ +
                                 'Size of lines from which to create mesh (represent width), mm. From bottom to top.')
        parser.add_argument('-dh', '--height_distance', metavar='Height, mm', type=int, nargs='+', required=True,
                            help='Size between lines (represent height), mm. From bottom to top')
        parser.add_argument('-l', '--length', metavar='Length, mm', type=int, required=True,
                            help='Length of the object')
