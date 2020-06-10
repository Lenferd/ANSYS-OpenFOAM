import subprocess
import os
from string import Template

from configs.fragmentation import FragmentationConfig
from configs.mesh import SimpleBlockMeshConfig
from configs.execution import ExecutionConfig
from mesh_generator.template import MESH_FILE_TEMPLATE
from utils.logger import LogLvl, Logger
from utils.profiler import Profiler

_logger = Logger(LogLvl.LOG_ERROR)
enable_profiler = os.environ.get('PROFILER')


class SimpleBlockMeshGenerator:
    def __init__(self, mesh_config: SimpleBlockMeshConfig, fragmentation_config: FragmentationConfig,
                 execution_config: ExecutionConfig = ExecutionConfig()):
        self.mesh_config = mesh_config
        self.fragmentation_config = fragmentation_config
        self.exec_config = execution_config
        self.out_file = "system/blockMeshDict"

        if self.exec_config is not None:
            self.out_file = os.path.join(execution_config.execution_folder, self.out_file)

        self._profiler = Profiler(enable_profiler)

    def __del__(self):
        self._profiler.print_report()

    def create(self, custom_out_file=None):
        _logger.info("\n\n===== Run geometry generating")
        self._profiler.start("Geometry creating")
        self._print_configuration()

        self._calculate_points()
        self._calculate_fragmentation()
        self._calculate_boundary()

        text = self._format_text()

        file_to_write = self.out_file
        if custom_out_file != 0 and (custom_out_file is not None) and (len(custom_out_file)):
            file_to_write = custom_out_file
        if custom_out_file == 0:
            file_to_write = 0

        self.save_geometry(text, file_to_write)
        self._profiler.stop("Geometry creating")
        _logger.info("===== End geometry generating\n\n")

    def generate(self):
        _logger.info("\n\n===== Run block mesh generating")
        self._profiler.start("Mesh generating")
        self.generate_mesh()
        self._profiler.stop("Mesh generating")
        # Just because there a lots of logs from blockMesh command
        _logger.info("===== End block mesh generating\n\n")

    def _print_configuration(self):
        _logger.log(LogLvl.LOG_INFO, "Generate mesh with size:")
        _logger.log(LogLvl.LOG_INFO,
                    "width_mm: {}\theight_mm: {}\tlength_mm: {}".format(
                        self.mesh_config.width_mm,
                        self.mesh_config.height_mm,
                        self.mesh_config.length_mm))

        _logger.log(LogLvl.LOG_INFO, "Generate mesh with fragmentation:")
        _logger.log(LogLvl.LOG_INFO,
                    "{:>25}{:>25}{:>25}\n".format(
                        "width_fragmentation: " + str(self.fragmentation_config.width),
                        "height_fragmentation: " + str(self.fragmentation_config.height),
                        "length_fragmentation: " + str(self.fragmentation_config.length)))

    def _calculate_points(self):
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

    def _calculate_fragmentation(self):
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

    def _calculate_boundary(self):
        _logger.error("Not implemented")

    def _format_text(self):
        t = Template(MESH_FILE_TEMPLATE)
        boundary = """    topSurface
    {
        type patch;
        faces
        (
            (2 3 7 6)
        );
    }

    bottomSurface
    {
        type patch;
        faces
        (
            (0 1 5 4)
        );
    }

    rearFixedEnd
    {
        type patch;
        faces
        (
            (4 5 6 7)
        );
    }

    frontTractionEnd
    {
        type patch;
        faces
        (
            (0 1 2 3)
        );
    }

    leftSurface
    {
        type patch;
        faces
        (
            (0 3 7 4)
        );
    }
    
    rightSurface
    {
        type patch;
        faces
        (
            (1 2 6 5)
        );
    }"""
        return t.substitute(points=self.points, fragmentation=self.fragmentation, boundary=boundary)

    @staticmethod
    def save_geometry(text, filename):
        if filename != 0:
            _logger.debug("Save file to: {}".format(filename))
            f = open(filename, "w+")
            f.writelines(text)
            f.close()
        else:
            print(text)

    def generate_mesh(self):
        # FIXME temporary solution
        # FIXME Not check that is not None
        openfoam_folder = "OPENFOAM FOLDER NOT SPECIFIED"
        if self.exec_config is not None:
            if self.exec_config.openfoam_folder is not None:
                openfoam_folder = self.exec_config.openfoam_folder

        env_script = "ENV SCRIPT NOT SPECIFIED"
        if self.exec_config is not None:
            if self.exec_config.prepare_env_script is not None:
                env_script = self.exec_config.prepare_env_script

        # Make sure script have commented lines, where FOAM_INST_DIR is set
        prepare_call = "export FOAM_INST_DIR=" + openfoam_folder
        prepare_call += "; "
        prepare_call += ". " + env_script
        prepare_call += "; "
        prepare_call += "cd " + self.exec_config.execution_folder
        try:
            # FIXME get back log for debug or info
            # subprocess.call(["{}; {} > /dev/null".format(prepare_call, "blockMesh")], shell=True)
            # FIXME Debug
            command = "{}; {}".format(prepare_call, "blockMesh")
            _logger.info(command)
            if _logger.log_lvl == LogLvl.LOG_DEBUG:
                subprocess.call("{}".format(command), shell=True)
            else:
                subprocess.call("{} > /dev/null".format(command), shell=True)
        except OSError:
            raise OSError("blockMesh not found. Please check that you have prepared OpenFOAM environment")
