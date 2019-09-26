#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_test2.py

    Description:  Blackbox testing of rmq_2_isse.py program.

    Usage:
        test/blackbox/rmq_2_isse/blackbox_test2.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import os
import sys
import time

# Third-party

# Local
sys.path.append(os.getcwd())
import version

__version__ = version.__version__


def test_1(isse_path, **kwargs):

    """Function:  test_1

    Description:  Test:  Process message already in queue.

    Arguments:
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test:  Process message already in queue")
    f_name = "file13.zip"

    time.sleep(1)

    if not os.path.isfile(os.path.join(isse_path, f_name)):
        print("\tError:  %s is not present" % (f_name))
        print("\tTest failed\n")

    else:
        os.remove(os.path.join(isse_path, f_name))
        print("\tTest successful\n")


def main():

    """Function:  main

    Description:  Control the blackbox testing of rmq_2_isse.py program.

    Variables:
        base_dir -> Directory path to blackbox testing directory.
        test_path -> Current full directory path, including base_dir.
        isse_path -> Directory path to simulated ISSE Guard directory.

    Arguments:

    """

    base_dir = "test/blackbox/rmq_2_isse"
    test_path = os.path.join(os.getcwd(), base_dir)
    isse_path = os.path.join(test_path, "isse_dir")

    test_1(isse_path)


if __name__ == "__main__":
    sys.exit(main())
