from unittest import TestCase
from utils.logger import LogLvl, Logger


class LoggerForTests(Logger):
    def log(self, msg_log_lvl=LogLvl.LOG_INFO, message=""):
        return self._generate_message(msg_log_lvl, message)


class TestLogger(TestCase):
    logger = LoggerForTests(LogLvl.LOG_DEBUG)
    test_message = "Hello there"

    def test_can_print(self):
        log_lvl = LogLvl.LOG_INFO
        expected_message = log_lvl.to_str() + " " + self.test_message
        self.assertEqual(expected_message, self.logger.log(message=self.test_message))

    def test_not_print_log_lvl_is_lower(self):
        logger = LoggerForTests(LogLvl.LOG_ERROR)
        log_msg = logger.log(LogLvl.LOG_DEBUG, self.test_message)
        self.assertEqual(len(log_msg), 0)
