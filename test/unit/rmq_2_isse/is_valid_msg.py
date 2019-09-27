#!/usr/bin/python
# Classification (U)

"""Program:  is_valid_msg.py

    Description:  Unit testing of is_valid_msg in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/is_valid_msg.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import rmq_2_isse
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        test_valid_line -> Test a valid line.
        test_empty_line -> Test for empty line.
        test_multiple_entries -> Test for multiple entries in line.

    """

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_valid_line(self, mock_log):

        """Function:  test_valid_line

        Description:  Test is_valid_msg function for one entry in line.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(rmq_2_isse.is_valid_msg("One", mock_log))

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_empty_line(self, mock_log):

        """Function:  test_empty_line

        Description:  Test is_valid_msg function for empty line.

        Arguments:

        """

        mock_log.return_value = True

        self.assertFalse(rmq_2_isse.is_valid_msg("", mock_log))

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_multiple_entries(self, mock_log):

        """Function:  test_multiple_entries

        Description:  Test is_valid_msg function for multiple entries in line.

        Arguments:

        """

        mock_log.return_value = True

        self.assertFalse(rmq_2_isse.is_valid_msg("One Two", mock_log))


if __name__ == "__main__":
    unittest.main()
