#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_publish.py

    Description:  Blackbox testing of rmq_2_isse.py program.

    Usage:
        test/blackbox/rmq_2_isse/blackbox_publish.py

    Arguments:

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

__version__ = version.__version__


def create_rq_pub(cfg, **kwargs):

    """Function:  create_rq_pub

    Description:  Create a RabbitMQ Publisher instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (output) rq -> RabbitMQ Publisher instance

    """

    rq = rabbitmq_class.RabbitMQPub(cfg.user, cfg.passwd, cfg.host, cfg.port,
                                    cfg.exchange_name, cfg.exchange_type,
                                    cfg.queue_name, cfg.queue_name,
                                    cfg.x_durable, cfg.q_durable,
                                    cfg.auto_delete)

    connect_status, err_msg = rq.create_connection()

    if connect_status and rq.channel.is_open:
        return rq

    else:
        print("Error:  Failed to connect to RabbitMQ as Publisher.")
        return None


def publish_message(rq, f_name, **kwargs):

    """Function:  publish_message

    Description:  Publish a message to RabbitMQ queue.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) f_name ->  File name of test file.
        (output) status -> True|False - Success of the test.
        (output) err_msg -> Error message or None.

    """

    status = True
    err_msg = None

    if not rq.publish_msg(f_name):
        err_msg = "\tError:  Failed to publish message to RabbitMQ."
        status = False

    time.sleep(1)

    return status, err_msg


def publish(RQ, **kwargs):

    """Function:  publish

    Description:  Publish test message to RabbitMQ queue.

    Arguments:
        (input) RQ -> RabbitMQ Publisher instance

    """

    f_name = "file13"

    status, err_msg = publish_message(RQ, f_name)

    if status:
        pass

    else:
        print(err_msg)
        print("\tPublish failed\n")


def main():

    """Function:  main

    Description:  Control the blackbox testing of rmq_2_isse.py program.

    Variables:
        status -> True|False - If connection to RabbitMQ was created.
        base_dir -> Directory path to blackbox testing directory.
        test_path -> Current full directory path, including base_dir.
        config_path -> Directory path to config, including test_path.

    Arguments:

    """

    base_dir = "test/blackbox/rmq_2_isse"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")

    cfg = gen_libs.load_module("rabbitmq", config_path)

    rq = create_rq_pub(cfg)

    if not rq:
        print("Error:  Failed to create RabbitMQ Publisher instance")

    else:
        publish(rq)


if __name__ == "__main__":
    sys.exit(main())
