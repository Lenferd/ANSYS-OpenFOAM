from string import Template
import sys
from mesh_generator.mesh_template import MESH_FILE_TEMPLATE


def calculate_points(width_mm, height_mm, length_mm):
    # TODO add check, that convertToMeters is 0.001 (m to mm)
    print("length_mm {}, height_mm {}, width_mm {}".format(length_mm, height_mm, width_mm))
    p1 = [0, 0, 0]
    p2 = [length_mm, 0, 0]
    p3 = [length_mm, height_mm, 0]
    p4 = [0, height_mm, 0]
    p5 = [0, 0, width_mm]
    p6 = [length_mm, 0, width_mm]
    p7 = [length_mm, height_mm, width_mm]
    p8 = [0, height_mm, width_mm]

    arr = [p1, p2, p3, p4, p5, p6, p7, p8]
    string = ""
    for i in range(len(arr)):
        # string += "    ({} {} {})\t\t// p{}".format(arr[i][0], arr[i][1], arr[i][2], i)
        string += "    ({} {} {})".format(arr[i][0], arr[i][1], arr[i][2])
        if i + 1 != len(arr):
            string += "\n"

        # print(string)
    return string


def calculate_fragmentation(width_mm, height_mm, length_mm, mesh_elem_size_mm):
    assert(width_mm >= mesh_elem_size_mm)
    assert(height_mm >= mesh_elem_size_mm)
    assert(length_mm >= mesh_elem_size_mm)
    # length_fragmentation = int(float(length_mm) / mesh_elem_size_mm)
    # height_fragmentation = int(float(height_mm) / mesh_elem_size_mm)
    # width_fragmentation = int(float(width_mm) / mesh_elem_size_mm)
    # TODO try to use 6 2 1 (default in tutorial)
    length_fragmentation = 5
    height_fragmentation = 2
    width_fragmentation = 2
    print("length_fragmentation {}, height_fragmentation {}, width_fragmentation {}".format(length_fragmentation,
                                                                                            height_fragmentation,
                                                                                            width_fragmentation))

    string = "    hex (0 1 2 3 4 5 6 7) ({} {} {}) simpleGrading (1.0 1.0 1.0)".format(
        length_fragmentation, height_fragmentation, width_fragmentation)
    return string


def format_text(points, fragmentation):
    t = Template(MESH_FILE_TEMPLATE)
    return t.substitute(points=points, fragmentation=fragmentation)


def generate_mesh(length, width, height, filename):
    print("w: {}, h: {}, l: {}, filename: {}".format(width, height, length, filename))
    # FIXME Temporary recast
    w = width
    l = length
    h = height
    points = calculate_points(w, h, l)
    fragmentation = calculate_fragmentation(w, h, l, 20)
    text = format_text(points, fragmentation)
    # print(text.format(points))
    if filename != 0:
        f = open(filename, "w+")
        f.writelines(text)
        f.close()
    else:
        print(text)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print(arg)

    w = 10
    h = 10
    l = 100

    if len(sys.argv) > 3:
        w = int(sys.argv[1])
        h = int(sys.argv[2])
        l = int(sys.argv[3])

    if len(sys.argv) > 4:
        filename = str(sys.argv[4])
    else:
        filename = 0

    # w = 100
    # h = 100
    # l = 1000

    print("hello there")
    print("General Kenobi")
    generate_mesh(l, w, h, filename)



