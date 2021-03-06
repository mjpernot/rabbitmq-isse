#!/usr/bin/python
# Classification (U)

"""Program:  rmq_cleanup.py

    Description:  Cleanup of RabbitMQ exchange and queues.

    Usage:
        test/blackbox/rmq_2_isse/rmq_cleanup.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import os
import sys

# Third-party
import pika

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rabbitmq_class
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def rmq_cleanup(cfg, queue_name, drop_exch=False):

    """Function:  rmq_cleanup

    Description:  Cleanup RabbitMQ exchanges and queues.

    Arguments:
        (input) cfg -> RabbitMQ configuration module handler.
        (input) queue_name -> Name of queue to drop.
        (input) drop_exch -> True|False - Drop the exchange.

    """

    rq = rabbitmq_class.RabbitMQPub(cfg.user, cfg.passwd, cfg.host, cfg.port,
                                    cfg.exchange_name, cfg.exchange_type,
                                    queue_name, queue_name, cfg.x_durable,
                                    cfg.q_durable, cfg.auto_delete)

    if isinstance(rq, rabbitmq_class.RabbitMQPub):
        connect_status, err_msg = rq.connect()

        if isinstance(rq.connection,
                      pika.adapters.blocking_connection.BlockingConnection) \
                and rq.connection._impl.connection_state > 0 \
                and connect_status:

            rq.open_channel()

            if rq.channel.is_open:
                rq.setup_exchange()

                try:
                    rq.channel.exchange_declare(exchange=rq.exchange,
                                                passive=True)
                    rq.create_queue()
                    _drop_queue(rq, drop_exch, connect_status)

                except pika.exceptions.ChannelClosed as msg:
                    print("\tWarning:  Unable to find an exchange")
                    print("Error Msg: %s" % msg)

            else:
                print("\tFailure:  Unable to open channel")
                print("\tChannel: %s" % rq.channel)

        else:
            print("\tFailure:  Unable to open connection")
            print("\tConnection: %s" % rq.connection)
            print("\tError Msg: %s" % err_msg)

    else:
        print("\tFailure:  Unable to initialize")
        print("\tClass: %s" % rabbitmq_class.RabbitMQPub)


def _drop_queue(rq, drop_exch, connect_status):

    """Function:  _drop_queue

    Description:  Private function for rmq_cleanup.

    Arguments:
        (input) rq -> RabbitMQ instance.
        (input) drop_exch -> True|False - Drop the exchange.
        (input) connect_status -> Status of RabbitMQ connection.

    """

    try:
        rq.channel.queue_declare(queue=rq.queue_name, passive=True)
        rq.clear_queue()
        rq.drop_queue()

        if drop_exch:
            rq.drop_exchange()

        rq.close_channel()

        if rq.channel.is_closed:

            if connect_status and rq.connection._impl.connection_state > 0:

                rq.close()

                if not rq.connection._impl.connection_state == 0:
                    print("\tFailed to close connection")
                    print("\tConnection: %s" % rq.connection)
                    print("\tConnection State: %s" %
                          rq.connection._impl.connection_state)

            else:
                print("\tConnection not opened")

        else:
            print("\tFailure:  Channel did not close")
            print("\tChannel: %s" % rq.channel)

    except pika.exceptions.ChannelClosed as msg:
        print("\tWarning:  Unable to locate queue")
        print("Error Msg: %s" % msg)


def main():

    """Function:  main

    Description:  Control the cleanup of RabbitMQ exchange and queues.

    Variables:
        base_dir -> Path directory to blackbox testing.
        test_path -> Full path directory to blackbox testing.
        config_path -> Path directory to configuration directory.
        cfg -> Configuration settings module for the program.

    Arguments:

    """

    base_dir = "test/blackbox/rmq_2_isse"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")

    cfg = gen_libs.load_module("rabbitmq", config_path)

    rmq_cleanup(cfg, cfg.queue_name, True)


if __name__ == "__main__":
    sys.exit(main())
