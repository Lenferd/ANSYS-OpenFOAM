from enum import IntEnum


class LogLvl(IntEnum):
    LOG_ERROR = 0
    LOG_INFO = 1
    LOG_DEBUG = 2

    def to_str(self):
        return "[" + self.name + "] "


class Logger:
    def __init__(self, log_lvl=LogLvl.LOG_INFO):
        self.log_lvl = log_lvl

    def log(self, msg_log_lvl=LogLvl.LOG_INFO, message=""):
        generated_msg = self._generate_message(msg_log_lvl, message)
        if len(generated_msg):
            print(generated_msg)

    def error(self, message):
        self.log(LogLvl.LOG_ERROR, message)

    def info(self, message):
        self.log(LogLvl.LOG_INFO, message)

    def debug(self, message):
        self.log(LogLvl.LOG_DEBUG, message)

    def _generate_message(self, msg_log_lvl=LogLvl.LOG_INFO, message=""):
        if self.log_lvl >= msg_log_lvl:
            message = message.replace('\n', '\n' + msg_log_lvl.to_str())
            return "{header}{body}".format(header=msg_log_lvl.to_str(), body=message)
        else:
            return ""

    def set_level(self, log_lvl):
        self.log_lvl = log_lvl
