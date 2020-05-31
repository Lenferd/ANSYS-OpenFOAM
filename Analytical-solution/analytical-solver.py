from argparse import ArgumentParser


def update_parser(parser: ArgumentParser):
    parser.add_argument("-len", "--length", type=float, help="Length of the model, mm", default=1000)
    parser.add_argument("-hei", "--height", type=float, help="Height of the model, mm", default=100)
    parser.add_argument("-wid", "--width", type=float, help="Width of the model, mm", default=50)
    parser.add_argument("-f", "--force", type=float, help="Force on end load, Pa", default=10000)
    parser.add_argument("-nu", "--elastic", type=float, help="Elastic modulus", default=200000)


class AnalyticBeamSolver:
    def __init__(self, args):
        self._args = args

        convert_to_m = 0.001
        self._width = args.width * convert_to_m
        self._height = args.height * convert_to_m
        self._length = args.length * convert_to_m

        self._force = args.force
        self._elastic_modulus = args.elastic

        self._max_stress = -1
        self._max_deformation = -1
        self._solve()

    def _solve(self):
        assert (self._width != -1)
        assert (self._height != -1)
        assert (self._length != -1)
        assert (self._force != -1)

        intertion_moment = (self._width * (self._height ** 3)) / 12.
        moment = self._force * self._length

        self._max_stress = moment * (self._height / 2.) / intertion_moment
        self._max_deformation = - (self._force * self._length ** 3.) / (
                3. * self._elastic_modulus * intertion_moment)

    def get_result(self):
        return {"max deformation": self._max_deformation,
                "max stress": self._max_stress}

    def print_results(self): print("max deformation {:.2e}\nmax stress {:.2e}".
                                   format(self._max_deformation, self._max_stress))


if __name__ == '__main__':
    parser = ArgumentParser()
    update_parser(parser)
    args = parser.parse_args()

    solver = AnalyticBeamSolver(args)

    solver.print_results()
