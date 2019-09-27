#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_teardown.py

    Description:  Clean up of test file environment for blackbox testing.

    Usage:  blackbox_teardown.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import shutil

# Third-party
import glob

# Local
sys.path.append(os.getcwd())
import version

__version__ = version.__version__


def delete_test_files(base_dir, **kwargs):

    """Function:  delete_test_files

    Description:  Delete test structure for blackbox testing.

    Arguments:
        (input) base_dir -> Base directory path to testing directory.

    """

    for dir_name in [x for x in os.listdir(base_dir)
                     if os.path.isdir(os.path.join(base_dir, x))]:

        shutil.rmtree(os.path.join(base_dir, dir_name))


def main():

    """Function:  main

    Description:  Initializes program-wide variables and controls flow of
        program

    Variables:
        base_dir -> Base directory path to testing directory.

    Arguments:

    """

    base_dir = "test/blackbox/rmq_2_isse/transfer_dir"

    delete_test_files(base_dir)


if __name__ == "__main__":
    sys.exit(main())
