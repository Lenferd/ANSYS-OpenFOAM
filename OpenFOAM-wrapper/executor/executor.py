import datetime
import os
import re
import subprocess

from utils import files
from mesh_generator.simple_generator import SimpleBlockMeshConfig, FragmentationConfig
from mesh_generator.rail_generator import RailMeshConfig
from configs.execution import ExecutionConfig
from utils.logger import Logger, LogLvl

_logger = Logger(LogLvl.LOG_INFO)


class Executor:
    # openfoam_solver = "solidEquilibriumDisplacementFoamMod"
    openfoam_solver = "solidDisplacementFoamMod"

    def __init__(self, exec_conf: ExecutionConfig, mesh_conf, fragmentation_conf: FragmentationConfig):
        _logger.info("Solver: {}".format(self.openfoam_solver))
        self.exec_config = exec_conf
        self.result_dir = exec_conf.output_dir
        files.create_directory(self.result_dir)
        self.results = {}
        result_file_geom_prefix = None
        if type(mesh_conf) is SimpleBlockMeshConfig:
            result_file_geom_prefix = "gw{}_gh{}_gl{}".format(
                mesh_conf.width_mm,
                mesh_conf.height_mm,
                mesh_conf.length_mm)
            self.geom_values = "{}\t{}\t{}".format(
                mesh_conf.width_mm,
                mesh_conf.height_mm,
                mesh_conf.length_mm)
            self.geom_titles = "Geometry width\tGeometry height\tGeometry length"
        else:
            result_file_geom_prefix = ""
            self.geom_values = ""
            self.geom_titles = ""

            for line_idx in range(len(mesh_conf.width_lines)):
                result_file_geom_prefix += "w{}={}_".format(line_idx, mesh_conf.width_lines[line_idx])
                self.geom_titles += "{} {}\t".format("Width line", line_idx)
                self.geom_values += "{}\t".format(mesh_conf.width_lines[line_idx])

            for line_idx in range(len(mesh_conf.height_distance)):
                result_file_geom_prefix += "h{}={}_".format(line_idx, mesh_conf.height_distance[line_idx])
                self.geom_titles += "{} {}\t".format("Height line", line_idx)
                self.geom_values += "{}\t".format(mesh_conf.height_distance[line_idx])

            result_file_geom_prefix += "l={}".format(mesh_conf.length)
            self.geom_titles += "{}".format("Length")
            self.geom_values += "{}".format(mesh_conf.length)

        _logger.debug(result_file_geom_prefix)
        _logger.debug(self.geom_values)

        fragmentation_options_line = "fw{}_fh{}_fl{}".format(
            fragmentation_conf.width,
            fragmentation_conf.height,
            fragmentation_conf.length)
        self.fragmentation_values = "{}\t{}\t{}".format(
            fragmentation_conf.width,
            fragmentation_conf.height,
            fragmentation_conf.length)

        result_file_name = "result_{}_{}.txt".format(result_file_geom_prefix, fragmentation_options_line)
        self.result_file = os.path.join(self.result_dir, result_file_name)
        self.parsed_name = datetime.datetime.now().strftime("%Y-%m-%d-%H.txt")

    def run(self):
        _logger.info("\n\n===== Run calculation")
        self.__run_execution()
        _logger.info("===== End calculation\n\n")

        _logger.info("\n\n===== Run result parsing")
        self.__parse_output_from_file("sigmaEq")
        self.__parse_output_from_file("D")
        self.__parse_output_from_file("Time")
        _logger.info("===== End result parsing\n\n")

    def __run_execution(self):
        # FIXME no check if none
        prepare_call = "export FOAM_INST_DIR=" + self.exec_config.openfoam_folder
        prepare_call += "; "
        prepare_call += ". " + "$HOME/prog/OpenFOAM/OpenFOAM-dev/etc/bashrc_modified"
        prepare_call += "; "
        prepare_call += "cd " + self.exec_config.execution_folder
        try:
            subprocess.call(["{}; {} > {}".format(prepare_call, self.openfoam_solver, self.result_file)], shell=True)
        except OSError:
            _logger.error("{} not found.".format(self.openfoam_solver))
            _logger.error("Please make sure you are using modified version of OpenFOAM and env is prepared")

    def __parse_time(self, text):
        found_exec = re.findall(r'ExecutionTime = (\d+.?\d*) s', text)[-1]
        found_clock = re.findall(r'ClockTime = (\d+.?\d*) s', text)[-1]
        exec_time = float(found_exec)
        clock_time = float(found_clock)

        # Save result to file
        file_parsed_name = "{}-{}".format("time", self.parsed_name)
        file_parsed_result = os.path.join(self.result_dir, file_parsed_name)
        formatted_result = "{geometry}\t{fragmentation}\t{exec_time}\t{clock_time}\n".format(
            geometry=self.geom_values,
            fragmentation=self.fragmentation_values,
            exec_time=exec_time, clock_time=clock_time)

        with open(file_parsed_result, "a") as log_file:
            if os.stat(file_parsed_result).st_size == 0:
                log_file.write("{}"
                               "\tFragmentation width\tFragmentation height\tFragmentation length"
                               "\t{}\t{}\n".format(self.geom_titles, "Execution time", "Clock time"))
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

        max_value = -1.
        # FIXME Workaround for cantilever beam to use D which is with -D flag
        if param_to_parse == "sigmaEq":
            max_value = max(float_val)
        elif param_to_parse == "D":
            max_value = abs(max(float_val, key=abs))

        _logger.info("Max (Min) {}: {}".format(param_to_parse, max_value))
        # Save to map
        self.results[param_to_parse] = max_value

        # Save result to file
        file_parsed_name = "{}-{}".format(param_to_parse, self.parsed_name)
        file_parsed_result = os.path.join(self.result_dir, file_parsed_name)
        formatted_result = "{geometry}\t{fragmentation}\t{value}\n".format(geometry=self.geom_values,
                                                                           fragmentation=self.fragmentation_values,
                                                                           value=max_value)

        with open(file_parsed_result, "a") as log_file:
            if os.stat(file_parsed_result).st_size == 0:
                log_file.write("{}"
                               "\tFragmentation width\tFragmentation height\tFragmentation length"
                               "\t{}\n".format(self.geom_titles, param_to_parse))
            log_file.write(formatted_result)

    def __parse_output_from_file(self, param_to_parse):
        with open(self.result_file, 'rt') as file:
            contents = file.read()

        # TODO yeaah, custom call for "time"!
        if param_to_parse == "Time":
            self.__parse_time(contents)
        else:
            self.__parse_output(param_to_parse, contents)

    def get_results(self):
        return self.results
