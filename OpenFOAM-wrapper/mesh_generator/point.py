class Point:
    def __repr__(self):
        return "({},{},{})".format(self.x, self.y, self.z)

    def __init__(self, x: int, y: int, z: int):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def get(self):
        return {self.x, self.y, self.z}

    def foam_print(self):
        return "({} {} {})".format(self.x, self.y, self.z)
