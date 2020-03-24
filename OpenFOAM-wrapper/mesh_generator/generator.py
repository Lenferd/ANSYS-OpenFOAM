import subprocess
from string import Template
from mesh_generator.template import MESH_FILE_TEMPLATE
from utils.logger import Logger, LogLvl
from configs.mesh import MeshConfig
from configs.fragmentation import FragmentationConfig

_logger = Logger(LogLvl.LOG_INFO)


class MeshGenerator:
    def __init__(self, mesh_config: MeshConfig, fragmentation_config: FragmentationConfig):
        self.mesh_config = mesh_config
        self.fragmentation_config = fragmentation_config

        self.out_file = "system/blockMeshDict"

    def generate(self, custom_out_file=None):
        _logger.info("\n\n===== Run geometry generating")
        self.__print_configuration()

        self.__calculate_points()
        self.__calculate_fragmentation()

        text = self.__format_text()

        file_to_write = self.out_file
        if (custom_out_file is not None) and (len(custom_out_file)):
            file_to_write = custom_out_file

        self.__save_geometry(text, file_to_write)
        _logger.info("===== End geometry generating\n\n")

        _logger.info("\n\n===== Run block mesh generating")
        self.__generate_mesh()
        # Just because there a lots of logs from blockMesh command
        _logger.info("===== End block mesh generating\n\n")

    def __print_configuration(self):
        _logger.log(LogLvl.LOG_INFO, "Generate mesh with size:")
        _logger.log(LogLvl.LOG_INFO,
                    "width_mm: {}\theight_mm: {}\tlength_mm: {}".format(
                        self.mesh_config.width_mm,
                        self.mesh_config.height_mm,
                        self.mesh_config.length_mm))

        _logger.log(LogLvl.LOG_INFO, "Generate mesh with fragmentation:")
        _logger.log(LogLvl.LOG_INFO,
                    "width_fragmentation: {}, height_fragmentation: {}, length_fragmentation: {}".format(
                        self.fragmentation_config.width,
                        self.fragmentation_config.height,
                        self.fragmentation_config.length))

    def __calculate_points(self):
        # TODO add check, that convertToMeters is 0.001 (m to mm)
        width_mm = self.mesh_config.width_mm
        height_mm = self.mesh_config.height_mm
        length_mm = self.mesh_config.length_mm

        p1 = [0, 0, 0]
        p2 = [width_mm, 0, 0]
        p3 = [width_mm, height_mm, 0]
        p4 = [0, height_mm, 0]
        p5 = [0, 0, length_mm]
        p6 = [width_mm, 0, length_mm]
        p7 = [width_mm, height_mm, length_mm]
        p8 = [0, height_mm, length_mm]

        arr = [p1, p2, p3, p4, p5, p6, p7, p8]
        self.points = ""
        for i in range(len(arr)):
            self.points += "    ({} {} {})".format(arr[i][0], arr[i][1], arr[i][2])
            if i + 1 != len(arr):
                self.points += "\n"

    def __calculate_fragmentation(self):
        mesh_elem_size_mm = self.fragmentation_config.elem_size_mm
        assert (self.mesh_config.width_mm >= mesh_elem_size_mm)
        assert (self.mesh_config.height_mm >= mesh_elem_size_mm)
        assert (self.mesh_config.length_mm >= mesh_elem_size_mm)

        # TODO enable dynamic fragmentation
        # length_fragmentation = int(float(length_mm) / mesh_elem_size_mm)
        # height_fragmentation = int(float(height_mm) / mesh_elem_size_mm)
        # width_fragmentation = int(float(width_mm) / mesh_elem_size_mm)
        # TODO try to use 6 2 1 (default in tutorial)

        # x - width, y - height, z - length
        self.fragmentation = "    hex (0 1 2 3 4 5 6 7) ({} {} {}) simpleGrading (1.0 1.0 1.0)".format(
            self.fragmentation_config.width,
            self.fragmentation_config.height,
            self.fragmentation_config.length)

    def __format_text(self):
        t = Template(MESH_FILE_TEMPLATE)
        return t.substitute(points=self.points, fragmentation=self.fragmentation)

    @staticmethod
    def __save_geometry(text, filename):
        if filename != 0:
            f = open(filename, "w+")
            f.writelines(text)
            f.close()
        else:
            print(text)

    @staticmethod
    def __generate_mesh():
        try:
            subprocess.call(['blockMesh'])
        except OSError:
            _logger.error("blockMesh not found. Please check that you have prepared OpenFOAM environment")