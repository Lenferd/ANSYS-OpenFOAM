import datetime
from runner.runner import run

# FIXME Global variables... meh
Arguments = namedtuple("Arguments", "length_mm height_mm width_mm file_name")

def parse_arguments(argv):
    parameters = Arguments
    for arg in sys.argv[1:]:
        print(arg)
    if len(argv) <= 3:
        print("Please provide size of mesh to generate."
              "Format: generator.py <width> <height> <length> <file_to_save>")
        exit(0)

    if len(argv) > 3:
        parameters.width_mm = int(argv[1])
        parameters.height_mm = int(argv[2])
        parameters.length_mm = int(argv[3])

    if len(argv) > 4:
        parameters.file_name = str(argv[4])
    else:
        parameters.file_name = 0

    return parameters


if __name__ == '__main__':
    # max w = 100, h = 100, l = 1000
    # We should iterate  over all params from 10 to 100
    w_range = list(range(20, 101, 10))
    h_range = list(range(20, 101, 10))
    l_range = [1000]

    print("\n\n\n ==== Ranges:\nw_range: {}\nh_range: {}\nl_range: {}".format(w_range, h_range, l_range))

    out_folder = "out/"
    global logfile
    logfile = datetime.datetime.now().strftime("{}%Y-%m-%d-%H-%M.out".format(out_folder))

    for l in l_range:
        for w in w_range:
            for h in h_range:
                run(w, h, l)

