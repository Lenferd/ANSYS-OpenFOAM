import datetime
import sys
from collections import namedtuple
from runner.runner import run

# FIXME Global variables... meh
Arguments = namedtuple("Arguments", "length_mm height_mm width_mm")


def help_msg():
    print("Please provide size of mesh to generate."
          "Format: run_foam_single.py <width> <height> <length>")
    exit(0)


def parse_arguments(argv):
    parameters = Arguments
    for arg in sys.argv[1:]:
        print(arg)
    if len(argv) < 3:
        help_msg()

    if len(argv) == 3:
        parameters.width_mm = int(argv[1])
        parameters.height_mm = int(argv[2])
        parameters.length_mm = int(argv[3])
    else:
        help_msg()

    return parameters


if __name__ == '__main__':
    # arguments = parse_arguments(sys.argv)
    arguments = Arguments(1000, 100, 100)

    out_folder = "out/"
    global logfile
    logfile = datetime.datetime.now().strftime("{}%Y-%m-%d-%H-%M.out".format(out_folder))

    run(arguments.width_mm, arguments.height_mm, arguments.length_mm)

