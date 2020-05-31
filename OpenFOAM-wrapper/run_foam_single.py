import os

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

    # FIXME Hardcoded
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rail_pos = script_dir.rfind("Beam")
    foam_pos = script_dir.rfind("OpenFOAM-wrapper")
    if rail_pos == -1 or foam_pos == -1:
        raise Exception("Failed to find Beam folder in path")
    else:
        execution_conf.execution_folder = script_dir[:foam_pos]

    print("[!!!!] WARNING: prepare script and openfoam folder is hardcoded")
    execution_conf.prepare_env_script = "/home/lenferd/prog/OpenFOAM/OpenFOAM-dev/etc/bashrc_modified"
    execution_conf.openfoam_folder = "/home/lenferd/prog/OpenFOAM/"

    print(execution_conf.execution_folder)
    print(execution_conf.prepare_env_script)
    print(execution_conf.openfoam_folder)

    mesh = mesh_generator(mesh_conf, fragmentation_conf, execution_conf)
    mesh.create()
    mesh.generate()

    executor = Executor(execution_conf, mesh_conf, fragmentation_conf)
    executor.run()
