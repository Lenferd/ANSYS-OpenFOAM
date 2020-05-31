from argparse import ArgumentParser


class FragmentationConfig:
    elem_size_mm = 20

    def __init__(self, width_fragmentation=12, height_fragmentation=12, length_fragmentation=10):
        self.width = width_fragmentation
        self.height = height_fragmentation
        self.length = length_fragmentation

    @staticmethod
    def create_from_args(args):
        fragmentation_conf = FragmentationConfig()
        # TODO How to avoid this duplication?
        if args.fragmentation_width:
            fragmentation_conf.width = args.fragmentation_width
        if args.fragmentation_height:
            fragmentation_conf.height = args.fragmentation_height
        if args.fragmentation_length:
            fragmentation_conf.length = args.fragmentation_length
        return fragmentation_conf


class FragmentationArguments:
    @staticmethod
    def add_fragmentation_arguments(parser: ArgumentParser):
        parser.add_argument("-fw", "--fragmentation_width", type=int, help="Fragmentation on width axes (X)")
        parser.add_argument("-fh", "--fragmentation_height", type=int, help="Fragmentation on height axes (Y)")
        parser.add_argument("-fl", "--fragmentation_length", type=int, help="Fragmentation on length axes (Z)")
