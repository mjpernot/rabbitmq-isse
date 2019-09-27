#!/usr/bin/python
# Classification (U)

"""Program:  process_list.py

    Description:  Unit testing of process_list in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/process_list.py

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
        test_is_valid_name_false -> Test with is valid name is false.
        test_is_valid_name_true -> Test with is valid name is true.
        test_file_list_empty_list -> Test with file list is an empty list.
        test_is_valid_ext_false -> Test with is valid extension is false.
        test_is_valid_ext_true -> Test with is valid extension is true.

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

                self.max_resend = 3
                self.proc_file = "files_processed"
                self.isse_dir = "/ISSE_DIR_PATH"

        self.cfg = CfgTest()
        self.line = "File1.txt"
        self.rq = "RabbitMQ Instance"
        self.file_list1 = ["File1.txt"]

    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_name_false(self, mock_log, mock_name, mock_msg):

        """Function:  test_is_valid_name_false

        Description:  Test with is valid name is false.

        Arguments:

        """

        mock_log.return_value = True
        mock_name.return_value = False
        mock_msg.return_value = True

        self.assertFalse(rmq_2_isse._process_list(self.file_list1, self.rq,
                                                  mock_log, self.cfg,
                                                  self.line))

    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_name_true(self, mock_log, mock_name, mock_msg, mock_ext):

        """Function:  test_is_valid_name_true

        Description:  Test with is valid name is true.

        Arguments:

        """

        mock_log.return_value = True
        mock_name.return_value = True
        mock_msg.return_value = True
        mock_ext.return_value = False

        self.assertFalse(rmq_2_isse._process_list(self.file_list1, self.rq,
                                                  mock_log, self.cfg,
                                                  self.line))

    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_file_list_empty_list(self, mock_log, mock_msg):

        """Function:  test_file_list_empty_list

        Description:  Test with file list is an empty list.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = True

        self.assertFalse(rmq_2_isse._process_list([], self.rq, mock_log,
                                                  self.cfg, self.line))

    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_ext_false(self, mock_log, mock_name, mock_msg, mock_ext):

        """Function:  test_is_valid_ext_false

        Description:  Test with is valid extension is false.

        Arguments:

        """

        mock_log.return_value = True
        mock_name.return_value = True
        mock_msg.return_value = True
        mock_ext.return_value = False

        self.assertFalse(rmq_2_isse._process_list(self.file_list1, self.rq,
                                                  mock_log, self.cfg,
                                                  self.line))

    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_ext_true(self, mock_log, mock_name, mock_msg, mock_ext,
                               mock_cp):

        """Function:  test_is_valid_ext_true

        Description:  Test with is valid extension is true.

        Arguments:

        """

        mock_log.return_value = True
        mock_name.return_value = True
        mock_msg.return_value = True
        mock_ext.return_value = True
        mock_cp.return_value = True

        self.assertFalse(rmq_2_isse._process_list(self.file_list1, self.rq,
                                                  mock_log, self.cfg,
                                                  self.line))


if __name__ == "__main__":
    unittest.main()
