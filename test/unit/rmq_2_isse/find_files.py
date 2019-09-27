#!/usr/bin/python
# Classification (U)

"""Program:  find_files.py

    Description:  Unit testing of find_files in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/find_files.py

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
        setUp -> Initialize testing environment.
        test_find_files_current_dir -> Test finding file in current directory.
        test_find_files_past_dir -> Test finding file in past directory.
        test_find_files_2nd_past_dir -> Test finding file in 2nd directory.
        test_find_files_no_file -> Test finding no files in directories.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.transfer_dir = "transfer_dir"
                self.delta_month = 2

        self.ct = CfgTest()

        self.file_list = [self.ct.transfer_dir + "/2018/01/File"]
        self.empty_file_list = []

    @mock.patch("rmq_2_isse.os.path.join")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_find_files_current_dir(self, mock_log, mock_libs, mock_join):

        """Function:  test_find_files_current_dir

        Description:  Test find_files function for files in current directory.

        Arguments:

        """

        mock_log.return_value = True
        mock_libs.dir_file_match.side_effect = [["File"], []]
        mock_libs.month_delta.return_value = (01, 2018)
        mock_join.return_value = self.ct.transfer_dir + "/2018/01/File"

        self.assertEqual(rmq_2_isse.find_files(mock_log, self.ct, "Line"),
                         self.file_list)

    @mock.patch("rmq_2_isse.os.path.join")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_find_files_past_dir(self, mock_log, mock_libs, mock_join):

        """Function:  test_find_files_past_dir

        Description:  Test find_files function for files in past directory.

        Arguments:

        """

        mock_log.return_value = True
        mock_libs.dir_file_match.side_effect = [[], ["File"]]
        mock_libs.month_delta.return_value = (01, 2018)
        mock_join.return_value = self.ct.transfer_dir + "/2018/01/File"

        self.assertEqual(rmq_2_isse.find_files(mock_log, self.ct, "Line"),
                         self.file_list)

    @mock.patch("rmq_2_isse.os.path.join")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_find_files_2nd_past_dir(self, mock_log, mock_libs, mock_join):

        """Function:  test_find_files_2nd_past_dir

        Description:  Test find_files function for files in 2nd past directory.

        Arguments:

        """

        mock_log.return_value = True
        mock_libs.dir_file_match.side_effect = [[], [], ["File"]]
        mock_libs.month_delta.return_value = (01, 2018)
        mock_join.return_value = self.ct.transfer_dir + "/2018/01/File"

        self.assertEqual(rmq_2_isse.find_files(mock_log, self.ct, "Line"),
                         self.file_list)

    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_find_files_no_file(self, mock_log, mock_libs):

        """Function:  test_find_files_no_file

        Description:  Test find_files function for no file found.

        Arguments:

        """

        mock_log.return_value = True
        mock_libs.dir_file_match.side_effect = [[], [], []]
        mock_libs.month_delta.return_value = (01, 2018)

        self.assertEqual(rmq_2_isse.find_files(mock_log, self.ct, "Line"),
                         self.empty_file_list)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        self.ct = None


if __name__ == "__main__":
    unittest.main()
