#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/run_program.py

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
import lib.gen_libs as gen_libs
import version

# Version
__version__ = version.__version__


def monitor_queue(cfg, LOG, **kwargs):

    """Function Stub:  monitor_queue

    Description:  This is a function stub for rmq_2_isse.monitor_queue

    Arguments:
        cfg -> Stub argument holder.
        LOG -> Stub argument holder.

    """

    pass


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Initialize testing environment.
        test_func_call_one -> Test function with call to one function.
        test_func_call_none -> Test function with call to no functions.
        test_status_false -> Test with status is False.
        test_status_true -> Test with status is True.
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

                self.host = "SERVER_NAME"
                self.exchange_name = "EXCHANGE_NAME"
                self.queue_name = "QUEUE_NAME"
                self.log_file = "LOG_FILE"
                self.to_line = "TO_LINE"
                self.transfer_dir = "TRANSFER_DIR"
                self.isse_dir = "ISSE_DIR"
                self.delta_month = 3
                self.max_resend = 5
                self.file_filter = []

        self.CT = CfgTest()

        self.args = {"-c": "config_file", "-d": "config_dir", "-M": True}
        self.func_dict = {"-M": monitor_queue}

    @mock.patch("rmq_2_isse.validate_create_settings")
    @mock.patch("rmq_2_isse.gen_libs.load_module")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    @mock.patch("rmq_2_isse.gen_class.ProgramLock")
    def test_exception_handler(self, mock_lock, mock_log, mock_load,
                               mock_valid):

        """Function:  test_exception_handler

        Description:  Test with exception handler.

        Arguments:

        """

        mock_lock.side_effect = rmq_2_isse.gen_class.SingleInstanceException
        mock_log.return_value = rmq_2_isse.gen_class.Logger
        mock_load = self.CT
        mock_valid.return_value = (self.CT, True)
        mock_log.log_close.return_value = True
        mock_log = rmq_2_isse.gen_class.ProgramLock

        with gen_libs.no_std_out():
            self.assertFalse(rmq_2_isse.main())

    @mock.patch("rmq_2_isse.monitor_queue")
    @mock.patch("rmq_2_isse.validate_create_settings")
    @mock.patch("rmq_2_isse.gen_libs.load_module")
    @mock.patch("rmq_2_isse.gen_class")
    def test_func_call_one(self, mock_class, mock_load, mock_valid, mock_func):

        """Function:  test_func_call

        Description:  Test run_program function with call to one function.

        Arguments:
            mock_class -> Mock Ref:  rmq_2_isse.gen_class
            mock_load -> Mock Ref:  rmq_2_isse.gen_libs.load_module
            mock_valid -> Mock Ref:  rmq_2_isse.validate_create_settings
            mock_func -> Mock Ref:  rmq_2_isse.monitor_queue

        """

        mock_class.Logger.return_value = rmq_2_isse.gen_class.Logger
        mock_load = self.CT
        mock_valid.return_value = (self.CT, True)
        mock_class.Logger.log_close.return_value = True
        mock_class.ProgramLock = rmq_2_isse.gen_class.ProgramLock
        mock_func.return_value = True

        self.assertFalse(rmq_2_isse.run_program(self.args, self.func_dict))

    @mock.patch("rmq_2_isse.monitor_queue")
    @mock.patch("rmq_2_isse.validate_create_settings")
    @mock.patch("rmq_2_isse.gen_libs.load_module")
    @mock.patch("rmq_2_isse.gen_class")
    def test_func_call_none(self, mock_class, mock_load, mock_valid,
                            mock_func):

        """Function:  test_func_call_none

        Description:  Test run_program function with call to no functions.

        Arguments:
            mock_class -> Mock Ref:  rmq_2_isse.gen_class
            mock_load -> Mock Ref:  rmq_2_isse.gen_libs.load_module
            mock_valid -> Mock Ref:  rmq_2_isse.validate_create_settings
            mock_func -> Mock Ref:  rmq_2_isse.monitor_queue

        """

        mock_class.Logger.return_value = rmq_2_isse.gen_class.Logger
        mock_load = self.CT
        mock_valid.return_value = (self.CT, True)
        mock_class.Logger.log_close.return_value = True
        mock_class.ProgramLock = rmq_2_isse.gen_class.ProgramLock
        mock_func.return_value = True

        self.assertFalse(rmq_2_isse.run_program(self.args, {}))

    @mock.patch("rmq_2_isse.validate_create_settings")
    @mock.patch("rmq_2_isse.gen_libs.load_module")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_status_false(self, mock_log, mock_load, mock_valid):

        """Function:  test_status_false

        Description:  Test run_program function with status is False.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_isse.gen_class.Logger
            mock_load -> Mock Ref:  rmq_2_isse.gen_libs.load_module
            mock_valid -> Mock Ref:  rmq_2_isse.validate_create_settings

        """

        # Set mock value for all returns.
        mock_log.return_value = True
        mock_load = self.CT
        mock_valid.return_value = (self.CT, False)

        with gen_libs.no_std_out():
            self.assertFalse(rmq_2_isse.run_program(self.args, self.func_dict))

    @mock.patch("rmq_2_isse.validate_create_settings")
    @mock.patch("rmq_2_isse.gen_libs.load_module")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_status_true(self, mock_log, mock_load, mock_valid):

        """Function:  test_status_true

        Description:  Test run_program function with status is True.

        Arguments:
            mock_log -> Mock Ref:  rmq_2_isse.gen_class.Logger
            mock_load -> Mock Ref:  rmq_2_isse.gen_libs.load_module
            mock_valid -> Mock Ref:  rmq_2_isse.validate_create_settings

        """

        # Set mock value for all returns.
        mock_log.return_value = rmq_2_isse.gen_class.Logger
        mock_load = self.CT
        mock_valid.return_value = (self.CT, True)
        mock_log.log_close.return_value = True

        # Remove to skip "for" loop.
        self.args.pop("-M")

        self.assertFalse(rmq_2_isse.run_program(self.args, self.func_dict))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:
            None

        """

        self.CT = None


if __name__ == "__main__":
    unittest.main()
