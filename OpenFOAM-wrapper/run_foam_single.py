from executor.executor import Executor
from argparse import ArgumentParser
from configs.mesh import add_mesh_switch_arguments
from configs.mesh import SimpleBlockMeshConfig, SimpleBlockMeshArguments
from configs.mesh import RailMeshArguments, RailMeshConfig
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from configs.execution import ExecutionConfig, ExecutionArguments
from mesh_generator.simple_generator import SimpleBlockMeshGenerator
from mesh_generator.rail_generator import RailMeshGenerator

if __name__ == '__main__':
    parser = ArgumentParser()
    add_mesh_switch_arguments(parser)
    args = parser.parse_known_args()

    config_generator = None
    mesh_generator = None
    if args[0].mesh_config == "SimpleBlockMeshConfig":
        SimpleBlockMeshArguments.add_geometry_arguments(parser)
        config_generator = SimpleBlockMeshConfig
        mesh_generator = SimpleBlockMeshGenerator
    else:
        RailMeshArguments.add_geometry_arguments(parser)
        config_generator = RailMeshConfig
        mesh_generator = RailMeshGenerator

    FragmentationArguments.add_fragmentation_arguments(parser)
    ExecutionArguments.add_execution_arguments(parser)
    args = parser.parse_args()

    mesh_conf = config_generator.create_from_args(args)
    fragmentation_conf = FragmentationConfig.create_from_args(args)
    execution_conf = ExecutionConfig.create_from_args(args)

    mesh = mesh_generator(mesh_conf, fragmentation_conf)
    mesh.create()
    mesh.generate()

    executor = Executor(execution_conf, mesh_conf, fragmentation_conf)
    executor.run()
