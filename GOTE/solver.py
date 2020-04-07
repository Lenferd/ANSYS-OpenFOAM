import random
from utils.logger import Logger, LogLvl
from executors import LocalExecutor, RemoteExecutor
import re

_logger = Logger(LogLvl.LOG_DEBUG)


class Solver:
    def __init__(self, left, right, start, step_size, executor):
        self.left = left
        self.right = right
        self.start = start
        self.step_size = step
        self.executor = executor

        self.previous_value = None
        self.previous_step = None

        _logger.info("Start params:")
        _logger.info("Left: {}, Right: {}, Start position: {}".format(left, right, start))

    def __parse_exec_result(self, result: str):
        if len(result) == 0:
            _logger.error("Incorrect result! : {}".format(result))

        found_result = re.findall(r'Result: (\d+.?\d*)', result)[-1]
        _logger.debug("Found result: {}".format(found_result))
        return found_result

    # def __step(self):

    def __first_step(self):
        _logger.debug("Run first step")
        result = executor.exec_command(self.start)
        start_value = self.__parse_exec_result(result)
        _logger.debug("On start value {} result: {}".format(self.start, start_value))

        first_left = self.start - self.step_size
        first_right = self.start + self.step_size
        next_val = random.randrange(first_left, first_right, step=self.step_size / 4)
        result = executor.exec_command(next_val)
        self.previous_value = self.__parse_exec_result(result)
        self.previous_step = next_val - self.start

    def step(self):
        if self.previous_value is None:
            self.__first_step()





if __name__ == '__main__':
    # executor = RemoteExecutor()
    executor = LocalExecutor(program_name="Python task.py")
    left = -10
    right = 10
    start = random.randrange(left, right)
    step = 2
    solver = Solver(left=left, right=right, start=start, step_size=step, executor=executor)
    solver.step()
