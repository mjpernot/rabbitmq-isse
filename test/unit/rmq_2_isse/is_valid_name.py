#!/usr/bin/python
# Classification (U)

"""Program:  is_valid_name.py

    Description:  Unit testing of is_valid_name in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/is_valid_name.py

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
        test_empty_list -> Test with empty list.
        test_not_found -> Test with no find in list.
        test_is_found -> Test with one find in set.
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

                self.file_filter = ["SCI-CW", "GEN-CW", "GEN-RELN"]

        self.CT = CfgTest()

        self.fname = "File_Name.txt"

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_empty_list(self, mock_log):

        """Function:  test_empty_list

        Description:  Test is_valid_name function with empty list.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_isse.gen_class.Logger

        """

        mock_log.return_value = True

        self.CT.file_filter = []

        self.assertTrue(rmq_2_isse.is_valid_name(self.fname, self.CT,
                                                 mock_log))

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_not_found(self, mock_log):

        """Function:  test_not_found

        Description:  Test is_valid_name function with not found in list.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_isse.gen_class.Logger

        """

        mock_log.return_value = True

        self.assertFalse(rmq_2_isse.is_valid_name(self.fname, self.CT,
                                                  mock_log))

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_found(self, mock_log):

        """Function:  test_is_found

        Description:  Test is_valid_name function with one find in list.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_isse.gen_class.Logger

        """

        mock_log.return_value = True

        self.fname = "File_Name_SCI-CW.txt"

        self.assertTrue(rmq_2_isse.is_valid_name(self.fname,
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
