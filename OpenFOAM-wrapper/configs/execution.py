from argparse import ArgumentParser


class ExecutionConfig:
    def __init__(self, output_dir="out/"):
        self.output_dir = output_dir
        self.execution_folder = "./"
        # self.prepare_env_script = "$HOME/openfoam/etc/bashrc"
        self.prepare_env_script = "$HOME/prog/scientific/openfoam/etc/bashrc"
        self.openfoam_folder = "/home/lenferd/prog/scientific/openfoam"

    @staticmethod
    def create_from_args(args):
        exec_conf = ExecutionConfig()
        # TODO How to avoid this duplication?
        if args.execution_output:
            exec_conf.output_dir = args.execution_output
        if args.execution_folder:
            exec_conf.execution_folder = args.execution_folder
        if args.prepare_openfoam_env_script:
            exec_conf.prepare_openfoam_env_script = args.prepare_openfoam_env_script
        if args.openfoam_folder:
            exec_conf.openfoam_folder = args.openfoam_folder
        return exec_conf


class ExecutionArguments:
    @staticmethod
    def add_execution_arguments(parser: ArgumentParser):
        parser.add_argument("-eo", "--execution_output", type=int, help="Execution output directory")
        parser.add_argument("-ef", "--execution_folder", type=str, help="Execution folder")
        parser.add_argument("-pofs", "--prepare_openfoam_env_script", type=str,
                            help="Script for preparing openfoam. Example path:$HOME/openfoam/etc/bashrc")
        parser.add_argument("-of", "--openfoam_folder", type=str, help="Folder with OpenFOAM application (core)")
