from enum import IntEnum


class LogLvl(IntEnum):
    LOG_ERROR = 0
    LOG_INFO = 1
    LOG_DEBUG = 2

    def to_str(self):
        return "[" + self.name + "]"


class Logger:
    def __init__(self, log_lvl):
        self.log_lvl = LogLvl.LOG_INFO

    def log(self, msg_log_lvl=LogLvl.LOG_INFO, message=""):
        print(self._generate_message(msg_log_lvl, message))

    def _generate_message(self, msg_log_lvl=LogLvl.LOG_INFO, message=""):
        if self.log_lvl >= msg_log_lvl:
            return "{header} {body}".format(header=msg_log_lvl.to_str(), body=message)
        else:
            return ""
