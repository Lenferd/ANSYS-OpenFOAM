
class FragmentationConfig:
    elem_size_mm = 20

    def __init__(self, width_fragmentation=2, height_fragmentation=2, length_fragmentation=5):
        self.width = width_fragmentation
        self.height = height_fragmentation
        self.length = length_fragmentation
