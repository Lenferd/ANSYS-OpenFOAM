import os
from string import Template

from mesh_generator.point import Point
from mesh_generator.simple_generator import SimpleBlockMeshGenerator
from mesh_generator.template import BOUNDARY_TEMPLATE, MESH_FILE_TEMPLATE
from configs.mesh import RailMeshConfig
from configs.fragmentation import FragmentationConfig
from configs.execution import ExecutionConfig
from utils.logger import Logger, LogLvl

_logger = Logger(LogLvl.LOG_DEBUG)
MIDDLE_LINE_ALGO = "middle_line"
LEFT_LINE_ALGO = "left_line"


class RailMeshGenerator(SimpleBlockMeshGenerator):
    def create(self, custom_out_file=None):
        super().create(custom_out_file)

    def _print_configuration(self):
        _logger.info("Generate mesh with size:")
        _logger.info("Width lines:")
        _logger.info(self.mesh_config.width_lines)
        _logger.info("Height distances:")
        _logger.info(self.mesh_config.height_distance)
        _logger.info("Length: {}\n".format(self.mesh_config.length))

        _logger.log(LogLvl.LOG_INFO, "Generate mesh with fragmentation:")
        _logger.log(LogLvl.LOG_INFO,
                    "{:>10}{:>10}{:>10}\n".format(
                        "width: " + str(self.fragmentation_config.width),
                        "height: " + str(self.fragmentation_config.height),
                        "length: " + str(self.fragmentation_config.length)))

    # TODO This implementation contains workaround, as it's use two lines width as value of two points
    def __left_line_points_calc(self):
        length = self.mesh_config.length
        front_plane = []
        back_plane = []

        if len(self.x_lines) % 2 != 0:
            raise Exception("Unable to use left line points generator, if amount of points % 2 != 0")

        it = 0
        it_y = 0
        # Need two create front and back plane (based on 4 point).
        # Step is 2, as we are using different lines width as first point coordinate + width
        while it < len(self.x_lines):
            # Here we are creating line for plane
            front_plane.append([Point(self.x_lines[it], sum(self.y_lines[0:it_y]), 0),
                                Point(self.x_lines[it] + self.x_lines[it + 1], sum(self.y_lines[0:it_y]), 0)])
            back_plane.append([Point(self.x_lines[it], sum(self.y_lines[0:it_y]), length),
                               Point(self.x_lines[it] + self.x_lines[it + 1], sum(self.y_lines[0:it_y]), length)])
            it += 2
            it_y += 1

        _logger.debug("Front plane")
        for line in front_plane:
            _logger.debug("{}".format(line))

        _logger.debug("Back plane")
        for line in back_plane:
            _logger.debug("{}".format(line))

        # Should it also be rewritten?
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
        # print(self.points_text)

    def __middle_line_points_calc(self):
        length = self.mesh_config.length

        middle_line_x = max(self.x_lines) / 2
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
        # print(self.points_text)

    def _calculate_points(self):
        # TODO add check, that convertToMeters is 0.001
        self.x_lines = self.mesh_config.width_lines
        self.y_lines = self.mesh_config.height_distance

        # OpenFOAM support working with float values of points, so %2 this restriction is not necessary

        if (len(self.x_lines) - 2) / 2 == len(self.y_lines):
            self.calc_algorithm = LEFT_LINE_ALGO
            print("[WARNING] Left line mesh generating algorithm")
        else:
            self.calc_algorithm = MIDDLE_LINE_ALGO

        if self.calc_algorithm == MIDDLE_LINE_ALGO:
            self.__middle_line_points_calc()
        if self.calc_algorithm == LEFT_LINE_ALGO:
            self.__left_line_points_calc()

    def _check_fragmentation_restriction(self):
        mesh_elem_size_mm = self.fragmentation_config.elem_size_mm
        for line in self.x_lines:
            assert (line >= mesh_elem_size_mm)
        for line in self.y_lines:
            assert (line >= mesh_elem_size_mm)
        assert (self.mesh_config.length >= mesh_elem_size_mm)

    def _calculate_fragmentation(self):
        # FIXME Some check also should exist for left line algorithm
        if self.calc_algorithm == MIDDLE_LINE_ALGO:
            self._check_fragmentation_restriction()

        indexes = " ".join(map(str, range(len(self.points))))

        # x - width, y - height, z - length
        hexs = []
        amount_of_hexs = len(self.y_lines)
        _logger.debug("amount_of_hexs: {}".format(amount_of_hexs))

        front_start = 0
        front_end = len(self.x_lines) * 2 - 1

        if self.calc_algorithm == LEFT_LINE_ALGO:
            front_end = len(self.x_lines) - 1

        back_start = front_end + 1
        back_end = len(self.x_lines) * 4 - 1

        if self.calc_algorithm == LEFT_LINE_ALGO:
            back_end = len(self.x_lines) * 2 - 1

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
        # print(self.fragmentation_text)

    def _calculate_boundary(self):
        self.boundaries_text = ""
        template = Template(BOUNDARY_TEMPLATE)

        amount_of_hexs = len(self.y_lines)

        # FIXME Duplication
        front_start = 0
        front_end = len(self.x_lines) * 2 - 1

        if self.calc_algorithm == LEFT_LINE_ALGO:
            front_end = len(self.x_lines) - 1

        back_start = front_end + 1
        back_end = len(self.x_lines) * 4 - 1

        if self.calc_algorithm == LEFT_LINE_ALGO:
            back_end = len(self.x_lines) * 2 - 1

        name = "frontTractionEnd"
        faces = []
        for hex_i in range(amount_of_hexs):
            faces.append("\t\t\t({} {} {} {})".format(
                front_start + hex_i,
                front_start + hex_i + 1,
                front_end - hex_i - 1,
                front_end - hex_i,
            ))
        self.boundaries_text += template.substitute(name=name, faces="\n".join(faces))
        self.boundaries_text += "\n\n"

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
        self.boundaries_text += template.substitute(name=name, faces="\n".join(faces))
        self.boundaries_text += "\n\n"

        name = "topSurface"
        faces = []
        faces.append("\t\t\t({} {} {} {})".format(
            front_start + amount_of_hexs,
            back_start + amount_of_hexs,
            back_end - amount_of_hexs,
            front_end - amount_of_hexs,
        ))
        self.boundaries_text += template.substitute(name=name, faces="\n".join(faces))
        self.boundaries_text += "\n\n"

        name = "bottomSurface"
        faces = []
        faces.append("\t\t\t({} {} {} {})".format(
            front_start,
            back_start,
            back_end,
            front_end,
        ))
        self.boundaries_text += template.substitute(name=name, faces="\n".join(faces))
        self.boundaries_text += "\n\n"

        name = "rightSurface"
        faces = []
        for hex_i in range(amount_of_hexs):
            faces.append("\t\t\t({} {} {} {})".format(
                front_start + hex_i,
                back_start + hex_i,
                back_start + hex_i + 1,
                front_start + hex_i + 1,
            ))
        self.boundaries_text += template.substitute(name=name, faces="\n".join(faces))
        self.boundaries_text += "\n\n"

        name = "leftSurface"
        faces = []
        for hex_i in range(amount_of_hexs):
            faces.append("\t\t\t({} {} {} {})".format(
                front_end - hex_i,
                front_end - hex_i - 1,
                back_end - hex_i - 1,
                back_end - hex_i,
            ))
        self.boundaries_text += template.substitute(name=name, faces="\n".join(faces))
        self.boundaries_text += "\n"

    def _format_text(self):
        t = Template(MESH_FILE_TEMPLATE)
        return t.substitute(points=self.points_text, fragmentation=self.fragmentation_text,
                            boundary=self.boundaries_text)

    @staticmethod
    def _save_geometry(text, filename):
        super().save_geometry(text, filename)

    @staticmethod
    def _generate_mesh():
        super().generate_mesh()

    def __init__(self, mesh_config: RailMeshConfig, fragmentation_config: FragmentationConfig,
                 exec_config: ExecutionConfig = ExecutionConfig()):
        self.mesh_config = mesh_config
        self.fragmentation_config = fragmentation_config
        self.exec_config = exec_config

        self.out_file = "system/blockMeshDict"
        if self.exec_config is not None:
            self.out_file = os.path.join(self.exec_config.execution_folder, self.out_file)
