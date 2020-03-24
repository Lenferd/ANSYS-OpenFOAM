import datetime
import sys
from collections import namedtuple
from executor.executor import Executor
from utils.arg_parser import Arguments
from argparse import ArgumentParser
from configs.mesh import MeshConfig, MeshArguments
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from configs.execution import ExecutionConfig, ExecutionArguments
from mesh_generator.generator import MeshGenerator

# # @Experiment description
# # Run signle calculation on w = 100, h = 100, l = 1000
# # Include block mesh generating and output parsing
# def single_test_run():
#     width = 100
#     height = 100
#     length = 1000
#     # arguments = Arguments(width_mm=width, height_mm=height, length_mm=length)
#     arguments = Arguments(width_mm=width, height_mm=height, length_mm=length, file_name="")
#     mesh_config = {'length_fragmentation': 8,
#                    'height_fragmentation': 2,
#                    'width_fragmentation': 2}
#     run(arguments.width_mm, arguments.height_mm, arguments.length_mm, mesh_config)


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
    # w = 2
    # while w <= 128:
    #     h = 2
    #     while h <= 128:
    #         mesh_config = {'length_fragmentation': 16,
    #                        'height_fragmentation': h,
    #                        'width_fragmentation': w}
    #         run(arguments.width_mm, arguments.height_mm, arguments.length_mm, mesh_config)
    #         h *= 2
    #     w *= 2

