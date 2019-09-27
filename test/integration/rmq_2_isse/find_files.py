#!/usr/bin/python
# Classification (U)

"""Program:  find_files.py

    Description:  Integration testing of find_files in rmq_2_isse.py.

    Usage:
        test/integration/rmq_2_isse/find_files.py

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

import datetime

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import rmq_2_isse
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_current_month -> Test of gen_libs.dir_file_match current month.
        test_past_month -> Test of gen_libs.dir_file_match past month.
        test_multi_files -> Test of gen_libs.dir_file_match for multiple files.
        test_no_files -> Test of gen_libs.dir_file_match for no files found.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

        Arguments:

        """

        self.base_dir = "test/integration/rmq_2_isse"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")
        self.cfg = gen_libs.load_module("rabbitmq", self.config_path)
        log_path = os.path.join(self.test_path, self.cfg.log_dir)
        self.cfg.log_file = os.path.join(log_path, self.cfg.log_file)
        self.cfg.transfer_dir = os.path.join(self.test_path,
                                             self.cfg.transfer_dir)
        self.cfg.message_dir = os.path.join(self.test_path,
                                            self.cfg.message_dir)
        self.cfg.isse_dir = os.path.join(self.test_path, self.cfg.isse_dir)
        self.cfg.proc_file = os.path.join(log_path, self.cfg.proc_file)
        self.cfg.delta_month = 2
        self.log = gen_class.Logger(self.cfg.log_file, self.cfg.log_file,
                                    "INFO",
                                    "%(asctime)s %(levelname)s %(message)s",
                                    "%Y-%m-%dT%H:%M:%SZ")
        self.line = "File1"
        self.cur_mon_file = "File1.txt"
        self.cur_mon = "2018/01"
        self.past_mon_file = "File2.txt"
        self.past_mon = "2017/12"
        self.multi_file = ["File5.txt", "File5.zip"]
        self.multi_mon = "2017/11"

    @mock.patch("rmq_2_isse.datetime")
    def test_current_month(self, mock_date):

        """Function:  test_current_month

        Description:  Test of gen_libs.dir_file_match call for current month.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.cur_mon
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime(self.cur_mon, "%Y/%m")

        file_list = rmq_2_isse.find_files(self.log, self.cfg, self.line)
        self.log.log_close()

        if os.path.join(self.cfg.transfer_dir, self.cur_mon,
                        self.cur_mon_file) in file_list:
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.datetime")
    def test_past_month(self, mock_date):

        """Function:  test_past_month

        Description:  Test of gen_libs.dir_file_match call for past month.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.past_mon
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime(self.past_mon, "%Y/%m")

        file_list = rmq_2_isse.find_files(self.log, self.cfg, "File2")
        self.log.log_close()

        if os.path.join(self.cfg.transfer_dir, self.past_mon,
                        self.past_mon_file) in file_list:
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.datetime")
    def test_multi_files(self, mock_date):

        """Function:  test_multi_files

        Description:  Test of gen_libs.dir_file_match call for multiple files.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.multi_mon
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime(self.multi_mon, "%Y/%m")

        file_list = rmq_2_isse.find_files(self.log, self.cfg, "File5")
        self.log.log_close()
        status = True

        for x in self.multi_file:
            if not os.path.join(self.cfg.transfer_dir, self.multi_mon,
                                x) in file_list:
                status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.datetime")
    def test_no_files(self, mock_date):

        """Function:  test_no_files

        Description:  Test of gen_libs.dir_file_match call for no files found.

        Arguments:

        """

        mock_date.datetime.strftime.side_effect = [self.cur_mon, self.past_mon]
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime(self.cur_mon, "%Y/%m")

        file_list = rmq_2_isse.find_files(self.log, self.cfg, "File6")
        self.log.log_close()

        if file_list:
            status = True

        else:
            status = False

        self.assertFalse(status)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        os.remove(self.cfg.log_file)


if __name__ == "__main__":
    unittest.main()
