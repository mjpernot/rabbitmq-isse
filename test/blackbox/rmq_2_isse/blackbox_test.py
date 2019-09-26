#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_test.py

    Description:  Blackbox testing of rmq_2_isse.py program.

    Usage:
        test/blackbox/rmq_2_isse/blackbox_test.py

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


def publish_and_test(rq, f_name, **kwargs):

    """Function:  publish_and_test

    Description:  Publish a message to RabbitMQ and test to see if the file
        exists where it should be.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) f_name ->  Full path and file name of test file.
        (output) status -> True|False - Success of the test.
        (output) err_msg -> Error message or None.

    """

    status = True
    err_msg = None

    if not rq.publish_msg(os.path.splitext(os.path.basename(f_name))[0]):
        err_msg = "\tError:  Failed to publish message to RabbitMQ."
        status = False

    time.sleep(1)

    if status and not os.path.isfile(f_name):
        err_msg = "\tError:  %s is not present" % (f_name)
        status = False

    else:
        os.remove(f_name)

    return status, err_msg


def test_1(rq, isse_path, **kwargs):

    """Function:  test_1

    Description:  Test:  Process message in the current year/month.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 1:  Process message in the current year/month")
    f_name = "file1.zip"

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_2(rq, isse_path, **kwargs):

    """Function:  test_2

    Description:  Test:  Process message in previous month.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 2:  Process message in previous month")
    f_name = "file2.zip"

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_3(rq, isse_path, **kwargs):

    """Function:  test_3

    Description:  Test:  Process message at delta limit.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 3:  Process message at delta limit")
    f_name = "file3.zip"

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_4(rq, isse_path, **kwargs):

    """Function:  test_4

    Description:  Test:  Process message outside the delta limit.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.
        (input) **kwargs:
            None

    """

    print("    Test 4:  Process message outside the delta limit")
    f_name = "file4.zip"

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print("\tThere should be an email that states file4 was not found.")
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_5(rq, isse_path, **kwargs):

    """Function:  test_5

    Description:  Test:  Process message up to max resend limit.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.
        (input) **kwargs:
            None

    """

    print("    Test 5:  Process message up to max resend limit")
    f_name = "file5.zip"

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_6(rq, isse_path, **kwargs):

    """Function:  test_6

    Description:  Test:  Process message over max resend limit.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 6:  Process message over max resend limit")
    f_name = "file6.zip"

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print(err_msg)

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if not status:
        print("\tShould be an email stating file6 has reached max resends.")
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def publish_and_test2(rq, f_list, **kwargs):

    """Function:  publish_and_test2

    Description:  Publish a message to RabbitMQ and test to see if multiple
        files exists where they should be.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) f_list ->  List of full path and file name of test files.
        (output) status -> True|False - Success of the test.
        (output) err_msg -> Error message or None.

    """

    status = True
    err_msg = None

    if not rq.publish_msg(os.path.splitext(os.path.basename(f_list[0]))[0]):
        err_msg = "\tError:  Failed to publish message to RabbitMQ."
        status = False

    time.sleep(1)

    for item in f_list:
        if status and not os.path.isfile(item):
            err_msg = "\tError:  %s is not present" % (item)
            status = False
            break

        else:
            os.remove(item)

    return status, err_msg


def test_7(rq, isse_path, **kwargs):

    """Function:  test_7

    Description:  Test:  Process multiple files for message.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 7:  Process multiple files for message")
    f_list = ["file7.zip", "file7.html"]

    for pos, item in enumerate(f_list[:]):
        f_list[pos] = os.path.join(isse_path, item)

    status, err_msg = publish_and_test2(rq, f_list)

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_8(rq, isse_path, **kwargs):

    """Function:  test_8

    Description:  Test:  Process message with excluded extension.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 8:  Process message with excluded extension")
    f_name = "file8.pptx"

    status, err_msg = publish_and_test(rq, os.path.join(isse_path, f_name))

    if status:
        if os.path.isfile(os.path.join(isse_path,
                                       os.path.basename(f_name) +
                                       "_pptx.64.txt")):
            err_msg = "\tError:  %s is present" % \
                      (os.path.basename(f_name) + "_pptx.64.txt")
            print("\tTest failed\n")

        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed")


def publish_and_test3(rq, msg_body, f_list, **kwargs):

    """Function:  publish_and_test3

    Description:  Publish a message to RabbitMQ with multiple entries on the
        same line.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) msg_body ->  Message body for RabbitMQ.
        (input) f_list ->  List of full path and file name of test files.
        (output) status -> True|False - Success of the test.
        (output) err_msg -> Error message or None.

    """

    status = True
    err_msg = None

    if not rq.publish_msg(msg_body):
        err_msg = "\tError:  Failed to publish message to RabbitMQ."
        status = False

    time.sleep(1)

    for item in f_list:
        if status and os.path.isfile(item):
            os.remove(item)

        else:
            err_msg = "\tError:  %s is not present" % (item)
            status = False
            break

    return status, err_msg


def test_9(rq, isse_path, **kwargs):

    """Function:  test_9

    Description:  Test:  Process message with multiple items - same line.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 9:  Process message with multiple items - same line")

    msg_body = "file9 file10"

    f_list = ["file9.zip", "file10.html"]

    for pos, item in enumerate(f_list[:]):
        f_list[pos] = os.path.join(isse_path, item)

    status, err_msg = publish_and_test3(rq, msg_body, f_list)

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_10(rq, isse_path, **kwargs):

    """Function:  test_10

    Description:  Test:  Process message with multiple items - multiple lines.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 10:  Process message with multiple items - multiple lines")

    msg_body = "file11\nfile12"

    f_list = ["file11.zip", "file12.html"]

    for pos, item in enumerate(f_list[:]):
        f_list[pos] = os.path.join(isse_path, item)

    status, err_msg = publish_and_test3(rq, msg_body, f_list)

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_11(rq, isse_path, **kwargs):

    """Function:  test_11

    Description:  Test:  Process message with empty body.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 11:  Process message with empty body")

    msg_body = ""

    f_list = []

    status, err_msg = publish_and_test3(rq, msg_body, f_list)

    if status:
        print("\tTest successful\n")

    else:
        print(err_msg)
        print("\tTest failed\n")


def test_12(rq, isse_path, **kwargs):

    """Function:  test_12

    Description:  Test:  Process message that is not present.

    Arguments:
        (input) rq -> RabbitMQ Publisher instance
        (input) isse_path ->  Directory path to the ISSE Guard directory.

    """

    print("    Test 12:  Process message that is not present")

    msg_body = "no_such_file"

    f_list = []

    status, err_msg = publish_and_test3(rq, msg_body, f_list)

    if status:
        print("\tShould be an email that states no_such_file was not found.")
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

    """

    base_dir = "test/blackbox/rmq_2_isse"
    test_path = os.path.join(os.getcwd(), base_dir)
    isse_path = os.path.join(test_path, "isse_dir")
    config_path = os.path.join(test_path, "config")

    cfg = gen_libs.load_module("rabbitmq", config_path)

    rq = create_rq_pub(cfg)

    if not rq:
        print("Error:  Failed to create RabbitMQ Publisher instance")

    else:
        test_1(rq, isse_path)
        test_2(rq, isse_path)
        test_3(rq, isse_path)
        test_4(rq, isse_path)
        test_5(rq, isse_path)
        test_6(rq, isse_path)
        test_7(rq, isse_path)
        test_8(rq, isse_path)
        test_9(rq, isse_path)
        test_10(rq, isse_path)
        test_11(rq, isse_path)
        test_12(rq, isse_path)


if __name__ == "__main__":
    sys.exit(main())
