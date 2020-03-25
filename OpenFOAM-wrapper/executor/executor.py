import datetime
import os
import re

from utils import files
from mesh_generator.generator import MeshGenerator, MeshConfig, FragmentationConfig
from configs.execution import ExecutionConfig
from utils.logger import Logger, LogLvl

_logger = Logger(LogLvl.LOG_INFO)


class Executor:
    def __init__(self, exec_conf: ExecutionConfig, mesh_conf: MeshConfig, fragmentation_conf: FragmentationConfig):
        self.result_dir = exec_conf.output_dir
        files.create_directory(self.result_dir)

        mesh_options_line = "gw{}_gh{}_gl{}".format(
            mesh_conf.width_mm,
            mesh_conf.height_mm,
            mesh_conf.length_mm)
        self.mesh_values = "{}\t{}\t{}".format(
            mesh_conf.width_mm,
            mesh_conf.height_mm,
            mesh_conf.length_mm)

        fragmentation_options_line = "fw{}_fh{}_fl{}".format(
            fragmentation_conf.width,
            fragmentation_conf.height,
            fragmentation_conf.length)
        self.fragmentation_values = "{}\t{}\t{}".format(
            fragmentation_conf.width,
            fragmentation_conf.height,
            fragmentation_conf.length)

        self.result_file = "{}result_{}_{}.txt".format(self.result_dir, mesh_options_line, fragmentation_options_line)
        self.parsed_name = datetime.datetime.now().strftime("%Y-%m-%d-%H.txt")

    def run(self):
        _logger.info("\n\n===== Run calculation")
        self.__run_execution()
        _logger.info("===== End calculation\n\n")

        _logger.info("\n\n===== Run result parsing")
        self.__parse_output_from_file("sigma")
        self.__parse_output_from_file("D")
        self.__parse_output_from_file("Time")
        _logger.info("===== End result parsing\n\n")

    def __run_execution(self):
        os.system("solidDisplacementFoamMod > {}".format(self.result_file))
        # TODO refactor to throw exception
        # except OSError:
        #     print(ERROR + "solidEquilibriumDisplacementFoamMod not found."
        #                   "Please make sure you are using modified version of OpenFOAM")

    def __parse_time(self, text):
        found_exec = re.findall(r'ExecutionTime = (\d+.?\d*) s', text)[-1]
        found_clock = re.findall(r'ClockTime = (\d+.?\d*) s', text)[-1]
        exec_time = float(found_exec)
        clock_time = float(found_clock)

        # Save result to file
        file_parsed_result = "{}{}-{}".format(self.result_dir, "time", self.parsed_name)
        formatted_result = "{geometry}\t{fragmentation}\t{exec_time}\t{clock_time}\n".format(
            geometry=self.mesh_values,
            fragmentation=self.fragmentation_values,
            exec_time=exec_time, clock_time=clock_time)

        with open(file_parsed_result, "a") as log_file:
            if os.stat(file_parsed_result).st_size == 0:
                log_file.write("Geometry width\tGeometry height\tGeometry length"
                               "\tFragmentation width\tFragmentation height\tFragmentation length"
                               "\t{}\t{}\n".format("Execution time", "Clock time"))
            log_file.write(formatted_result)

    def __parse_output(self, param_to_parse, text):
        _logger.debug("Parse: {}".format(param_to_parse))

        start_index = text.rfind("Max {} = ".format(param_to_parse))
        len = text[start_index:].find('\n')

        _logger.debug(text[start_index:start_index + len])

        # (.123 250000 1.00009e+06 160325 7.29635e-10 2.36271e+06 0 -2.40131e-45 5.12455e-06 2.01673e-06 1.18136e-05)
        p = re.compile(r'[-+]?[0-9]*\.?[0-9]+[eE]?[-+]?[0-9]*')
        values = p.findall(text[start_index:start_index + len])

        _logger.debug("Found values: {}".format(values))

        float_val = []
        for val in values:
            float_val.append(float(val))

        _logger.debug("Values as float: {}".format(float_val))

        max_value = max(float_val, key=abs)
        _logger.info("Max (Min) {}: {}".format(param_to_parse, max_value))

        # Save result to file
        file_parsed_result = "{}{}-{}".format(self.result_dir, param_to_parse, self.parsed_name)
        formatted_result = "{geometry}\t{fragmentation}\t{value}\n".format(geometry=self.mesh_values,
                                                                           fragmentation=self.fragmentation_values,
                                                                           value=max_value)

        with open(file_parsed_result, "a") as log_file:
            if os.stat(file_parsed_result).st_size == 0:
                log_file.write("Geometry width\tGeometry height\tGeometry length"
                               "\tFragmentation width\tFragmentation height\tFragmentation length"
                               "\t{}\n".format(param_to_parse))
            log_file.write(formatted_result)

    def __parse_output_from_file(self, param_to_parse):
        with open(self.result_file, 'rt') as file:
            contents = file.read()

        # TODO yeaah, custom call for "time"!
        if param_to_parse == "Time":
            self.__parse_time(contents)
        else:
            self.__parse_output(param_to_parse, contents)
