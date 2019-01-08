#!/usr/bin/python
# Classification (U)

"""Program:  is_valid_ext.py

    Description:  Unit testing of is_valid_ext in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/is_valid_ext.py

    Arguments:
        None

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

# Version
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Initialize testing environment.
        test_is_valid_ext_empty_set -> Test with empty ignore set.
        test_is_valid_ext_not_fnd -> Test with no find in set.
        test_is_valid_ext_fnd -> Test with one find in set.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:
                        None

                """

                self.ignore_ext = ["_kmz.64.txt", "_pptx.64.txt"]

        self.CT = CfgTest()

        self.fname = "File1_kmz.64.txt"

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_ext_empty_set(self, mock_log):

        """Function:  test_is_valid_ext_empty_set

        Description:  Test is_valid_ext function with empty ignore set.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_isse.gen_class.Logger

        """

        mock_log.return_value = True

        self.CT.ignore_ext = []

        self.assertTrue(rmq_2_isse.is_valid_ext(self.fname, self.CT, mock_log))

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_ext_not_fnd(self, mock_log):

        """Function:  test_is_valid_ext_not_fnd

        Description:  Test is_valid_ext function with not found in set.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_isse.gen_class.Logger

        """

        mock_log.return_value = True

        self.fname = "File1.txt"

        self.assertTrue(rmq_2_isse.is_valid_ext(self.fname, self.CT, mock_log))

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_ext_fnd(self, mock_log):

        """Function:  test_is_valid_ext_fnd

        Description:  Test is_valid_ext function with one find in set.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_isse.gen_class.Logger

        """

        mock_log.return_value = True

        self.assertFalse(rmq_2_isse.is_valid_ext(self.fname,
                                                 self.CT, mock_log))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:
            None

        """

        self.CT = None


if __name__ == "__main__":
    unittest.main()
