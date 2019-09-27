#!/usr/bin/python
# Classification (U)

"""Program:  process_msg.py

    Description:  Integration testing of process_msg in rmq_2_isse.py.

    Usage:
        test/integration/rmq_2_isse/process_msg.py

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
        test_file_search_cnt_true -> Test of gen_libs.file_search_cnt call.
        test_non_proc_msg -> Test of non_proc_msg function call.
        test_is_valid_msg_true -> Test is_valid_msg function with a valid
            message body.
        test_is_valid_msg_false -> Test non_proc_msg function call with false
            from is_valid_msg.
        test_find_files_zero -> Test find_files function with no files found.
        test_find_files_one -> Test find_files function with one file found.
        test_fine_files_past -> Test find_files function with one file found in
            past history directory.
        test_find_files_past2 -> Test find_files function with no file found in
            past history directory.
        test_is_valid_ext_true -> Test is_valid_ext function with a valid
            extension.
        test_is_valid_ext_false -> Test is_valid_ext function with an invalid
            extension.
        test_cp_file2 -> Test gen_libs.cp_file2 function with valid file.
        test_max_resend -> Test test_max_resend with reading from file.
        test_is_valid_name_false -> Test is_valid_name function with invalid
            file name.
        test_is_valid_name_true -> Test is_valid_name function with valid
            file name.
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
        self.file_search_cnt_true = "to tracking file:"
        self.non_proc_msg = "Reached max resends"
        self.is_valid_msg_true = "Looking for files"
        self.is_valid_msg_false = "Invalid message format"
        self.find_files_zero = "File not found"
        self.find_files_one = "Processing file:"
        self.valid_ext_true = "File1.txt to ISSE directory"
        self.valid_ext_false = "File extension invalid for:"
        self.valid_name_true = "File1_SCI-CW.txt to ISSE directory"
        self.valid_name_false = "File does not meet file criteria"

    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.is_valid_msg")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_file_search_cnt_true(self, mock_write, mock_copy, mock_valid,
                                  mock_find, mock_ext):

        """Function:  test_file_search_cnt_true

        Description:  Test of gen_libs.file_search_cnt call.

        Arguments:

        """

        mock_write.return_value = True
        mock_copy.return_value = True
        mock_valid.return_value = True
        mock_find.return_value = ["File1.txt"]
        mock_ext.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.file_search_cnt_true in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    def test_non_proc_msg(self, mock_mail):

        """Function:  test_non_proc_msg

        Description:  Test of non_proc_msg function call.

        Arguments:

        """

        mock_mail.send_mail.return_value = True

        self.cfg.max_resend = -1

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.non_proc_msg in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.find_files")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_is_valid_msg_true(self, mock_write, mock_copy, mock_find,
                               mock_ext):

        """Function:  test_is_valid_msg_true

        Description:  Test is_valid_msg function with a valid message body.

        Arguments:

        """

        mock_find.return_value = ["File1.txt"]
        mock_ext.return_value = True
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.is_valid_msg_true in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.is_valid_msg")
    def test_is_valid_msg_false(self, mock_valid, mock_mail):

        """Function:  test_is_valid_msg_false

        Description:  Test non_proc_msg function call with false from
            is_valid_msg.

        Arguments:

        """

        mock_valid.return_value = False
        mock_mail.send_mail.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.is_valid_msg_false in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_find_files_zero(self, mock_write, mock_copy, mock_ext, mock_date,
                             mock_mail):

        """Function:  test_find_files_zero

        Description:  Test find_files function with no files found.

        Arguments:

        """

        self.body = "File1a.txt"
        self.cfg.delta_month = 0

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_ext.return_value = True
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.find_files_zero in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_find_files_one(self, mock_write, mock_copy, mock_ext, mock_date,
                            mock_mail):

        """Function:  test_find_files_zero

        Description:  Test find_files function with one file found.

        Arguments:

        """

        self.body = "File1.txt"
        self.cfg.delta_month = 0

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_ext.return_value = True
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.find_files_one in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_find_files_past(self, mock_write, mock_copy, mock_ext, mock_date,
                             mock_mail):

        """Function:  test_find_files_past

        Description:  Test find_files function with one file found in past
            history directory.

        Arguments:

        """

        self.body = "File2.txt"
        self.cfg.delta_month = 1

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")
        mock_ext.return_value = True
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.find_files_one in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.is_valid_ext")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_find_files_past2(self, mock_write, mock_copy, mock_ext, mock_date,
                              mock_mail):

        """Function:  test_find_files_past

        Description:  Test find_files function with no file found in past
            history directory.

        Arguments:

        """

        self.body = "File3.txt"
        self.cfg.delta_month = 1

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")
        mock_ext.return_value = True
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.find_files_zero in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_is_valid_ext_true(self, mock_write, mock_copy, mock_date,
                               mock_mail):

        """Function:  test_is_valid_ext_true

        Description:  Test is_valid_ext function with a valid extension.

        Arguments:

        """

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.valid_ext_true in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_is_valid_ext_false(self, mock_write, mock_copy, mock_date,
                                mock_mail):

        """Function:  test_is_valid_ext_true

        Description:  Test is_valid_ext function with an invalid extension.

        Arguments:

        """

        self.body = "File4_pptx.64.txt"

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.valid_ext_false in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_cp_file2(self, mock_write, mock_date, mock_mail):

        """Function:  test_cp_file2

        Description:  Test gen_libs.cp_file2 function with valid file.

        Arguments:

        """

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")
        mock_write.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.valid_ext_true in open(self.cfg.log_file).read() \
           and os.path.isfile(os.path.join(self.cfg.isse_dir, self.body)):
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    def test_max_resend(self, mock_date, mock_mail):

        """Function:  test_max_resend

        Description:  Test test_max_resend with reading from file.

        Arguments:

        """

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")

        for x in range(0, 6):
            gen_libs.write_file(self.cfg.proc_file, data=self.body)

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.non_proc_msg in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_is_valid_name_false(self, mock_write, mock_copy, mock_date,
                                 mock_mail):

        """Function:  test_is_valid_name_false

        Description:  Test is_valid_name function with an invalid file name.

        Arguments:

        """

        self.cfg.file_filter = ["SCI-CW", "GEN-CW", "GEN-RELN"]

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.valid_name_false in open(self.cfg.log_file).read():
            status = True

        else:
            status = False

        self.assertTrue(status)

    @mock.patch("rmq_2_isse.gen_class.Mail")
    @mock.patch("rmq_2_isse.datetime")
    @mock.patch("rmq_2_isse.gen_libs.cp_file2")
    @mock.patch("rmq_2_isse.gen_libs.write_file")
    def test_is_valid_name_true(self, mock_write, mock_copy, mock_date,
                                mock_mail):

        """Function:  test_is_valid_name_true

        Description:  Test is_valid_name function with an valid file name.

        Arguments:

        """

        self.cfg.file_filter = ["SCI-CW", "GEN-CW", "GEN-RELN"]
        self.body = "File1_SCI-CW.txt"

        mock_mail.send_mail.return_value = True
        mock_date.datetime.strftime.return_value = "2018/01"
        mock_date.datetime.now.return_value = \
            datetime.datetime.strptime("2018-01", "%Y-%m")
        mock_write.return_value = True
        mock_copy.return_value = True

        rmq_2_isse.process_msg(self.rq, self.log, self.cfg, self.method,
                               self.body)

        self.log.log_close()

        if self.valid_name_true in open(self.cfg.log_file).read():
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
