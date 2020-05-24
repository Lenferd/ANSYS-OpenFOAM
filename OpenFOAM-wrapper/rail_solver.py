from executor.executor import Executor
import os
from sys import argv

from argparse import ArgumentParser
from configs.mesh import add_mesh_switch_arguments
from configs.mesh import SimpleBlockMeshConfig, SimpleBlockMeshArguments
from configs.mesh import RailMeshArguments, RailMeshConfig
from configs.fragmentation import FragmentationConfig, FragmentationArguments
from configs.execution import ExecutionConfig, ExecutionArguments
from mesh_generator.simple_generator import SimpleBlockMeshGenerator
from mesh_generator.rail_generator import RailMeshGenerator

from sys import argv

# TODO Remove unnecessary comments
# TODO use subprocess.getoutput() - where (?)

MIDDLE_LINE_ALGO = "middle_line"
LEFT_LINE_ALGO = "left_line"


class RailSolver:
    def __init__(self):
        # TODO Should we also use those values?
        self.k_full_height = 400
        self.k_length = 1000

        self.k_max_deformation = 2.139e-6
        self.k_max_stress = 775900
        self.k_density = 7850
        self.k_mm_to_m = 0.001
        self.k_approach = LEFT_LINE_ALGO

        # Mesh config
        self.mesh_config = RailMeshConfig()

        # Fragmentation config
        self.fragmentation_config = FragmentationConfig(6, 6, 6)

        # Exec config
        self.execution_config = ExecutionConfig()
        # FIXME Hardcoded
        # FIXME Aware of potential duplication "OpenFOAM/OpenFOAM-dev/OpenFOAM-dev"
        self.execution_config.openfoam_folder = "/home/lenferd/prog/OpenFOAM"
        self.execution_config.execution_folder = "/home/lenferd/OpenFOAM/lenferd-dev/run/gl-cantileverBeam-20200524"
        self.execution_config.output_dir = os.path.join(self.execution_config.execution_folder, "out")
        # FIXME Hardcoded
        self.execution_config.prepare_env_script = "/home/lenferd/prog/OpenFOAM/OpenFOAM-dev/etc/bashrc_modified"

    def set_plane_sizes(self, width_cuts):
        # Specify mesh config
        self.mesh_config.width_lines = width_cuts

        # Calculate height based on amount of cuts
        number_of_cuts = 0
        if self.k_approach == MIDDLE_LINE_ALGO:
            number_of_cuts = len(width_cuts)
        else:
            assert (len(width_cuts) % 2 == 0)
            number_of_cuts = int(len(width_cuts) / 2)

        height = self.k_full_height / number_of_cuts
        self.mesh_config.height_distance = [height] * (number_of_cuts - 1)

        self.mesh_config.length = self.k_length

        # Create mesh
        mesh = RailMeshGenerator(self.mesh_config, self.fragmentation_config, self.execution_config)
        mesh.create()
        mesh.generate()

    # Deformation not more than ...
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

    # Stress not more than ...
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
        weight = 0

        for i in range(len(self.mesh_config.width_lines)):
            volume = 0.5 * (self.mesh_config.width_lines[i] + self.mesh_config.width_lines[i + 1]) \
                     * self.mesh_config.height_distance[i] * self.mesh_config.length * self.k_mm_to_m
            weight += volume * self.k_density

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

    beamSolver = RailSolver()
    # first - height, second - width
    beamSolver.set_plane_sizes(points)

    result = None
    if function == "constraint.0":
        result = beamSolver.constraint_0()
    if function == "constraint.1":
        result = beamSolver.constraint_1()
    if function == "criterion.0":
        result = beamSolver.criterion_0()

    print("RailSolver:[{}]".format(result))
