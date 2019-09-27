#!/usr/bin/python
# Classification (U)

"""Program:  process_msg.py

    Description:  Unit testing of process_msg in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/process_msg.py

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
        test_empty_line_body -> Test an empty body argument.
        test_one_line_body -> Test with a one line body argument.
        test_one_line_multi_body -> Test one line multiple entries for body.
        test_multi_line_body -> Test with multiple line body argument.
        test_multi_line_multi_body -> Test with multi line multi body.
        test_file_search_zero -> Test with zero count on resends.
        test_file_search_one -> Test with one count on resends.
        test_file_search_equal -> Test with count equal to resends.
        test_file_search_greater -> Test with count greater than resends.
        test_valid_msg_false -> Test with valid message is false.
        test_valid_msg_true -> Test with valid message is true.
        test_file_list_empty_list -> Test with file list returns empty list.
        test_file_list_data_list -> Test with file list returns data in list.
        test_empty_line_file_list -> Test with an empty file list.
        test_one_line_file_list -> Test with one entry in file list.
        test_multi_line_file_list -> Test with multiple entries in file list.
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

        self.method = "Method Properties"
        self.body = "File1.txt"
        self.rq = "RabbitMQ Instance"

    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_name_false(self, mock_log, mock_lib, mock_valid,
                                 mock_find, mock_name, mock_msg):

        """Function:  test_is_valid_name_false

        Description:  Test with is valid name is false.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_valid.return_value = True
        mock_find.return_value = ["File1.txt"]
        mock_lib.gen_libs.write_file.return_value = True
        mock_name.return_value = False
        mock_msg.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_name_true(self, mock_log, mock_lib, mock_valid,
                                mock_find, mock_ext, mock_name):

        """Function:  test_is_valid_name_true

        Description:  Test with is valid name is true.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_valid.return_value = True
        mock_find.return_value = ["File1.txt"]
        mock_ext.return_value = True
        mock_lib.gen_libs.write_file.return_value = True
        mock_lib.gen_libs.cp_file2.return_value = True
        mock_name.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_empty_line_body(self, mock_log):

        """Function:  test_empty_line_body

        Description:  Test process_msg function with empty line body.

        Arguments:

        """

        mock_log.return_value = True

        self.body = ""

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs.file_search_cnt")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_one_line_body(self, mock_log, mock_cnt, mock_msg):

        """Function:  test_one_line_body

        Description:  Test process_msg function with an one line body.

        Arguments:

        """

        mock_log.return_value = True
        mock_cnt.return_value = self.cfg.max_resend + 1
        mock_msg.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs.file_search_cnt")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_one_line_multi_body(self, mock_log, mock_cnt, mock_msg):

        """Function:  test_one_line_multi_body

        Description:  Test process_msg function with multiple line body
            argument.

        Arguments:

        """

        mock_log.return_value = True
        mock_cnt.return_value = self.cfg.max_resend + 1
        mock_msg.return_value = True

        self.body = "File1.txt File2.txt"

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs.file_search_cnt")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_multi_line_body(self, mock_log, mock_cnt, mock_msg):

        """Function:  test_multi_line_body

        Description:  Test process_msg function with multi line body.

        Arguments:

        """

        mock_log.return_value = True
        mock_cnt.return_value = self.cfg.max_resend + 1
        mock_msg.return_value = True

        self.body = "File1.txt\nFile2.txt"

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs.file_search_cnt")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_multi_line_multi_body(self, mock_log, mock_cnt, mock_msg):

        """Function:  test_multi_line_multi_body

        Description:  Test process_msg function with multi line multi body.

        Arguments:

        """

        mock_log.return_value = True
        mock_cnt.return_value = self.cfg.max_resend + 1
        mock_msg.return_value = True

        self.body = "File1.txt\nFile2.txt File3.txt"

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_file_search_zero(self, mock_log, mock_lib, mock_msg, mock_valid):

        """Function:  test_file_search_zero

        Description:  Test process_msg function with zero count on resends.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_lib.gen_libs.write_file.return_value = True
        mock_msg.return_value = True
        mock_valid.return_value = False

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_file_search_one(self, mock_log, mock_lib, mock_msg, mock_valid):

        """Function:  test_file_search_one

        Description:  Test process_msg function with one count on resends.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 1
        mock_lib.gen_libs.write_file.return_value = True
        mock_msg.return_value = True
        mock_valid.return_value = False

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_file_search_equal(self, mock_log, mock_lib, mock_msg, mock_valid):

        """Function:  test_file_search_equal

        Description:  Test process_msg function with count equal to resends.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = self.cfg.max_resend
        mock_lib.gen_libs.write_file.return_value = True
        mock_msg.return_value = True
        mock_valid.return_value = False

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_file_search_greater(self, mock_log, mock_lib, mock_msg):

        """Function:  test_file_search_greater

        Description:  Test process_msg function with count greater than
            resends.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = self.cfg.max_resend + 1
        mock_lib.gen_libs.write_file.return_value = True
        mock_msg.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_valid_msg_false(self, mock_log, mock_lib, mock_msg, mock_valid):

        """Function:  test_valid_msg_false

        Description:  Test process_msg function with valid message is false.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_lib.gen_libs.write_file.return_value = True
        mock_msg.return_value = True
        mock_valid.return_value = False

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_valid_msg_true(self, mock_log, mock_lib, mock_msg, mock_valid,
                            mock_find):

        """Function:  test_valid_msg_true

        Description:  Test process_msg function with valid message is true.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_lib.gen_libs.write_file.return_value = True
        mock_msg.return_value = True
        mock_valid.return_value = True
        mock_find.return_value = []

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_file_list_empty_list(self, mock_log, mock_lib, mock_msg,
                                  mock_valid, mock_find):

        """Function:  test_file_list_empty_list

        Description:  Test process_msg function with file list returns empty
            list.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_lib.gen_libs.write_file.return_value = True
        mock_msg.return_value = True
        mock_valid.return_value = True
        mock_find.return_value = []

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_file_list_data_list(self, mock_log, mock_lib, mock_valid,
                                 mock_find, mock_ext, mock_name):

        """Function:  test_file_list_data_list

        Description:  Test process_msg function with file list returns data in
            list.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_valid.return_value = True
        mock_find.return_value = ["File1.txt"]
        mock_ext.return_value = False
        mock_lib.gen_libs.write_file.return_value = True
        mock_name.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.non_proc_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_empty_line_file_list(self, mock_log, mock_lib, mock_msg,
                                  mock_valid, mock_find):

        """Function:  test_empty_line_file_list

        Description:  Test process_msg function with empty file list.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_lib.gen_libs.write_file.return_value = True
        mock_msg.return_value = True
        mock_valid.return_value = True
        mock_find.return_value = []

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_one_line_file_list(self, mock_log, mock_lib, mock_valid,
                                mock_find, mock_ext, mock_name):

        """Function:  test_one_line_file_list

        Description:  Test process_msg function with one entry in file list.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_valid.return_value = True
        mock_find.return_value = ["File1.txt"]
        mock_ext.return_value = False
        mock_lib.gen_libs.write_file.return_value = True
        mock_name.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_multi_line_file_list(self, mock_log, mock_lib, mock_valid,
                                  mock_find, mock_ext, mock_name):

        """Function:  test_multi_line_file_list

        Description:  Test process_msg function with multiple entries in file
            list.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_valid.return_value = True
        mock_find.return_value = ["File1.txt", "File2.txt"]
        mock_ext.return_value = False
        mock_lib.gen_libs.write_file.return_value = True
        mock_name.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_ext_false(self, mock_log, mock_lib, mock_valid,
                                mock_find, mock_ext, mock_name):

        """Function:  test_is_valid_ext_false

        Description:  Test process_msg function with is valid extension is
            false.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_valid.return_value = True
        mock_find.return_value = ["File1.txt"]
        mock_ext.return_value = False
        mock_lib.gen_libs.write_file.return_value = True
        mock_name.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))

    @mock.patch("rmq_2_isse.is_valid_name")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.gen_libs")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_is_valid_ext_true(self, mock_log, mock_lib, mock_valid, mock_find,
                               mock_ext, mock_name):

        """Function:  test_is_valid_ext_true

        Description:  Test process_msg function with is valid extension is
            true.

        Arguments:

        """

        mock_log.return_value = True
        mock_lib.file_search_cnt.return_value = 0
        mock_valid.return_value = True
        mock_find.return_value = ["File1.txt"]
        mock_ext.return_value = True
        mock_lib.gen_libs.write_file.return_value = True
        mock_lib.gen_libs.cp_file2.return_value = True
        mock_name.return_value = True

        self.assertFalse(rmq_2_isse.process_msg(self.rq, mock_log, self.cfg,
                                                self.method, self.body))


if __name__ == "__main__":
    unittest.main()
