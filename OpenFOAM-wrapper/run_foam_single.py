
from executor.executor import Executor
from argparse import ArgumentParser
from configs.mesh import MeshConfig, MeshArguments
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from configs.execution import ExecutionConfig, ExecutionArguments
from mesh_generator.generator import MeshGenerator

if __name__ == '__main__':
    parser = ArgumentParser()
    MeshArguments.add_geometry_arguments(parser)
    FragmentationArguments.add_fragmentation_arguments(parser)
    ExecutionArguments.add_execution_arguments(parser)
    args = parser.parse_args()

    mesh_conf = MeshConfig.create_from_args(args)
    fragmentation_conf = FragmentationConfig.create_from_args(args)
    execution_conf = ExecutionConfig.create_from_args(args)

    mesh = MeshGenerator(mesh_conf, fragmentation_conf)
    mesh.generate(args.geometry_output)

    executor = Executor(execution_conf, mesh_conf, fragmentation_conf)
    executor.run()
