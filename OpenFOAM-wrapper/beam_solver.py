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

def constraint0(points):
    # -y
    print(-points[1])


def constraint1(points):
    #     -x
    print(-points[0])


def constraint2(points):
    x = points[0]
    y = points[1]
    k = 0.75
    result = k / (x * y) - 1
    print(result)


def criterion0(points):
    x = points[0]
    y = points[1]
    result = x * y

    print(result)

# @restrictions
# 1) Stress no more then
# @criterions
# 1) Weight should be minimum
#
#

class BeamSolver:
    def __init__(self):
        # Create default mesh generator config and fragmentation config
        self.mesh_cof = SimpleBlockMeshConfig()
        self.fragmentation_conf = FragmentationConfig()
        self.execution_config = ExecutionConfig()

        # TODO check that specified is required
        self.height = -1
        self.width = -1

    def setPlaneSizes(self, height, width):
        self.height = height
        self.width = width

    # Weight not more
    def constraint0(self):
        # FIXME
        mesh_generator = SimpleBlockMeshGenerator()


        mesh = mesh_generator(mesh_conf, fragmentation_conf)
        mesh.create()
        mesh.generate()

        executor = Executor(execution_conf, mesh_conf, fragmentation_conf)
        executor.run()


# def constraint0(points):
    #     # -y
    #     print(-points[1])
    #
    #
    # def constraint1(points):
    #     #     -x
    #     print(-points[0])
    #
    #
    # def constraint2(points):
    #     x = points[0]
    #     y = points[1]
    #     k = 0.75
    #     result = k / (x * y) - 1
    #     print(result)
    #
    #
    # def criterion0(points):
    #     x = points[0]
    #     y = points[1]
    #     result = x * y
    #     print(result)

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


    if function == "constraint.0":
        constraint0(points)
    if function == "constraint.1":
        constraint1(points)
    if function == "constraint.2":
        constraint2(points)
    if function == "criterion.0":
        criterion0(points)