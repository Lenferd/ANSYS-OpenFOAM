import unittest
import os
from utils import files
from mesh_generator.mesh_generator import generate_mesh


class MeshGenerator(unittest.TestCase):
    out_dir = "out"
    file_out = os.path.join(out_dir, "testBlobMesh.out")
    reference_file = "mesh_reference/foam-7-mm-reference.txt"

    def setUp(self):
        files.remove_directory(self.out_dir)
        if not files.is_directory_exists(self.out_dir):
            files.create_directory(self.out_dir)

    # def tearDown(self):
    #     files.remove_directory(self.out_dir)

    def test_generate_default_mesh(self):
        generate_mesh(1000, 100, 100, self.file_out)
        self.assertTrue(files.equal(self.file_out, self.reference_file))


if __name__ == '__main__':
    unittest.main()
