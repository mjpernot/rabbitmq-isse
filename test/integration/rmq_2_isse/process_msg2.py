#!/usr/bin/python
# Classification (U)

"""Program:  process_msg2.py

    Description:  Integration testing of process_msg in rmq_2_isse.py.

    Usage:
        test/integration/rmq_2_isse/process_msg2.py

    Arguments:

    NOTE:  This test is seperate from the other integration tests for the
        process_msg function due to some type of conflict.  When the
        test_write_file function is in the process_msg.py program there is
        nothing written to file and fails the test.  But when the test is
        executed by itself then the file is written to as normal.  Unable to
        resolve why this is occurring.

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
        test_write_file -> Test gen_libs.write_file with write to file.
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

        self.cfg = gen_libs.Load_Module("rabbitmq", self.config_path)

        log_path = os.path.join(self.test_path, self.cfg.log_dir)
        self.cfg.log_file = os.path.join(log_path, self.cfg.log_file)

        self.cfg.transfer_dir = os.path.join(self.test_path,
                                             self.cfg.transfer_dir)
        self.cfg.message_dir = os.path.join(self.test_path,
                                            self.cfg.message_dir)
        self.cfg.isse_dir = os.path.join(self.test_path, self.cfg.isse_dir)

        gen_libs.chk_crt_file(os.path.join(log_path, self.cfg.proc_file),
                              create=True, write=True, read=True)
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

        self.method = "Method_Properties"
        self.body = "File1.txt"

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    def test_write_file(self, mock_date, mock_mail):

        """Function:  test_write_file

        Description:  Test gen_libs.write_file with write to file.

        Arguments:

        """

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.body in open(self.cfg.proc_file).read():
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
        os.remove(self.cfg.proc_file)

        for f_name in os.listdir(self.cfg.message_dir):

            if ".gitignore" not in f_name:
                os.remove(os.path.join(self.cfg.message_dir, f_name))

        for f_name in os.listdir(self.cfg.isse_dir):

            if ".gitignore" not in f_name:
                os.remove(os.path.join(self.cfg.isse_dir, f_name))


if __name__ == "__main__":
    unittest.main()
