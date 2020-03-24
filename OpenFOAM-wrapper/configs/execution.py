from argparse import ArgumentParser


class ExecutionConfig:
    def __init__(self, output_dir="out/"):
        self.output_dir = output_dir

    @staticmethod
    def create_from_args(args):
        exec_conf = ExecutionConfig()
        # TODO How to avoid this duplication?
        if args.execution_output:
            exec_conf.output_dir = args.execution_output
        return exec_conf


class ExecutionArguments:
    @staticmethod
    def add_execution_arguments(parser: ArgumentParser):
        parser.add_argument("-eo", "--execution_output", type=int, help="Execution output directory")
