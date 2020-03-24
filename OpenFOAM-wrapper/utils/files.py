import os
import shutil
from utils.logger import Logger, LogLvl

_logger = Logger(LogLvl.LOG_ERROR)

# Creation


def is_directory_exists(dir_name):
    directory_exists = os.path.exists(dir_name)
    if not directory_exists:
        _logger.info("Directory \"{}\" not exists".format(dir_name))
    return directory_exists


def create_directory(dir_name):
    if not is_directory_exists(dir_name):
        os.makedirs(dir_name)
        _logger.info("Creating directory {}".format(dir_name))
    return dir_name


def remove_directory(dir_name):
    if is_directory_exists(dir_name):
        shutil.rmtree(dir_name)
        _logger.info("Removing directory {}".format(dir_name))

# Query


def list_all_dirs_in_folder(folder_name):
    return os.listdir(folder_name)

# Comparators


def equal(fname1, fname2):
    # Open file for reading in text mode (default mode)
    f1 = open(fname1)
    f2 = open(fname2)

    files_equal = True

    # Print confirmation
    _logger.info("-----------------------------------")
    _logger.info("Comparing files\n > " + fname1 + "\n < " + fname2)
    _logger.info("-----------------------------------")

    # Read the first line from the files
    f1_line = f1.readline()
    f2_line = f2.readline()

    # Initialize counter for line number
    line_no = 1

    # Loop if either file1 or file2 has not reached EOF
    while f1_line != '' or f2_line != '':

        # Strip the leading whitespaces
        f1_line = f1_line.rstrip()
        f2_line = f2_line.rstrip()

        # Compare the lines from both file
        if f1_line != f2_line:

            # If a line does not exist on file2 then mark the output with
            # + sign
            if f2_line == '' and f1_line != '':
                print(">+", "Line-%d" % line_no, f1_line)
            # otherwise output the line on file1 and mark it with > sign
            elif f1_line != '':
                print(">", "Line-%d" % line_no, f1_line)

            # If a line does not exist on file1 then mark the output with
            # + sign
            if f1_line == '' and f2_line != '':
                print("<+", "Line-%d" % line_no, f2_line)

            # otherwise output the line on file2 and mark it with < sign
            elif f2_line != '':
                print("<", "Line-%d" % line_no, f2_line)

            # Print a blank line
            print()

            files_equal = False

        # Read the next line from the file
        f1_line = f1.readline()
        f2_line = f2.readline()

        # Increment line counter
        line_no += 1

    # Close the files
    f1.close()
    f2.close()

    return files_equal