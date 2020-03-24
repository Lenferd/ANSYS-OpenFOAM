import sys
from mesh_generator.generator import MeshGenerator
from configs.mesh import MeshConfig
from configs.fragmentation import FragmentationConfig
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-gw", "--geom_width", type=int, help="Geometry object width in mm")
    parser.add_argument("-gh", "--geom_height", type=int, help="Geometry object height in mm")
    parser.add_argument("-gl", "--geom_length", type=int, help="Geometry object length in mm")

    parser.add_argument("-fw", "--fragmentation_width", type=int, help="Fragmentation on width axes (X)")
    parser.add_argument("-fh", "--fragmentation_height", type=int, help="Fragmentation on height axes (Y)")
    parser.add_argument("-fl", "--fragmentation_length", type=int, help="Fragmentation on length axes (Z)")

    parser.add_argument("-o", "--output_file", type=str, help="Save mesh description to specified file")
    args = parser.parse_args()

    mesh_conf = MeshConfig()
    # TODO How to avoid this duplication?
    if args.geom_width:
        mesh_conf.width_mm = args.geom_width
    if args.geom_height:
        mesh_conf.height_mm = args.geom_height
    if args.geom_length:
        mesh_conf.length_mm = args.geom_length

    fragmentation_conf = FragmentationConfig()
    if args.fragmentation_width:
        fragmentation_conf.width = args.fragmentation_width
    if args.fragmentation_height:
        fragmentation_conf.height = args.fragmentation_height
    if args.fragmentation_length:
        fragmentation_conf.length = args.fragmentation_length

    mesh = MeshGenerator(mesh_conf, fragmentation_conf)
    mesh.generate(args.output_file)
