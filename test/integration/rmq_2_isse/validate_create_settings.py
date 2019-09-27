#!/usr/bin/python
# Classification (U)

"""Program:  validate_create_settings.py

    Description:  Integration testing of validate_create_settings in
        rmq_2_isse.py.

    Usage:
        test/integration/rmq_2_isse/validate_create_settings.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import datetime

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import rmq_2_isse
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_chk_crt_dir_true -> Test gen_libs.chk_crt_dir is true.
        test_chk_crt_file_true -> Test gen_libs.chk_crt_file is true.
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
        self.cfg.isse_dir = os.path.join(self.test_path, self.cfg.isse_dir)

        self.test_message_dir = os.path.join(self.test_path,
                                             self.cfg.message_dir)
        proc_name = self.cfg.proc_file + "_" + self.cfg.exchange_name + "_" \
            + self.cfg.queue_name + "." + "2018-01-01"
        self.test_proc_file = os.path.join(log_path, proc_name)

    @mock.patch("rmq_2_isse.gen_libs.get_base_dir")
    @mock.patch("rmq_2_isse.datetime")
    def test_chk_crt_dir_true(self, mock_date, mock_base):

        """Function:  test_chk_crt_dir_true

        Description:  Test gen_libs.chk_crt_dir is true.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = "2018-01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")
        mock_base.return_value = self.test_path

        self.cfg, status_flag = rmq_2_isse.validate_create_settings(self.cfg)

        self.assertTrue(status_flag)
        self.assertEqual(self.cfg.message_dir, self.test_message_dir)

    @mock.patch("rmq_2_isse.gen_libs.get_base_dir")
    @mock.patch("rmq_2_isse.datetime")
    def test_chk_crt_file_true(self, mock_date, mock_base):

        """Function:  test_chk_crt_file_true

        Description:  Test gen_libs.chk_crt_file is true.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = "2018-01-01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01-01", "%Y-%m-%d")
        mock_base.return_value = self.test_path

        self.cfg, status_flag = rmq_2_isse.validate_create_settings(self.cfg)

        self.assertTrue(status_flag)
        self.assertEqual(self.cfg.proc_file, self.test_proc_file)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        os.remove(self.cfg.proc_file)
        self.cfg = None


if __name__ == "__main__":
    unittest.main()
