from unittest import TestCase
from utils.logger import LogLvl, Logger


class LoggerForTests(Logger):
    def log(self, msg_log_lvl=LogLvl.LOG_INFO, message=""):
        message = self._generate_message(msg_log_lvl, message)
        return message


class TestLogger(TestCase):
    logger = LoggerForTests(LogLvl.LOG_DEBUG)
    test_message = "Hello there"

    def test_can_print(self):
        expected_message = LogLvl.LOG_INFO.to_str() + self.test_message
        self.assertEqual(expected_message, self.logger.log(message=self.test_message))

    def test_not_print_log_lvl_is_lower(self):
        logger = LoggerForTests(LogLvl.LOG_ERROR)
        log_msg = logger.log(LogLvl.LOG_DEBUG, self.test_message)
        self.assertEqual(len(log_msg), 0)

    def test_add_header_when_newline(self):
        message = "Test\nTest"
        expected_message = LogLvl.LOG_INFO.to_str() + "Test" + "\n" + LogLvl.LOG_INFO.to_str() + "Test"
        log_msg = self.logger.log(LogLvl.LOG_INFO, message)
        self.assertEqual(expected_message, log_msg)

    def test_list_to_log(self):
        a_list = ["123", "32"]
        log_msg = self.logger.log(message=a_list)
        self.assertNotEqual(-1, log_msg.find(a_list[0]))
        self.assertNotEqual(-1, log_msg.find(a_list[1]))
