from mesh_generator.simple_generator import SimpleBlockMeshGenerator
from configs.mesh import SimpleBlockMeshConfig, SimpleBlockMeshArguments
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    SimpleBlockMeshArguments.add_geometry_arguments(parser)
    FragmentationArguments.add_fragmentation_arguments(parser)

    args = parser.parse_args()

    mesh_conf = SimpleBlockMeshConfig.create_from_args(args)
    fragmentation_conf = FragmentationConfig.create_from_args(args)

    mesh = SimpleBlockMeshGenerator(mesh_conf, fragmentation_conf)
    mesh.create()
