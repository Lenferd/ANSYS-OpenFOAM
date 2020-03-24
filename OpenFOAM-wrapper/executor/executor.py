import datetime
import os
import re

from utils import files
from mesh_generator.generator import MeshGenerator, MeshConfig, FragmentationConfig
from configs.execution import ExecutionConfig
import subprocess
from utils.logger import Logger, LogLvl

_logger = Logger(LogLvl.LOG_INFO)


# sw = {}
# sh = {}
# sw["sigma"] = 0
# sw["D"] = 0
# sh["sigma"] = 0
# sh["D"] = 0

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
        self.parsed_name = datetime.datetime.now().strftime("%Y-%m-%d-%H.out")

    def run(self):
        _logger.info("\n\n===== Run calculation")
        # out_folder = "out/"
        # files.create_directory(out_folder)

        # generate_mesh(w, h, l, mesh_config)
        # params = "w{}_h{}_l{}".format(w, h, l)

        # length_fragmentation = mesh_config.get("length_fragmentation")
        # height_fragmentation = mesh_config.get("height_fragmentation")
        # width_fragmentation = mesh_config.get("width_fragmentation")
        # mesh_params = "sw{}_sh{}_sl{}".format(width_fragmentation, height_fragmentation, length_fragmentation)

        # filename = "{}result_{}_{}.txt".format(out_folder, params, mesh_params)

        # %Y-%m-%d %H:%M:%S
        # print(datetime.datetime.now().strftime("%H:%M:%S"))

        out_folder = "out/"
        # logfile = datetime.datetime.now().strftime("{}%Y-%m-%d-%H.out".format(out_folder))

        self.__run_execution()
        _logger.info("===== End calculation\n\n")
        # parse_output("sigma", filename, logfile+"-sigma", [w,h,l])
        # parse_output("D", filename, logfile+"-D", [w,h,l])

        _logger.info("\n\n===== Run result parsing")
        self.__parse_output_from_file("sigma")
        self.__parse_output_from_file("D")
        # parse_output_from_file("D",  self.result_file, self.parsing_result_file + "-SD",
        #                        [width_fragmentation, height_fragmentation, length_fragmentation])
        _logger.info("===== End result parsing\n\n")

    def __run_execution(self):
        os.system("solidEquilibriumDisplacementFoamMod > {}".format(self.result_file))
        # TODO refactor to throw exception
        # except OSError:
        #     print(ERROR + "solidEquilibriumDisplacementFoamMod not found."
        #                   "Please make sure you are using modified version of OpenFOAM")

    # Also parse time
    def __parse_output(self, param_to_parse, text):
        _logger.debug("Parse: {}".format(param_to_parse))

        start_index = text.rfind("Max {} = ".format(param_to_parse))
        len = text[start_index:].find('\n')

        _logger.debug(text[start_index:start_index + len])

        # All inside (58779.5 13647 74094.2 57.0585 277569 0)
        # p = re.compile('\d+\.*\d+')
        # p = re.compile(r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?')
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
        formatted_result = "{geometry}{fragmentation}{value}".format(geometry=self.mesh_values,
                                                                     fragmentation=self.fragmentation_values,
                                                                     value=max_value)

        with open(file_parsed_result, "a") as log_file:
            if os.stat(file_parsed_result).st_size == 0:
                log_file.write("Geometry width\tGeometry height\tGeometry length"
                               "\tFragmentation width\tFragmentation height\tFragmentation length"
                               "\t{}".format(param_to_parse))
            log_file.write(formatted_result)

        # w = params[0]
        # global sw
        # with open(logfile, "a") as log_file:
        #     if os.stat(logfile).st_size == 0:
        #         log_file.write("w rows, h collums, values is max {}\n".format(params_to_parse))
        #     if w != sw[params_to_parse]:  # not as prev
        #         log_file.write("\n")
        #     log_file.write("{}\t".format(max_sigma))
        #     sw[params_to_parse] = w
        # with open(logfile, "a") as log_file:
        #     if os.stat(logfile).st_size == 0:
        #         log_file.write("{}\t{}\t{}\t{}\n".format("w", "h", "l", "max_sigma"))
        #     log_file.write("{}\t{}\t{}\t{}\n".format(params[0], params[1], params[2], max_sigma))

    # FIXME Only geometry change for now
    def __parse_output_from_file(self, param_to_parse):
        with open(self.result_file, 'rt') as file:
            contents = file.read()

        self.__parse_output(param_to_parse, contents)
