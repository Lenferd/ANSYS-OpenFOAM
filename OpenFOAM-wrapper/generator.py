from mesh_generator.generator import MeshGenerator
from configs.mesh import MeshConfig, MeshArguments
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    MeshArguments.add_geometry_arguments(parser)
    FragmentationArguments.add_fragmentation_arguments(parser)

    args = parser.parse_args()

    mesh_conf = MeshConfig.create_from_args(args)
    fragmentation_conf = FragmentationConfig.create_from_args(args)

    mesh = MeshGenerator(mesh_conf, fragmentation_conf)
    mesh.generate(args.geometry_output)
