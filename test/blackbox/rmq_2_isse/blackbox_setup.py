#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_setup.py

    Description:  Setup test enviornment for blackbox testing.

    Usage:  blackbox_setup.py

    Arguments:  None

"""

# Libraries and Global Variables

# Standard
import sys
import os
import datetime

# Third-party

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs
import version

# Version
__version__ = version.__version__


def create_test_files(base_dir, files, **kwargs):

    """Function:  create_test_files

    Description:  Create test files for blackbox testing.

    Arguments:
        (input) base_dir -> Base directory path to testing directory.
        (input) files -> List of list of files to create in sub-directories.

    """

    for delta in range(0, 4):
        month, year = gen_libs.month_delta(datetime.datetime.now(), delta * -1)
        month = "%02d" % (month)
        crt_dir = os.path.join(base_dir, str(year) + "/" + str(month))
        gen_libs.chk_crt_dir(crt_dir, create=True)

        for f_name in files[delta]:
            gen_libs.chk_crt_file(os.path.join(crt_dir, f_name), create=True)


def main():

    """Function:  main

    Description:  Initializes program-wide variables and controls flow of
        program

    Variables:
        base_dir -> Base directory path to testing directory.

    Arguments:
        None

    """

    base_dir = "test/blackbox/rmq_2_isse/transfer_dir"
    files = [["file1.zip", "file5.zip", "file6.zip", "file7.zip", "file7.html",
              "file8.pptx", "file8_pptx.64.txt", "file15.zip", "file16.zip",
              "file17.zip", "file18_SCI-CW.zip"],
             ["file2.zip", "file9.zip", "file10.html", "file13.zip"],
             ["file3.zip", "file11.zip", "file12.html", "file14.zip"],
             ["file4.zip"]]

    create_test_files(base_dir, files)


if __name__ == "__main__":
    sys.exit(main())
