from executor.executor import Executor
from argparse import ArgumentParser
from configs.mesh import add_mesh_switch_arguments
from configs.mesh import SimpleBlockMeshConfig, SimpleBlockMeshArguments
from configs.mesh import RailMeshArguments, RailMeshConfig
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from configs.execution import ExecutionConfig, ExecutionArguments
from mesh_generator.simple_generator import SimpleBlockMeshGenerator
from mesh_generator.rail_generator import RailMeshGenerator

from sys import argv

# TODO use subprocess.getoutput()

# @brief Beam end load task, only two configurable parameters and two restrictions (3 functions)
# @restrictions
# 1) Stress is not more than specified value
# 2) Deformation is not more than specified value
# @criterion
# 1) Weight should be minimum
class BeamSolver:
    def __init__(self):
        self.k_max_deformation = 2.139e-6
        self.k_max_stress = 775900
        self.k_density = 7850
        self.k_mm_to_m = 0.001

        # Create default mesh generator config and fragmentation config
        self.mesh_config = SimpleBlockMeshConfig()
        self.fragmentation_config = FragmentationConfig()
        self.execution_config = ExecutionConfig()

        self.execution_config.execution_folder = "/home/lenferd/OpenFOAM/lenferd-v1906/run/beamEndLoad-20-04-25/"
        self.execution_config.output_dir = self.execution_config.execution_folder + "out/"
        self.execution_config.prepare_env_script = "$HOME/prog/scientific/openfoam/etc/bashrc"

    def set_plane_sizes(self, height, width):
        self.mesh_config.length_mm = 1000
        self.mesh_config.height_mm = height
        self.mesh_config.width_mm = width

        mesh = SimpleBlockMeshGenerator(self.mesh_config, self.fragmentation_config, self.execution_config)
        mesh.create()
        mesh.generate()

    # Deformation not more then
    def constraint_0(self):
        deformation_name = "D"
        # FIXME execution for reproduced constrain. Need to use hash if possible
        executor = Executor(self.execution_config, self.mesh_config, self.fragmentation_config)
        executor.run()
        results = executor.get_results()
        print("==== D constraint_0")
        print(results)
        print(results[deformation_name])
        print(results[deformation_name] < self.k_max_deformation)
        print(results[deformation_name] - self.k_max_deformation)
        return results[deformation_name] - self.k_max_deformation

    # Stress not more then
    def constraint_1(self):
        stresss_name = "D"
        executor = Executor(self.execution_config, self.mesh_config, self.fragmentation_config)
        executor.run()
        results = executor.get_results()
        print("==== stress constraint_1")
        print(results)
        print(results[stresss_name])
        print(results[stresss_name] < self.k_max_stress)
        print(results[stresss_name] - self.k_max_stress)
        return results[stresss_name] - self.k_max_stress

    # Weight (minimum should be)
    def criterion_0(self):
        print("==== mass criterion_0")
        weight = self.k_density * \
                 self.mesh_config.width_mm * self.k_mm_to_m \
                 * self.mesh_config.height_mm * self.k_mm_to_m \
                 * self.mesh_config.length_mm * self.k_mm_to_m
        print(weight)
        return weight


if __name__ == '__main__':
    # print("BEAM SOLVER")
    # print("args: {}".format(argv))
    parameters = argv[1]

    paramList = parameters.split(";")

    dict = {}
    for param in paramList:
        split_result = param.split(":")
        pair = {split_result[0]: split_result[1]}
        dict.update(pair)

    # print(dict)
    dict["Points"] = dict["Points"].split(",")
    dict["Points"] = [float(i) for i in dict["Points"]]

    # print(dict)

    function = dict["Function"]
    points = dict["Points"]
    # Create BeamSolver

    beamSolver = BeamSolver()
    # first - height, second - width
    beamSolver.set_plane_sizes(points[0], points[1])

    result = None
    if function == "constraint.0":
        result = beamSolver.constraint_0()
    if function == "constraint.1":
        result = beamSolver.constraint_1()
    if function == "criterion.0":
        result = beamSolver.criterion_0()

    print("BeamSolver:[{}]".format(result))
