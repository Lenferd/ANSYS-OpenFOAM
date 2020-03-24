import sys
from mesh_generator.generator import MeshGenerator
from configs.mesh import MeshConfig
from configs.fragmentation import FragmentationConfig


def parse_arguments(argv):
    print("Generator arguments:")
    print(argv)

    if len(argv) <= 3:
        print("Please provide size of mesh to generate."
              "Format: generator.py <width> <height> <length> <file_to_save>")
        exit(0)

    mesh_conf = MeshConfig()
    # TODO Specify also fragmentation
    fragmentation_conf = FragmentationConfig()

    if len(argv) > 3:
        mesh_conf.width_mm = int(argv[1])
        mesh_conf.height_mm = int(argv[2])
        mesh_conf.length_mm = int(argv[3])

    if len(argv) > 4:
        file_name = str(argv[4])
    else:
        file_name = ""

    return {"mesh_conf": mesh_conf, "fragmentation_conf": fragmentation_conf, "file_name": file_name}


if __name__ == '__main__':
    params = parse_arguments(sys.argv)
    # params = parse_arguments(["", "100", "100", "1000"])

    mesh = MeshGenerator(params.get("mesh_conf"), params.get("fragmentation_conf"))
    mesh.generate(params.get("file_name"))