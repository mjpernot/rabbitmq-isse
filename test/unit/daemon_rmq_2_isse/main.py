#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in daemon_rmq_2_isse.py.

    Usage:
        test/unit/daemon_rmq_2_isse/main.py

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
import daemon_rmq_2_isse
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        test_start_daemon -> Test main function with daemon start option.
        test_stop_daemon -> Test main function with daemon stop option.
        test_restart_daemon -> Test main function with daemon restart option.
        test_invalid_daemon -> Test main function with invalid option.
        test_arg_require_false -> Test main function with arg_require false.
        test_arg_require_true -> Test main function with arg_require true.

    """

    @mock.patch("daemon_rmq_2_isse.arg_parser")
    @mock.patch("daemon_rmq_2_isse.Rmq2IsseDaemon.start")
    def test_start_daemon(self, mock_daemon, mock_arg):

        """Function:  test_start_daemon

        Description:  Test main function with daemon start option.

        Arguments:

        """

        args = {"-a": "start", "-c": "rabbitmq"}

        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_isse.main)

    @mock.patch("daemon_rmq_2_isse.arg_parser")
    @mock.patch("daemon_rmq_2_isse.Rmq2IsseDaemon.stop")
    def test_stop_daemon(self, mock_daemon, mock_arg):

        """Function:  test_stop_daemon

        Description:  Test main function with daemon stop option.

        Arguments:

        """

        args = {"-a": "stop", "-c": "rabbitmq"}

        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_isse.main)

    @mock.patch("daemon_rmq_2_isse.arg_parser")
    @mock.patch("daemon_rmq_2_isse.Rmq2IsseDaemon.restart")
    def test_restart_daemon(self, mock_daemon, mock_arg):

        """Function:  test_restart_daemon

        Description:  Test main function with daemon restart option.

        Arguments:

        """

        args = {"-a": "restart", "-c": "rabbitmq"}

        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_isse.main)

    @mock.patch("daemon_rmq_2_isse.arg_parser")
    def test_invalid_daemon(self, mock_arg):

        """Function:  test_invalid_daemon

        Description:  Test main function with invalid option.

        Arguments:

        """

        args = {"-a": "nostart", "-c": "rabbitmq"}

        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_2_isse.main)

    @mock.patch("daemon_rmq_2_isse.arg_parser")
    @mock.patch("daemon_rmq_2_isse.Rmq2IsseDaemon.start")
    def test_arg_require_false(self, mock_daemon, mock_arg):

        """Function:  test_arg_require_false

        Description:  Test main function with arg_require false.

        Arguments:

        """

        args = {"-a": "start", "-c": "rabbitmq"}

        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = False
        mock_daemon.return_value = True

        self.assertRaises(SystemExit, daemon_rmq_2_isse.main)

    @mock.patch("daemon_rmq_2_isse.arg_parser")
    def test_arg_require_true(self, mock_arg):

        """Function:  test_arg_require_true

        Description:  Test main function with arg_require true.

        Arguments:

        """

        args = {"-a": "start", "-c": "rabbitmq"}

        mock_arg.arg_parse2.return_value = args
        mock_arg.arg_require.return_value = True

        with gen_libs.no_std_out():
            self.assertRaises(SystemExit, daemon_rmq_2_isse.main)


if __name__ == "__main__":
    unittest.main()
