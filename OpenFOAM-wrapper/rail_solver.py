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

from sys import argv

# TODO Remove unnecessary comments
# TODO use subprocess.getoutput() - where (?)

MIDDLE_LINE_ALGO = "middle_line"
LEFT_LINE_ALGO = "left_line"


class RailSolver:
    def __init__(self):
        # Only for wo height case
        self.k_full_height = 30
        self.wo_height = False
        self.k_length = 1000

        self.k_max_deformation = 4.4e-5
        self.k_max_stress = 3.3e+9
        self.k_density = 7850
        self.k_mm_to_m = 0.001
        # FIXME Manual switch required
        self.k_approach = MIDDLE_LINE_ALGO

        # Mesh config
        self.mesh_config = RailMeshConfig()

        # Fragmentation config
        self.fragmentation_config = FragmentationConfig(5, 5, 10)

        # Exec config
        self.execution_config = ExecutionConfig()

        # FIXME Hardcoded
        # FIXME Aware of potential duplication "OpenFOAM/OpenFOAM-dev/OpenFOAM-dev"
        self.execution_config.openfoam_folder = "/home/lenferd/prog/OpenFOAM"
        # self.execution_config.execution_folder = os.path.abspath(os.getcwd())
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Fixme hardcoded. Expected format: /home/lenferd/OpenFOAM/lenferd-v1906/run/rail-20-05-06-2/OpenFOAM-wrapper
        #  /rail_solver.py
        rail_pos = script_dir.rfind("Beam")
        foam_pos = script_dir.rfind("OpenFOAM-wrapper")
        if rail_pos == -1 or foam_pos == -1:
            # FIXME Hardcoded
            # raise Exception("rail folder (openfoam project folder) or OpenFOAM-wrapper not found in path: {}".format(script_dir))
            print("HARDCORED value is used!")
            self.execution_config.execution_folder = "/home/lenferd/OpenFOAM/lenferd-dev/run/glsymm-cantileverBeam-20200524"
        else:
            self.execution_config.execution_folder = script_dir[:foam_pos]

        print("[D] execution_folder: {}".format(self.execution_config.execution_folder))
        self.execution_config.output_dir = os.path.join(self.execution_config.execution_folder, "out")
        # FIXME Hardcoded
        self.execution_config.prepare_env_script = "/home/lenferd/prog/OpenFOAM/OpenFOAM-dev/etc/bashrc_modified"

    def set_plane_sizes(self, width_cuts):
        if self.wo_height:
            # Specify mesh config
            self.mesh_config.width_lines = width_cuts

            # Calculate height based on amount of cuts
            number_of_cuts = 0
            if self.k_approach == MIDDLE_LINE_ALGO:
                number_of_cuts = len(width_cuts)
            else:
                assert (len(width_cuts) % 2 == 0)
                number_of_cuts = int(len(width_cuts) / 2)

            height = self.k_full_height / (number_of_cuts - 1)
            self.mesh_config.height_distance = [height] * (number_of_cuts - 1)
        else:
            number_of_cuts = int((len(width_cuts) + 1) / 2)
            self.mesh_config.width_lines = width_cuts[:number_of_cuts]
            self.mesh_config.height_distance = width_cuts[number_of_cuts:]

        self.mesh_config.length = self.k_length

        # Create mesh
        mesh = RailMeshGenerator(self.mesh_config, self.fragmentation_config, self.execution_config)
        mesh.create()
        mesh.generate()

    def __debug_message(self, results):
        debug = os.environ.get('DEBUG')
        if debug:
            print("=== Debug ===")
            print("python3 " + " ".join(argv[:-1]) + " \"{}\"".format(argv[-1]))
            print("\"{}\"".format(argv[-1]))
            print(self.mesh_config.width_lines)
            self.criterion_0()
            print("Targets: deform {:.2e}, stress {:.2e}".format(self.k_max_deformation, self.k_max_stress))
            print("Deform: {:.2e} : {}".format(results["D"], results["D"] < self.k_max_deformation))
            print("Stress: {:.2e} : {}".format(results["sigmaEq"], results["sigmaEq"] < self.k_max_stress))

    # Deformation not more than ...
    def constraint_0(self):
        deformation_name = "D"
        # FIXME execution for reproduced constrain. Need to use hash if possible
        executor = Executor(self.execution_config, self.mesh_config, self.fragmentation_config)
        executor.run()
        results = executor.get_results()
        print("==== D constraint_0")
        self.__debug_message(results)

        return results[deformation_name] - self.k_max_deformation

    # Stress not more than ...
    def constraint_1(self):
        stresss_name = "sigmaEq"
        executor = Executor(self.execution_config, self.mesh_config, self.fragmentation_config)
        executor.run()
        results = executor.get_results()
        print("==== stress constraint_1")

        self.__debug_message(results)
        return results[stresss_name] - self.k_max_stress

    # Weight (minimum should be)
    def criterion_0(self):
        print("==== mass criterion_0")
        weight = 0

        if self.k_approach == MIDDLE_LINE_ALGO:
            for i in range(len(self.mesh_config.width_lines) - 1):
                volume = 0.5 * (self.mesh_config.width_lines[i] * self.k_mm_to_m + self.mesh_config.width_lines[i + 1] * self.k_mm_to_m) \
                         * self.mesh_config.height_distance[i] * self.k_mm_to_m * self.mesh_config.length * self.k_mm_to_m
                weight += volume * self.k_density
        else:
            for i in range(len(self.mesh_config.height_distance)):
                # Second point is width itself
                volume = 0.5 * (self.mesh_config.width_lines[i * 2 + 1] * self.k_mm_to_m + self.mesh_config.width_lines[(i + 1) * 2 + 1] * self.k_mm_to_m ) \
                         * self.mesh_config.height_distance[i] * self.k_mm_to_m * self.mesh_config.length * self.k_mm_to_m
                print("volume {} ".format(volume))
                weight += volume * self.k_density

        print("Weight: {}".format(weight))
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