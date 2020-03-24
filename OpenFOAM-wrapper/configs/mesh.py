from argparse import ArgumentParser


class MeshConfig:
    def __init__(self, width_mm=100, height_mm=100, length_mm=1000):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.length_mm = length_mm

    @staticmethod
    def create_from_args(args):
        mesh_conf = MeshConfig()
        # TODO How to avoid this duplication?
        if args.geom_width:
            mesh_conf.width_mm = args.geom_width
        if args.geom_height:
            mesh_conf.height_mm = args.geom_height
        if args.geom_length:
            mesh_conf.length_mm = args.geom_length
        return mesh_conf


class MeshArguments:
    @staticmethod
    def add_geometry_arguments(parser: ArgumentParser):
        parser.add_argument("-gw", "--geom_width", type=int, help="Geometry object width in mm")
        parser.add_argument("-gh", "--geom_height", type=int, help="Geometry object height in mm")
        parser.add_argument("-gl", "--geom_length", type=int, help="Geometry object length in mm")

        parser.add_argument("-go", "--geometry_output", type=str, help="Save geometry description to specified file")
