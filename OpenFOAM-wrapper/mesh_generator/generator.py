import subprocess
from string import Template
from mesh_generator.template import MESH_FILE_TEMPLATE, BOUNDARY_TEMPLATE
from configs.mesh import MeshConfig, RailMeshConfig
from configs.fragmentation import FragmentationConfig
from utils.logger import Logger, LogLvl

_logger = Logger(LogLvl.LOG_DEBUG)


class Point:
    def __repr__(self):
        return "({},{},{})".format(self.x, self.y, self.z)

    def __init__(self, x: int, y: int, z: int):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def get(self):
        return {self.x, self.y, self.z}

    def foam_print(self):
        return "({} {} {})".format(self.x, self.y, self.z)


class MeshGenerator:
    def __init__(self, mesh_config: MeshConfig, fragmentation_config: FragmentationConfig):
        self.mesh_config = mesh_config
        self.fragmentation_config = fragmentation_config

        self.out_file = "system/blockMeshDict"

    def generate(self, custom_out_file=None):
        _logger.info("\n\n===== Run geometry generating")
        self._print_configuration()

        self._calculate_points()
        self._calculate_fragmentation()
        self._calculate_boundary()

        text = self._format_text()

        file_to_write = self.out_file
        if (custom_out_file is not None) and (len(custom_out_file)):
            file_to_write = custom_out_file

        self._save_geometry(text, file_to_write)
        _logger.info("===== End geometry generating\n\n")

        _logger.info("\n\n===== Run block mesh generating")
        self._generate_mesh()
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
        return t.substitute(points=self.points, fragmentation=self.fragmentation)

    @staticmethod
    def _save_geometry(text, filename):
        if filename != 0:
            f = open(filename, "w+")
            f.writelines(text)
            f.close()
        else:
            print(text)

    @staticmethod
    def _generate_mesh():
        try:
            subprocess.call(['blockMesh'])
        except OSError:
            _logger.error("blockMesh not found. Please check that you have prepared OpenFOAM environment")


