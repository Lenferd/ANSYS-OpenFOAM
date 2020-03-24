from executor.executor import Executor
from argparse import ArgumentParser
from configs.mesh import MeshConfig, MeshArguments
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from configs.execution import ExecutionConfig, ExecutionArguments
from mesh_generator.generator import MeshGenerator

if __name__ == '__main__':
    parser = ArgumentParser()
    MeshArguments.add_geometry_argument_iter(parser)
    FragmentationArguments.add_fragmentation_arguments(parser)
    ExecutionArguments.add_execution_arguments(parser)
    args = parser.parse_args()

    fragmentation_conf = FragmentationConfig.create_from_args(args)
    execution_conf = ExecutionConfig.create_from_args(args)

    # TODO No fragmentation iters for now
    for width in range(args.geom_width_start, args.geom_width_end + 1, args.geom_width_diff):
        for height in range(args.geom_height_start, args.geom_height_end + 1, args.geom_height_diff):
            for length in range(args.geom_length_start, args.geom_length_end + 1, args.geom_length_diff):
                mesh_conf = MeshConfig(width, height, length)
                mesh = MeshGenerator(mesh_conf, fragmentation_conf)
                mesh.generate(args.geometry_output)

                executor = Executor(execution_conf, mesh_conf, fragmentation_conf)
                executor.run()
