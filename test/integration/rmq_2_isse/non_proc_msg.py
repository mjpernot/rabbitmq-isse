#!/usr/bin/python
# Classification (U)

"""Program:  non_proc_msg.py

    Description:  Integration testing of non_proc_msg in rmq_2_isse.py.

    Usage:
        test/integration/rmq_2_isse/non_proc_msg.py

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
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_write_file -> Test of gen_libs.write_file call.
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
        self.log = gen_class.Logger(self.cfg.log_file, self.cfg.log_file,
                                    "INFO",
                                    "%(asctime)s %(levelname)s %(message)s",
                                    "%Y-%m-%dT%H:%M:%SZ")
        self.rq = rabbitmq_class.RabbitMQCon(self.cfg.user, self.cfg.passwd,
                                             self.cfg.host, self.cfg.port,
                                             self.cfg.exchange_name,
                                             self.cfg.exchange_type,
                                             self.cfg.queue_name,
                                             self.cfg.queue_name,
                                             self.cfg.x_durable,
                                             self.cfg.q_durable,
                                             self.cfg.auto_delete)

        self.line = "Test_Me_File"
        self.subj = "Test_Me"
        self.test_date = "2018-01-01"
        self.test_time = "10:00:00"

        self.test_file = self.rq.exchange + "_" + self.rq.queue_name + "_" \
            + self.test_date + "_" + self.test_time + ".txt"

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.gen_libs.get_time")
    @mock.patch("rmq_2_isse.gen_libs.get_date")
    def test_write_file(self, mock_date, mock_time, mock_mail):

        """Function:  test_write_file

        Description:  Test of gen_libs.write_file call.

        Arguments:

        """

        mock_date.return_value = self.test_date
        mock_time.return_value = self.test_time
        mock_mail.send_mail.return_value = True

        rmq_2_isse.non_proc_msg(self.rq, self.log, self.cfg, self.line,
                                self.subj)

        self.log.log_close()

        if self.line in open(os.path.join(self.cfg.message_dir,
                                          self.test_file)).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        os.remove(self.cfg.log_file)
        os.remove(os.path.join(self.cfg.message_dir, self.test_file))


if __name__ == "__main__":
    unittest.main()