class RailMeshGenerator(MeshGenerator):
    def generate(self, custom_out_file=None):
        super().generate(custom_out_file)

    def _print_configuration(self):
        _logger.log(LogLvl.LOG_INFO, "Generate mesh with size:")
        _logger.log(LogLvl.LOG_INFO,
                    "{:>20}{:>20}{:>20}{:>20}\n"
                    "{:>20}{:>20}{:>20}\n"
                    "{:>20}\t".format(
                        "first_line: " + str(self.mesh_config.first_line),
                        "second_line: " + str(self.mesh_config.second_line),
                        "third_line: " + str(self.mesh_config.third_line),
                        "fourth_line: " + str(self.mesh_config.fourth_line),
                        "height_first: " + str(self.mesh_config.height_first),
                        "height_second: " + str(self.mesh_config.height_second),
                        "height_third: " + str(self.mesh_config.height_third),
                        "length: " + str(self.mesh_config.length),
                    ))

        _logger.log(LogLvl.LOG_INFO, "Generate mesh with fragmentation:")
        _logger.log(LogLvl.LOG_INFO,
                    "{:>25}{:>25}{:>25}\n".format(
                        "width_fragmentation: " + str(self.fragmentation_config.width),
                        "height_fragmentation: " + str(self.fragmentation_config.height),
                        "length_fragmentation: " + str(self.fragmentation_config.length)))

    def _check_points_restriction(self):
        for line in self.x_lines:
            assert (line % 2 == 0)
        for line in self.y_lines:
            assert (line % 2 == 0)
        assert (self.mesh_config.length % 2 == 0)

    def _calculate_points(self):
        # TODO add check, that convertToMeters is 0.001
        self.x_lines = [self.mesh_config.first_line,
                        self.mesh_config.second_line,
                        self.mesh_config.third_line,
                        self.mesh_config.fourth_line]
        self.y_lines = [self.mesh_config.height_first,
                        self.mesh_config.height_second,
                        self.mesh_config.height_third]

        self._check_points_restriction()

        middle_line_x = max(self.x_lines) / 2
        length = self.mesh_config.length
        front_plane = []
        back_plane = []

        for it in range(len(self.x_lines)):
            front_plane.append([Point(middle_line_x - self.x_lines[it] / 2, sum(self.y_lines[0:it]), 0),
                                Point(middle_line_x + self.x_lines[it] / 2, sum(self.y_lines[0:it]), 0)])
            back_plane.append([Point(middle_line_x - self.x_lines[it] / 2, sum(self.y_lines[0:it]), length),
                               Point(middle_line_x + self.x_lines[it] / 2, sum(self.y_lines[0:it]), length)])

        _logger.debug("Front plane")
        for line in front_plane:
            _logger.debug("{}".format(line))

        _logger.debug("Back plane")
        for line in back_plane:
            _logger.debug("{}".format(line))

        self.points = []
        for plane in [front_plane, back_plane]:
            # Reverse clock order
            for line in plane:
                # First, right side of line (from bottom to top)
                self.points.append(line[1].foam_print())
            for line in plane[::-1]:
                # Second, left side of plane (from top to bottom)
                self.points.append(line[0].foam_print())

        _logger.debug("Generated points:")
        _logger.debug("{}".format(self.points))
        self.points_text = "\n".join(self.points)
        print(self.points_text)

    def _check_fragmentation_restriction(self):
        mesh_elem_size_mm = self.fragmentation_config.elem_size_mm
        for line in self.x_lines:
            assert (line >= mesh_elem_size_mm)
        for line in self.y_lines:
            assert (line >= mesh_elem_size_mm)
        assert (self.mesh_config.length >= mesh_elem_size_mm)

    def _calculate_fragmentation(self):
        self._check_fragmentation_restriction()
        indexes = " ".join(map(str, range(len(self.points))))

        # x - width, y - height, z - length
        hexs = []
        amount_of_hexs = len(self.y_lines)
        _logger.debug("amount_of_hexs: {}".format(amount_of_hexs))

        front_start = 0
        front_end = len(self.x_lines) * 2 - 1
        back_start = front_end + 1
        back_end = len(self.x_lines) * 4 - 1
        _logger.debug("front_start: {}".format(front_start))
        _logger.debug("front_end: {}".format(front_end))
        _logger.debug("back_start: {}".format(back_start))
        _logger.debug("back_end: {}".format(back_end))

        for hex_i in range(amount_of_hexs):
            hexs.append("{} {} {} {} {} {} {} {}".format(
                front_start + hex_i,
                front_start + hex_i + 1,
                front_end - hex_i - 1,
                front_end - hex_i,

                back_start + hex_i,
                back_start + hex_i + 1,
                back_end - hex_i - 1,
                back_end - hex_i,
            ))

        self.fragmentation_text = ""
        for hex in hexs:
            self.fragmentation_text += "    hex ({}) ({} {} {}) simpleGrading (1.0 1.0 1.0)\n".format(
                hex,
                self.fragmentation_config.width,
                self.fragmentation_config.height,
                self.fragmentation_config.length)

        _logger.info(self.fragmentation_text)
        print(self.fragmentation_text)

    def _calculate_boundary(self):
        boundaries_text = ""
        template = Template(BOUNDARY_TEMPLATE)

        # FIXME Hardcoded for now
        amount_of_hexs = len(self.y_lines)
        assert(amount_of_hexs == 3)
        # FIXME Duplication
        front_start = 0
        front_end = len(self.x_lines) * 2 - 1
        back_start = front_end + 1
        back_end = len(self.x_lines) * 4 - 1

        name = "frontTractionEnd"
        faces = []
        for hex_i in range(amount_of_hexs):
            faces.append("\t\t\t({} {} {} {})".format(
                front_start + hex_i,
                front_start + hex_i + 1,
                front_end - hex_i - 1,
                front_end - hex_i,
            ))
        print(template.substitute(name=name, faces="\n".join(faces)))

        name = "rearFixedEnd"
        faces = []
        for hex_i in range(amount_of_hexs):
            faces.append("\t\t\t({} {} {} {})".format(
                back_start + hex_i,
                back_start + hex_i + 1,
                back_end - hex_i - 1,
                back_end - hex_i,
            ))
        #
        print(template.substitute(name=name, faces="\n".join(faces)))

        name = "topSurface"
        faces = []
        faces.append("\t\t\t({} {} {} {})".format(
            front_start + amount_of_hexs,
            back_start + amount_of_hexs,
            back_end - amount_of_hexs,
            front_end - amount_of_hexs,
        ))
        print(template.substitute(name=name, faces="\n".join(faces)))

        name = "bottomSurface"
        faces = []
        faces.append("\t\t\t({} {} {} {})".format(
            front_start,
            back_start,
            back_end,
            front_end,
        ))
        print(template.substitute(name=name, faces="\n".join(faces)))

        name = "rightSurface"
        faces = []
        for hex_i in range(amount_of_hexs):
            faces.append("\t\t\t({} {} {} {})".format(
                front_start + hex_i,
                back_start + hex_i,
                back_start + hex_i + 1,
                front_start + hex_i + 1,
            ))
        print(template.substitute(name=name, faces="\n".join(faces)))

        name = "leftSurface"
        faces = []
        for hex_i in range(amount_of_hexs):
            faces.append("\t\t\t({} {} {} {})".format(
                front_end - hex_i,
                front_end - hex_i - 1,
                back_end - hex_i - 1,
                back_end - hex_i,
            ))
        print(template.substitute(name=name, faces="\n".join(faces)))


    def _format_text(self):
        return super()._format_text()

    @staticmethod
    def _save_geometry(text, filename):
        super()._save_geometry(text, filename)

    @staticmethod
    def _generate_mesh():
        super()._generate_mesh()

    def __init__(self, mesh_config: RailMeshConfig, fragmentation_config: FragmentationConfig):
        self.mesh_config = mesh_config
        self.fragmentation_config = fragmentation_config

        self.out_file = "system/blockMeshDict"
