#!/usr/bin/python
# Classification (U)

"""Program:  validate_create_settings.py

    Description:  Unit testing of validate_create_settings in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/validate_create_settings.py

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
import version
import lib.gen_libs as gen_libs

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_valid_values -> Test module values.
        test_return_status -> Test status return.
        test_validate_msg_path -> Test existence of message directory.
        test_validate_log_path -> Test existence of log directory.
        test_validate_proc_name -> Test existence of process file.
        test_validate_transfer_dir -> Test existence of transfer directory.
        test_validate_isse_dir -> Test existence of isse directory.

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

                self.host = "HOSTNAME"
                self.exchange_name = "rmq_2_isse_unit_test"
                self.queue_name = "rmq_2_isse_unit_test"
                self.to_line = None
                self.transfer_dir = "/TRANSFER_DIR_PATH"
                self.isse_dir = "/ISSE_DIR_PATH"
                self.delta_month = 6
                self.port = 5672
                self.exchange_type = "direct"
                self.x_durable = True
                self.q_durable = True
                self.auto_delete = False
                self.message_dir = "message_dir"
                self.log_dir = "logs"
                self.log_file = "rmq_2_isse.log"
                self.proc_file = "files_processed"
                self.ignore_ext = ["_kmz.64.txt", "_pptx.64.txt"]

        self.cfg = CfgTest()

        self.base_dir = "/BASE_DIR_PATH"
        self.err_msg = "ERROR_MESSAGE"
        self.dtg = "20190226"

    @mock.patch("rmq_2_isse.datetime.datetime")
    @mock.patch("rmq_2_isse.gen_libs")
    def test_valid_values(self, mock_lib, mock_date):

        """Function:  test_valid_values

        Description:  Test validate_create_settings function for module values.

        Arguments:

        """

        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None), (True, None)]
        mock_lib.chk_crt_file.return_value = (True, None)
        mock_date.now.return_value = "(2019, 2, 26, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg

        cfg_mod = rmq_2_isse.validate_create_settings(self.cfg)

        self.assertEqual(
            (cfg_mod[0].host, cfg_mod[0].exchange_name, cfg_mod[0].queue_name,
             cfg_mod[0].to_line, cfg_mod[0].transfer_dir, cfg_mod[0].isse_dir,
             cfg_mod[0].delta_month, cfg_mod[0].port, cfg_mod[0].exchange_type,
             cfg_mod[0].x_durable, cfg_mod[0].q_durable,
             cfg_mod[0].auto_delete, cfg_mod[0].message_dir,
             cfg_mod[0].log_dir, cfg_mod[0].log_file, cfg_mod[0].proc_file,
             cfg_mod[0].ignore_ext),
            (self.cfg.host, self.cfg.exchange_name, self.cfg.queue_name,
             self.cfg.to_line, self.cfg.transfer_dir, self.cfg.isse_dir,
             self.cfg.delta_month, self.cfg.port, self.cfg.exchange_type,
             self.cfg.x_durable, self.cfg.q_durable, self.cfg.auto_delete,
             self.cfg.message_dir, self.cfg.log_dir, self.cfg.log_file,
             self.cfg.proc_file, self.cfg.ignore_ext))

    @mock.patch("rmq_2_isse.datetime.datetime")
    @mock.patch("rmq_2_isse.gen_libs")
    def test_return_status(self, mock_lib, mock_date):

        """Function:  test_return_status

        Description:  Test validate_create_settings function for status return.

        Arguments:

        """

        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None), (True, None)]
        mock_lib.chk_crt_file.return_value = (True, None)
        mock_date.now.return_value = "(2019, 2, 26, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg

        self.assertTrue(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.datetime.datetime")
    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_msg_path(self, mock_lib, mock_date):

        """Function:  test_validate_msg_path

        Description:  Mock test validate_create_settings function for message
            directory validation.

        Arguments:

        """

        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(False, self.err_msg),
                                            (True, None), (True, None),
                                            (True, None)]
        mock_lib.chk_crt_file.return_value = (True, None)
        mock_date.now.return_value = "(2019, 2, 26, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.datetime.datetime")
    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_log_path(self, mock_lib, mock_date):

        """Function:  test_validate_log_path

        Description:  Mock test validate_create_settings function for log
            directory validation.

        Arguments:

        """

        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None),
                                            (False, self.err_msg),
                                            (True, None), (True, None)]
        mock_date.now.return_value = "(2019, 2, 26, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.datetime.datetime")
    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_proc_name(self, mock_lib, mock_date):

        """Function:  test_validate_proc_name

        Description:  Mock test validate_create_settings function for process
            file validation.

        Arguments:

        """

        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None), (True, None)]
        mock_lib.chk_crt_file.return_value = (False, self.err_msg)
        mock_date.now.return_value = "(2019, 2, 26, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.datetime.datetime")
    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_transfer_dir(self, mock_lib, mock_date):

        """Function:  test_validate_transfer_dir

        Description:  Mock test validate_create_settings function for transfer
            directory validation.

        Arguments:

        """

        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (False, self.err_msg),
                                            (True, None)]
        mock_lib.chk_crt_file.return_value = (True, None)
        mock_date.now.return_value = "(2019, 2, 26, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.datetime.datetime")
    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_isse_dir(self, mock_lib, mock_date):

        """Function:  test_validate_isse_dir

        Description:  Mock test validate_create_settings function for isse
            directory validation.

        Arguments:

        """

        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None),
                                            (False, self.err_msg)]
        mock_lib.chk_crt_file.return_value = (True, None)
        mock_date.now.return_value = "(2019, 2, 26, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])


if __name__ == "__main__":
    unittest.main()
