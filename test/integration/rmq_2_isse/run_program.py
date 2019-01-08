#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Integration testing of run_program in rmq_2_isse.py.

    Usage:
        test/integration/rmq_2_isse/run_program.py

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
import lib.gen_libs as gen_libs
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
        test_run_program -> Test of test_run_program function.
        tearDown -> Clean up of testing environment.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

        Arguments:
            None

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

        self.connect_true = "Connected to RabbitMQ node"
        self.args_array = {"-M": True, "-c": "rabbitmq", "-d": "config"}
        self.func_dict = {"-M": rmq_2_isse.monitor_queue}

    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.gen_libs.get_base_dir")
    @mock.patch("rmq_2_isse.gen_libs.load_module")
    @mock.patch("rmq_2_isse.rabbitmq_class.RabbitMQCon.consume")
    def test_run_program(self, mock_consume, mock_cfg, mock_base, mock_date):

        """Function:  test_run_program

        Description:  Test of test_run_program function.

        Arguments:
            mock_consume -> Mock Ref:  rmq_2_isse.rabbitmq_class.RabbitMQCon
            mock_cfg -> Mock Ref:  rmq_2_isse.gen_libs.load_module
            mock_base -> Mock Ref:  rmq_2_isse.gen_libs.get_base_dir
            mock_date -> Mock Ref:  rmq_2_isse.datetime

        """

        mock_consume.return_value = "RabbitMQ_Tag"
        mock_cfg.return_value = self.cfg
        mock_base.return_value = self.test_path
        mock_date.datetime.strftime.return_value = "2018-01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")

        rmq_2_isse.run_program(self.args_array, self.func_dict)

        if self.connect_true in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:
            None

        """

        os.remove(self.cfg.log_file)
        os.remove(self.cfg.proc_file)


if __name__ == "__main__":
    unittest.main()
