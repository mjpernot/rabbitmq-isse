#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_test4.py

    Description:  Blackbox testing of rmq_2_isse.py program.

    Usage:
        test/blackbox/rmq_2_isse/blackbox_test4.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import os
import sys
import time

# Third-party

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import version

# Version
__version__ = version.__version__


def create_rq_pub(cfg, **kwargs):

    """Function:  create_rq_pub

    Description:  Create a RabbitMQ Publisher instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (output) RQ -> RabbitMQ Publisher instance
        (input) **kwargs:
            None

    """

    RQ = rabbitmq_class.RabbitMQPub(cfg.user, cfg.passwd, cfg.host, cfg.port,
                                    cfg.exchange_name, cfg.exchange_type,
                                    cfg.queue_name, cfg.queue_name,
                                    cfg.x_durable, cfg.q_durable,
                                    cfg.auto_delete)

    connect_status, err_msg = RQ.create_connection()

    if connect_status and RQ.channel.is_open:
        return RQ

    else:
        print("Error:  Failed to connect to RabbitMQ as Publisher.")
        return None


def publish_and_test(RQ, f_name, **kwargs):

    """Function:  publish_and_test

    Description:  Publish a message to RabbitMQ and test to see if the file
        exists where it should be.

    Arguments:
        (input) RQ -> RabbitMQ Publisher instance
        (input) f_name ->  Full path and file name of test file.
        (input) **kwargs:
            None
        (output) status -> True|False - Success of the test.
        (output) err_msg -> Error message or None.

    """

    status = True
    err_msg = None

    if not RQ.publish_msg(os.path.splitext(os.path.basename(f_name))[0]):
        err_msg = "\tError:  Failed to publish message to RabbitMQ."
        status = False

    time.sleep(1)

    if status and not os.path.isfile(f_name):
        err_msg = "\tError:  %s is not present" % (f_name)
        status = False

    else:
        os.remove(f_name)

    return status, err_msg


def test_1(RQ, isse_path, **kwargs):

    """Function:  test_1

    Description:  Test:  Process message for restart of service.

    Arguments:
        (input) RQ -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.
        (input) **kwargs:
            None

    """

    print("    Test:  Process message for restart of service")
    f_name = "file15.zip"

    status, err_msg = publish_and_test(RQ, os.path.join(isse_path, f_name))

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def main():

    """Function:  main

    Description:  Control the blackbox testing of rmq_2_isse.py program.

    Variables:
        status -> True|False - If connection to RabbitMQ was created.
        base_dir -> Directory path to blackbox testing directory.
        test_path -> Current full directory path, including base_dir.
        isse_path -> Directory path to simulated ISSE Guard directory.
        config_path -> Directory path to config, including test_path.

    Arguments:
        None

    """

    base_dir = "test/blackbox/rmq_2_isse"
    test_path = os.path.join(os.getcwd(), base_dir)
    isse_path = os.path.join(test_path, "isse_dir")
    config_path = os.path.join(test_path, "config")

    cfg = gen_libs.load_module("rabbitmq", config_path)

    RQ = create_rq_pub(cfg)

    if not RQ:
        print("Error:  Failed to create RabbitMQ Publisher instance")
        status = False

    else:
        test_1(RQ, isse_path)


if __name__ == "__main__":
    sys.exit(main())
