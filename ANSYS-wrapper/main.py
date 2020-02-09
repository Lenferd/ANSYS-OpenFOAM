import os

def is_directory_exists(dir_name):
    directory_exists = os.path.exists(dir_name)
    if not directory_exists:
        print("Directory {} not exists".format(dir_name))
    return directory_exists


def create_directory(dir_name):
    if not is_directory_exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def list_all_dirs_in_folder(folder_name):
    return os.listdir(folder_name)


def check_params(params):
    if len(params) != 2:
        print("Incorrect parameters for one folder: {}".format(params))
        print("Pattern should be {width}-{height}")
        exit(-1)


def wrap_str_to_quotes(str):
    return '\'' + str + '\''


class AnsysParsers:
    @staticmethod
    def parse_parameters_for_solver(dir_with_parameters):
        subdirs = list_all_dirs_in_folder(dir_with_parameters)
        print(subdirs)
        parameters_for_solver = []
        for folder in subdirs:
            params = folder.split('-')[1:]
            check_params(params)
            trash_subfolders = 'SYS/MECH'
            path_to_folder = '/'.join([dir_with_parameters, folder, trash_subfolders])
            parameters_for_solver.append({path_to_folder: params})
        return parameters_for_solver


class AnsysExecObject:
    commandToExecute = "ansys195.exe\n"

    def set_input_file(self, folder, name='ds'):
        file_format = wrap_str_to_quotes('dat')
        if not is_directory_exists(folder):
            exit(-2)
        full_pat = os.path.abspath(folder)
        full_pat = wrap_str_to_quotes(full_pat)
        self.commandToExecute +=\
            "/INPUT,'{file_name}',{file_format},{folder_with_input},0"\
            .format(file_name=name, file_format=file_format, folder_with_input=full_pat)

    def print_command(self):
        print(self.commandToExecute)


def prepare_apdl_solution(solution_parameter, output_directory):
    execution_obj = AnsysExecObject()
    for path_to_file, params in solution_parameter.items():
        if not is_directory_exists(path_to_file):
            exit(-3)
        dir_name = create_directory(output_directory + "/" + "-".join(params))
        print(path_to_file)
        execution_obj.set_input_file(path_to_file)

    return execution_obj


def run_apdl_solution(apdl_obj):
    apdl_obj.print_command()


if __name__ == '__main__':
    inputDirectory = "input"
    outputDirectory = "output"

    create_directory(outputDirectory)
    if not (is_directory_exists(inputDirectory)):
        print("Input directory not found!")
        exit(-1)

    # Parse directories in this dir: format ansys-{width}-{height}
    solutionParameters = AnsysParsers.parse_parameters_for_solver(inputDirectory)
    print(solutionParameters)

    # Run ansys apdl with inputs
    executors = []
    for solutionParameter in solutionParameters:
        executors.append(prepare_apdl_solution(solutionParameter, outputDirectory))

    for executor in executors:
        run_apdl_solution(executor)
