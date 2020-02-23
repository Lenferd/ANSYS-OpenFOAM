import sys
from mesh_generator.generator import parse_arguments, generate_mesh, Arguments

if __name__ == '__main__':
    params = parse_arguments(sys.argv)
    # params = Arguments(100, 100, 100, "example")

    print("Hello there")
    print("General Kenobi")
    # TODO Use always this struct for input?
    generate_mesh(params.length_mm, params.width_mm, params.height_mm, params.file_name)
