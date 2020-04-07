import paramiko
import os
import subprocess
from utils.logger import Logger, LogLvl

_logger = Logger(LogLvl.LOG_DEBUG)

class LocalExecutor:
    def __init__(self, program_name, program_path=""):
        self.program_name = program_name
        self.program_path = program_path

    def exec_command(self, command: str):
        path_to_program = os.path.join(self.program_path, self.program_name)
        full_command = "{} {}".format(path_to_program, command)
        _logger.debug("Command to execute: \"{}\"".format(full_command))

        result = subprocess.check_output(full_command, shell=True).decode(encoding="utf-8")

        _logger.debug("Result of command: {}".format(result))
        return result


class RemoteExecutor:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # VirtualBox
        self.client.connect('127.0.0.1', username='cat', password='cat', port=2222)

        stdin, stdout, stderr = self.client.exec_command('ls -la prog')
        for line in stdout:
            print('... ' + line.strip('\n'))

    def __del__(self):
        self.client.close()
