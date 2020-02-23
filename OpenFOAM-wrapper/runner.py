import os
import re
import datetime

from utils import files

def check_params(params):
    if len(params) != 2:
        print("Incorrect parameters for one folder: {}".format(params))
        print("Pattern should be {width}-{height}")
        exit(-1)


def wrap_str_to_quotes(str):
    return '\'' + str + '\''


def generate_mesh(w, h, l):
    os.system('pwd')
    os.system("python mesh_generator.py {} {} {} system/blockMeshDict".format(w, h, l))
    print("\n\n\n ===== Run block mesh generating")
    os.system('blockMesh')


def run_execution(filename):
    os.system("solidEquilibriumDisplacementFoamMod > {}".format(filename))


sw = {}
sh = {}
sw["sigma"] = 0
sw["D"] = 0
sh["sigma"] = 0
sh["D"] = 0


def parse_output(paramToParse, filename, logfile, params):
    with open(filename, 'rt') as file:
        contents = file.read()
    # print(contents)
    # print(type(contents))
    start_index = contents.rfind("Max {} = ".format(paramToParse))
    len = contents[start_index:].find('\n')
    # print(contents[start_index:start_index + len])

    # All inside (58779.5 13647 74094.2 57.0585 277569 0)
    p = re.compile('\d+\.*\d+')
    values = p.findall(contents[start_index:start_index + len])
    float_val = []

    for val in values:
        float_val.append(float(val))
    # print(float_val)
    max_sigma = max(float_val)
    print("\n\n === Max {}: {}".format(paramToParse, max_sigma))

    w = params[0]
    global sw
    with open(logfile, "a") as log_file:
        if os.stat(logfile).st_size == 0:
            log_file.write("w rows, h collums, values is max {}\n".format(paramToParse))
        if w != sw[paramToParse]:   # not as prev
            log_file.write("\n")
        log_file.write("{}\t".format(max_sigma))
        sw[paramToParse] = w
    # with open(logfile, "a") as log_file:
    #     if os.stat(logfile).st_size == 0:
    #         log_file.write("{}\t{}\t{}\t{}\n".format("w", "h", "l", "max_sigma"))
    #     log_file.write("{}\t{}\t{}\t{}\n".format(params[0], params[1], params[2], max_sigma))


logfile = ""
def run(w, h, l):
    out_folder = "out/"
    files.create_directory(out_folder)
    print("\n\n\n ==== Ranges:\nw_range: {}\nh_range: {}\nl_range: {}".format(w_range, h_range, l_range))
    generate_mesh(w, h, l)
    params = "w{}_h{}_l{}".format(w, h, l)
    filename = "{}result_{}.txt".format(out_folder, params)

    # %Y-%m-%d %H:%M:%S
    # print(datetime.datetime.now().strftime("%H:%M:%S"))

    run_execution(filename)
    parse_output("sigma", filename, logfile+"-sigma", [w,h,l])
    parse_output("D", filename, logfile+"-D", [w,h,l])


if __name__ == '__main__':
    # max w = 100, h = 100, l = 1000
    # We should iterate  over all params from 10 to 100
    w_range = list(range(20, 101, 10))
    h_range = list(range(20, 101, 10))
    l_range = [1000]

    out_folder = "out/"
    global logfile
    logfile = datetime.datetime.now().strftime("{}%Y-%m-%d-%H-%M.out".format(out_folder))

    for l in l_range:
        for w in w_range:
            for h in h_range:
                run(w, h, l)


