import unittest
import os
from utils import files
from mesh_generator.simple_generator import SimpleBlockMeshGenerator
from configs.mesh import SimpleBlockMeshConfig
from configs.fragmentation import FragmentationConfig


class MeshGeneratorTests(unittest.TestCase):
    out_dir = "out"
    file_out = os.path.join(out_dir, "testBlobMesh.out")
    reference_file = "mesh_reference/foam-7-mm-reference.txt"
    width_mm = 100
    height_mm = 100
    length_mm = 1000

    def setUp(self):
        files.remove_directory(self.out_dir)
        if not files.is_directory_exists(self.out_dir):
            files.create_directory(self.out_dir)

    def tearDown(self):
        files.remove_directory(self.out_dir)

    def test_generate_default_mesh(self):
        mesh_conf = SimpleBlockMeshConfig(self.width_mm, self.height_mm, self.length_mm)
        fragmentation_conf = FragmentationConfig()
        mesh = SimpleBlockMeshGenerator(mesh_conf, fragmentation_conf)
        mesh.create(self.file_out)
        self.assertTrue(files.equal(self.file_out, self.reference_file))


if __name__ == '__main__':
    unittest.main()
