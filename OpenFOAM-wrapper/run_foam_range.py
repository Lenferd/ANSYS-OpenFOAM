from executor.executor import Executor
from argparse import ArgumentParser
from configs.mesh import SimpleBlockMeshConfig, SimpleBlockMeshArguments
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from configs.execution import ExecutionConfig, ExecutionArguments
from mesh_generator.simple_generator import SimpleBlockMeshGenerator

if __name__ == '__main__':
    parser = ArgumentParser()
    SimpleBlockMeshArguments.add_geometry_argument_iter(parser)
    FragmentationArguments.add_fragmentation_arguments(parser)
    ExecutionArguments.add_execution_arguments(parser)
    args = parser.parse_args()

    fragmentation_conf = FragmentationConfig.create_from_args(args)
    execution_conf = ExecutionConfig.create_from_args(args)

    # FIXME Hardcoded
    execution_conf.execution_folder = "/home/lenferd/OpenFOAM/lenferd-dev/run/cantieverBeam-20200528"
    print("[!!!!] WARNING: execution folder is hardcoded and is : {}".format(execution_conf.execution_folder))
    execution_conf.prepare_env_script = "/home/lenferd/prog/OpenFOAM/OpenFOAM-dev/etc/bashrc_modified"
    execution_conf.openfoam_folder = "/home/lenferd/prog/OpenFOAM/"

    # TODO No fragmentation iters for now
    for width in range(args.geom_width_start, args.geom_width_end + 1, args.geom_width_diff):
        for height in range(args.geom_height_start, args.geom_height_end + 1, args.geom_height_diff):
            for length in range(args.geom_length_start, args.geom_length_end + 1, args.geom_length_diff):
                mesh_conf = SimpleBlockMeshConfig(width, height, length)
                mesh = SimpleBlockMeshGenerator(mesh_conf, fragmentation_conf, execution_conf)
                mesh.create()
                mesh.generate()
                executor = Executor(execution_conf, mesh_conf, fragmentation_conf)
                executor.run()
