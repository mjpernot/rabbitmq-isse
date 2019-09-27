#!/usr/bin/python
# Classification (U)

"""Program:  callback.py

    Description:  Unit testing of callback in rmq_2_isse.py.

    Usage:
        test/unit/rmq_2_isse/callback.py

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
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_callback -> Test callback function.
        tearDown -> Clean up of testing environment.

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

                pass

        self.ct = CfgTest()

    @mock.patch("rmq_2_isse.rabbitmq_class.RabbitMQCon.ack")
    @mock.patch("rmq_2_isse.process_msg")
    @mock.patch("rmq_2_isse.monitor_queue")
    @mock.patch("rmq_2_isse.gen_class.Logger")
    def test_callback(self, mock_log, mock_monitor, mock_msg, mock_ack):

        """Function:  test_callback

        Description:  Test callback function.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = True
        mock_monitor.return_value.callback.return_value = True
        mock_ack.return_value = True

        self.assertTrue(rmq_2_isse.monitor_queue(self.ct, mock_log).
                        callback("Channel", "Method", "Props", "Body"))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        self.ct = None


if __name__ == "__main__":
    unittest.main()
