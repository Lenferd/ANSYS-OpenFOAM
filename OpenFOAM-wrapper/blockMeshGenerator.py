from string import Template
import sys


def calculate_points(width_mm, height_mm, length_mm):
    # Calculate in meters for OpenFOAM
    length_m = length_mm / 1000.
    height_m = height_mm / 1000.
    width_m = width_mm / 1000.

    print("length_m {}, height_m {}, width_m {}".format(length_m, height_m, width_m))
    p1 = [0, 0, 0]
    p2 = [length_m, 0, 0]
    p3 = [length_m, height_m, 0]
    p4 = [0, height_m, 0]
    p5 = [0, 0, width_m]
    p6 = [length_m, 0, width_m]
    p7 = [length_m, height_m, width_m]
    p8 = [0, height_m, width_m]

    arr = [p1, p2, p3, p4, p5, p6, p7, p8]
    string = ""
    for i in range(len(arr)):
        string += "    ({} {} {})\t\t// p{}\n".format(arr[i][0], arr[i][1], arr[i][2], i)
        # print(string)
    return string


def calculate_fragmentation(width_mm, height_mm, length_mm, mesh_elem_size_mm):
    assert(width_mm >= mesh_elem_size_mm)
    assert(height_mm >= mesh_elem_size_mm)
    assert(length_mm >= mesh_elem_size_mm)
    # length_fragmentation = int(float(length_mm) / mesh_elem_size_mm)
    # height_fragmentation = int(float(height_mm) / mesh_elem_size_mm)
    # width_fragmentation = int(float(width_mm) / mesh_elem_size_mm)
    length_fragmentation = 5
    height_fragmentation = 2
    width_fragmentation = 2
    print("length_fragmentation {}, height_fragmentation {}, width_fragmentation {}".format(length_fragmentation,
                                                                                            height_fragmentation,
                                                                                            width_fragmentation))

    string = "    hex (0 1 2 3 4 5 6 7) ({} {} {}) simpleGrading (1.0 1.0 1.0)\n".format(
        length_fragmentation, height_fragmentation, width_fragmentation)
    return string


def format_text(points, fragmentation):
    t = Template("""\
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  v1906                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

scale   1;

vertices
(

$points

);

blocks
(
$fragmentation
);

edges
(
);

boundary
(
    topSurface
    {
        type patch;
        faces
        (
            (3 7 6 2)
        );
    }

    bottomSurface
    {
        type patch;
        faces
        (
            (4 0 1 5)
        );
    }

    fixedEnd
    {
        type patch;
        faces
        (
            (0 4 7 3)
        );
    }

    tractionEnd
    {
        type patch;
        faces
        (
            (1 2 6 5)
        );
    }
);

mergePatchPairs
(
);

// ************************************************************************* //
""")
    return t.substitute(points=points, fragmentation=fragmentation)


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
    print("w: {}, h: {}, l: {}, filename: {}".format(w, h, l, filename))
    print("hello there")
    print("General Kenobi")
    points = calculate_points(w, h, l)
    fragmentation = calculate_fragmentation(w, h, l, 20)
    text = format_text(points, fragmentation)
    # print(text.format(points))
    if filename != 0:
        f = open(filename, "w+")
        f.writelines(text)
    else:
        print(text)


