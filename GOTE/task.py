from argparse import ArgumentParser
from utils.logger import Logger, LogLvl
import matplotlib.pyplot as plt
import numpy as np

_logger = Logger(LogLvl.LOG_DEBUG)


class Task:
    @staticmethod
    def function(x):
        y = x ** 2
        _logger.debug("Value of y: {}".format(y))
        return y

    @staticmethod
    def _function_name():
        return "y = x ** 2"

    @staticmethod
    def restriction_1(x):
        y = -((x + 1) ** 2) + 100
        return y

    @staticmethod
    def _restriction_name():
        return "y = -((x + 1) ** 2) + 100"

    #
    # def restriction_2(self):

    def plot(self):
        # create 1000 equally spaced points between -10 and 10
        x = np.linspace(-10, 10, 1000)

        y = self.function(x)
        restriction_y = self.restriction_1(x)

        fig, ax = plt.subplots()
        ax.plot(x, y, label="function {}".format(self._function_name()))
        ax.plot(x, restriction_y, label="restriction {}".format(self._restriction_name()), color="red")
        plt.legend()
        plt.grid()
        plt.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("x", type=float, help="x argument")
    parser.add_argument("-v", "--view_plot", type=bool, help="show plot of task")
    args = parser.parse_args()

    task = Task()
    task.function(x=args.x)
    if args.view_plot:
        task.plot()
