#!/usr/bin/python
# Classification (U)

"""Program:  validate_create_settings.py

    Description:  Unit testing of validate_create_settings in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/validate_create_settings.py

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

import datetime

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import rmq_2_isse
import version
import lib.gen_libs as gen_libs

# Version
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Initialize testing environment.
        test_valid_values -> Test module values.
        test_return_status -> Test status return.
        test_validate_msg_path -> Test existence of message directory.
        test_validate_log_path -> Test existence of log directory.
        test_validate_proc_name -> Test existence of process file.
        test_validate_transfer_dir -> Test existence of transfer directory.
        test_validate_isse_dir -> Test existence of isse directory.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        self.base_dir = "test/unit/rmq_2_isse"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")
        self.cfg = gen_libs.load_module("rabbitmq", self.config_path)
        self.cfg.transfer_dir = os.path.join(self.base_dir,
                                             self.cfg.transfer_dir)
        self.cfg.isse_dir = os.path.join(self.base_dir, self.cfg.isse_dir)
        self.err_msg = "Error Message"

    @mock.patch("rmq_2_isse.gen_libs")
    def test_valid_values(self, mock_lib):

        """Function:  test_valid_values

        Description:  Test validate_create_settings function for module values.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_isse.gen_libs

        """

        # This is the base module on which to test against.
        cfg = gen_libs.load_module("rabbitmq", self.config_path)
        cfg.message_dir = os.path.join(self.base_dir, cfg.message_dir)
        cfg.log_file = os.path.join(self.base_dir, cfg.log_dir, cfg.log_file)
        proc_name = cfg.proc_file + "." \
            + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m")
        cfg.proc_file = os.path.join(self.base_dir, cfg.log_dir, proc_name)

        # Set mock values.
        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None), (True, None)]
        mock_lib.chk_crt_file.return_value = (True, None)

        cfg_mod = rmq_2_isse.validate_create_settings(self.cfg)

        self.assertEqual(
            (cfg_mod[0].user, cfg_mod[0].passwd, cfg_mod[0].host,
             cfg_mod[0].exchange_name, cfg_mod[0].queue_name,
             cfg_mod[0].to_line, cfg_mod[0].transfer_dir, cfg_mod[0].isse_dir,
             cfg_mod[0].delta_month, cfg_mod[0].port, cfg_mod[0].exchange_type,
             cfg_mod[0].x_durable, cfg_mod[0].q_durable,
             cfg_mod[0].auto_delete, cfg_mod[0].message_dir,
             cfg_mod[0].log_dir, cfg_mod[0].log_file, cfg_mod[0].proc_file,
             cfg_mod[0].ignore_ext),
            (cfg.user, cfg.passwd, cfg.host, cfg.exchange_name, cfg.queue_name,
             cfg.to_line, cfg.transfer_dir, cfg.isse_dir, cfg.delta_month,
             cfg.port, cfg.exchange_type, cfg.x_durable, cfg.q_durable,
             cfg.auto_delete, cfg.message_dir, cfg.log_dir, cfg.log_file,
             cfg.proc_file, cfg.ignore_ext))

    @mock.patch("rmq_2_isse.gen_libs")
    def test_return_status(self, mock_lib):

        """Function:  test_return_status

        Description:  Test validate_create_settings function for status return.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_isse.gen_libs

        """

        # Set mock values.
        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None), (True, None)]
        mock_lib.chk_crt_file.return_value = (True, None)

        self.assertTrue(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_msg_path(self, mock_lib):

        """Function:  test_validate_msg_path

        Description:  Mock test validate_create_settings function for message
            directory validation.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_isse.gen_libs

        """

        # Set mock values.
        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(False, self.err_msg),
                                            (True, None), (True, None),
                                            (True, None)]
        mock_lib.chk_crt_file.return_value = (True, None)

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_log_path(self, mock_lib):

        """Function:  test_validate_log_path

        Description:  Mock test validate_create_settings function for log
            directory validation.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_isse.gen_libs

        """

        # Set mock values.
        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None),
                                            (False, self.err_msg),
                                            (True, None), (True, None)]

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_proc_name(self, mock_lib):

        """Function:  test_validate_proc_name

        Description:  Mock test validate_create_settings function for process
            file validation.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_isse.gen_libs

        """

        # Set mock values.
        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None), (True, None)]
        mock_lib.chk_crt_file.return_value = (False, self.err_msg)

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_transfer_dir(self, mock_lib):

        """Function:  test_validate_transfer_dir

        Description:  Mock test validate_create_settings function for transfer
            directory validation.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_isse.gen_libs

        """

        # Set mock values.
        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (False, self.err_msg),
                                            (True, None)]
        mock_lib.chk_crt_file.return_value = (True, None)

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    @mock.patch("rmq_2_isse.gen_libs")
    def test_validate_isse_dir(self, mock_lib):

        """Function:  test_validate_isse_dir

        Description:  Mock test validate_create_settings function for isse
            directory validation.

        Arguments:
            mock_lib -> Mock Ref:  rmq_2_isse.gen_libs

        """

        # Set mock values.
        mock_lib.get_base_dir.return_value = self.base_dir
        mock_lib.chk_crt_dir.side_effect = [(True, None), (True, None),
                                            (True, None),
                                            (False, self.err_msg)]
        mock_lib.chk_crt_file.return_value = (True, None)

        self.assertFalse(rmq_2_isse.validate_create_settings(self.cfg)[1])

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:
            None

        """

        del sys.modules["rabbitmq"]


if __name__ == "__main__":
    unittest.main()
