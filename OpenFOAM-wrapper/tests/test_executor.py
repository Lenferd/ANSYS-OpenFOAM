from unittest import TestCase
import re


class TestExecutor(TestCase):
    def test_can_parse_time(self):
        text = "ExecutionTime = 5.73 s  ClockTime = 6 s\nExecutionTime = 6.73 s  ClockTime = 7 s"

        try:
            found = re.findall(r'ExecutionTime = (\d+.?\d*) s', text)[-1]
        except AttributeError:
            print("Pattern not found")
            found = ''
        print(found)
        self.assertEqual(6.73, float(found))
