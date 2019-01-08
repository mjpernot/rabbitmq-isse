#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_cleanup.py

    Description:  Clean up of log and message files in test environment for
        blackbox testing.

    Usage:  blackbox_cleanup.py

    Arguments:  None

"""

# Libraries and Global Variables

# Standard
import sys
import os

# Third-party
import glob

# Local
sys.path.append(os.getcwd())
import version

# Version
__version__ = version.__version__


def delete_log_files(base_dir, **kwargs):

    """Function:  delete_test_files

    Description:  Delete log files for blackbox testing.

    Arguments:
        (input) base_dir -> Base directory path to testing directory.

    """

    for item in glob.glob(os.path.join(base_dir, "rmq_2_isse*.log")):
        os.remove(item)

    for item in glob.glob(os.path.join(base_dir, "files_processed*")):
        os.remove(item)


def delete_msg_files(base_dir, **kwargs):

    """Function:  delete_msg_files

    Description:  Delete message files for blackbox testing.

    Arguments:
        (input) base_dir -> Base directory path to testing directory.

    """

    for item in glob.glob(os.path.join(base_dir,
                                       "blackbox-test_blackbox-test_*.txt")):
        os.remove(item)


def main():

    """Function:  main

    Description:  Controls flow of program.

    Variables:
        None

    Arguments:
        None

    """

    delete_log_files("logs")
    delete_msg_files("message_dir")


if __name__ == "__main__":
    sys.exit(main())
