#!/usr/bin/python
# Classification (U)

"""Program:  rmq_2_isse.py

    Description:  Process a RabbitMQ message, locate the document referenced
        in the message and copy the document to the ISSE review directory.

    Usage:
        rmq_2_isse.py -c file -d path/config [-M] [-v | -h]

    Arguments:
        -M => Monitor and process messages from a RabbitMQ queue.
        -c file => RabbitMQ configuration file.  Required argument.
        -d dir path => Directory path for option '-c'.  Required argument.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.

    Notes:
        The option to monitor the RabbitMQ is setup to run in an infinite loop
        and can only be killed with a CTRL-C on the command line or shutdown of
        the service.

        The configuration file below is required to run this program.  Create
        them and replace those variables (i.e. <VARIABLE>) with a value.

        Configuration file format (rabbitmq.py).  The configuration file format
        is for the initial environment setup for the program.

            # RabbitMQ Configuration file
            # Classification (U)
            # Unclassified until filled.
            user = "USER"
            passwd = "PASSWORD"
            host = "HOSTNAME"
            # RabbitMQ Exchange name being monitored.
            exchange_name = "EXCHANGE_NAME"
            # RabbitMQ Queue name being monitored.
            queue_name = "QUEUE_NAME"
            # Email address(es) to send non-processed messages to or None.
            # None state no emails are required to be sent.
            to_line = "EMAIL_ADDRESS@DOMAIN_NAME"
            # Base path and transfer directory for searching.
            transfer_dir = "BASE_PATH/SEARCH_DIR"
            # Base path and ISSE review directory.
            isse_dir = "BASE_PATH/ISSE_DIR"
            # File search criteria.
            # Filename must contain one of the strings in list to be processed.
            # Example:  file_filter = ["SCI-CW", "GEN-CW", "GEN-RELN"]
            # NOTE: If list is empty, all files will be processed.
            file_filter = []
            # Number of months to search in the past.
            # 0 (zero) means only search current month.
            delta_month = 6
            # RabbitMQ listening port, default is 5672.
            port = 5672
            # Type of exchange:  direct, topic, fanout, headers
            exchange_type = "direct"
            # Is exchange durable: True|False
            x_durable = True
            # Are queues durable: True|False
            q_durable = True
            # Queues automatically delete message after processing: True|False
            auto_delete = False
            # Archive directory name for non-processed messages.
            message_dir = "message_dir"
            # Directory name for log files.
            log_dir = "logs"
            # File name to program log.
            log_file = "rmq_2_isse.log"
            # File name to processed file log.
            proc_file = "files_processed"
            # Do not transfer the base64 file, only the original file.
            # Extensions must match what is in isse_guard_class.Isse_Guard.
            ignore_ext = ["_kmz.64.txt", "_pptx.64.txt"]

    Example:
        rmq_2_isse.py -c rabbitmq -d config -M

"""

# Libraries and Global Variables

# Standard
import sys
import os
import datetime
import socket
import getpass

# Third-party

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import version

__version__ = version.__version__


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def validate_create_settings(cfg, **kwargs):

    """Function:  validate_create_settings

    Description:  Validate the configuration settings and creation of certain
        settings.

    Arguments:
        (input) cfg -> Configuration module name.
        (output) cfg -> Configuration module handler.
        (output) status_flag -> True|False - successfully validation/creation.

    """

    status_flag = True
    base_dir = gen_libs.get_base_dir(__file__)
    msg_path = os.path.join(base_dir, cfg.message_dir)
    log_path = os.path.join(base_dir, cfg.log_dir)
    proc_name = cfg.proc_file + "_" + cfg.exchange_name + "_" \
        + cfg.queue_name + "." \
        + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    status, err_msg = gen_libs.chk_crt_dir(msg_path, write=True, read=True)

    if status:
        cfg.message_dir = msg_path

    else:
        status_flag = False

    status, err_msg = gen_libs.chk_crt_dir(log_path, write=True, read=True)

    if status:
        base_name, ext_name = os.path.splitext(cfg.log_file)
        log_name = base_name + "_" + cfg.exchange_name + "_" + cfg.queue_name \
            + ext_name
        cfg.log_file = os.path.join(log_path, log_name)
        status, err_msg = gen_libs.chk_crt_file(os.path.join(log_path,
                                                             proc_name),
                                                create=True, write=True,
                                                read=True)

        if status:
            cfg.proc_file = os.path.join(log_path, proc_name)

        else:
            status_flag = False

    else:
        status_flag = False

    status, err_msg = gen_libs.chk_crt_dir(cfg.transfer_dir, read=True)

    if not status:
        status_flag = False

    status, err_msg = gen_libs.chk_crt_dir(cfg.isse_dir, write=True, read=True)

    if not status:
        status_flag = False

    return cfg, status_flag


def is_valid_msg(line, log, **kwargs):

    """Function:  is_valid_msg

    Description:  Checks to see that the message is formatted correctly.

    Arguments:
        (input) line -> Single entry line from RabbitMQ queue message.
        (input) log -> Log class instance.
        (output) True|False - If the message is valid.

    """

    log.log_info("is_valid_msg:  Checking validation of message...")
    status = True

    if len(line.split()) == 0:
        log.log_err("Detected no entries in message line.")
        status = False

    elif len(line.split()) > 1:
        log.log_err("Detected more than one entry in message line: %s" %
                    (line))
        status = False

    return status


def non_proc_msg(rq, log, cfg, line, subj, **kwargs):

    """Function:  non_proc_msg

    Description:  Process non-processed messages.

    Arguments:
        (input) rq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) line -> Line of message that was not processed.

    """

    log.log_info("non_proc_msg:  Processing non-processed message...")
    frm_line = getpass.getuser() + "@" + socket.gethostname()
    f_name = rq.exchange + "_" + rq.queue_name + "_" + gen_libs.get_date() \
        + "_" + gen_libs.get_time() + ".txt"
    f_path = os.path.join(cfg.message_dir, f_name)
    subj = "rmq_2_isse: " + subj

    if cfg.to_line:
        log.log_info("Sending email to: %s..." % (cfg.to_line))
        email = gen_class.Mail(cfg.to_line, subj, frm_line)
        email.add_2_msg(line)
        email.send_mail()

    else:
        log.log_warn("No email being sent as TO line is empty.")

    log.log_err("Message: %s was not processed due to: %s" % (line, subj))
    log.log_info("Saving message to: %s" % (f_path))
    gen_libs.write_file(f_path, data="Exchange: %s, Queue: %s"
                        % (rq.exchange, rq.queue_name))
    gen_libs.write_file(f_path, data=line)


def find_files(log, cfg, line, **kwargs):

    """Function:  find_files

    Description:  Find one or more files from in a directory.

    Arguments:
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) line -> Line of message that was not processed.
        (output) file_list -> List of files found or empty list.

    """

    log.log_info("find_files:  Searching for files...")

    # Check current year/month.
    year_mon = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m")
    log.log_info("Search current year/month directory: %s" % (year_mon))
    file_list = gen_libs.dir_file_match(os.path.join(cfg.transfer_dir,
                                                     year_mon), line)

    if not file_list:
        log.log_info("Nothing found in current year/month directory: %s"
                     % (year_mon))

        # Add one to delta so as to produce a range.
        for delta in range(1, abs(cfg.delta_month) + 1):
            month, year = gen_libs.month_delta(datetime.datetime.now(),
                                               delta * -1)
            month = "%02d" % (month)
            log.log_info("Searching pass year/month: %s/%s" % (month, year))
            file_list = gen_libs.dir_file_match(os.path.join(cfg.transfer_dir,
                                                             str(year) + "/" +
                                                             str(month)),
                                                line)

            # Break loop if file(s) found.
            if file_list:

                # Add directory path to each file name.
                for pos, item in enumerate(file_list[:]):
                    file_list[pos] = os.path.join(cfg.transfer_dir,
                                                  str(year) + "/" + str(month),
                                                  item)

                break

    else:

        # Add directory path to each file name.
        for pos, item in enumerate(file_list[:]):
            file_list[pos] = os.path.join(cfg.transfer_dir, year_mon, item)

    return file_list


def is_valid_ext(f_name, cfg, log, **kwargs):

    """Function:  is_valid_ext

    Description:  Determine if the file extension is part of a list of
        extensions to be ignored.

    Arguments:
        (input) f_name -> File name.
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.
        (output) Status -> True|False - File extension is valid.

    """

    log.log_info("is_valid_ext:  Validating file extension...")
    status = True

    for ext in cfg.ignore_ext:
        if ext in f_name:
            log.log_warn("File extension invalid for: %s" % (f_name))
            status = False
            break

    return status


def is_valid_name(f_name, cfg, log, **kwargs):

    """Function:  is_valid_name

    Description:  Determine if the file name meets the search criteria.  If the
        file name has one of the items in the filter criteria, then it will be
        processed.  If the filter criteria is empty, then all files will be
        processed.

    Arguments:
        (input) f_name -> File name.
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.
        (output) status -> True|False - File name is valid.

    """

    log.log_info("is_valid_name:  Validating file name...")

    if cfg.file_filter:
        for filter_str in cfg.file_filter:
            if filter_str in f_name:
                status = True
                break

        # Else is for "for" loop.
        else:
            status = False
            log.log_warn("File name does not meet the file name criteria:  %s"
                         % (f_name))

    else:
        status = True

    return status


def process_msg(rq, log, cfg, method, body, **kwargs):

    """Function:  process_msg

    Description:  Process message from RabbitMQ queue.

    Arguments:
        (input) rq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) method -> Delivery properties.
        (input) body -> Message body.

    """

    log.log_info("process_msg:  Processing body of message...")

    for line in body.split():
        log.log_info("Processing line: %s" % (line))

        if gen_libs.file_search_cnt(cfg.proc_file, line) < cfg.max_resend:
            log.log_info("Write entry: %s to tracking file: %s"
                         % (line, cfg.proc_file))
            gen_libs.write_file(cfg.proc_file, data=line)

            if is_valid_msg(line, log):
                log.log_info("Looking for files...")
                file_list = find_files(log, cfg, line)

                if file_list:

                    for f_name in file_list:
                        log.log_info("Processing file: %s" % (f_name))

                        if is_valid_name(f_name, cfg, log):

                            if is_valid_ext(f_name, cfg, log):
                                log.log_info("Copy file: %s to ISSE directory."
                                             % (f_name))

                                gen_libs.cp_file2(os.path.basename(f_name),
                                                  os.path.dirname(f_name),
                                                  cfg.isse_dir)

                        else:
                            non_proc_msg(rq, log, cfg, line,
                                         "File does not meet file criteria")

                else:
                    non_proc_msg(rq, log, cfg, line, "File not found")

            else:
                non_proc_msg(rq, log, cfg, line, "Invalid message format")

        else:
            non_proc_msg(rq, log, cfg, line, "Reached max resends")


def monitor_queue(cfg, log, **kwargs):

    """Function:  monitor_queue

    Description:  Monitor RabbitMQ queue for messages.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.

    """

    def callback(channel, method, properties, body):

        """Function:  callback

        Description:  Process message from RabbitMQ.

        Arguments:
            (input) channel -> Channel properties.
            (input) method -> Delivery properties.
            (input) properties -> Properties of the message.
            (input) body -> Message body.

        """

        log.log_info("callback:  Processing message...")
        process_msg(rq, log, cfg, method, body)

        log.log_info("Deleting message from RabbitMQ")
        rq.ack(method.delivery_tag)

    log.log_info("monitor_queue:  Start monitoring queue...")
    rq = rabbitmq_class.RabbitMQCon(cfg.user, cfg.passwd, cfg.host, cfg.port,
                                    cfg.exchange_name, cfg.exchange_type,
                                    cfg.queue_name, cfg.queue_name,
                                    cfg.x_durable, cfg.q_durable,
                                    cfg.auto_delete)
    log.log_info("Connection info: %s->%s" % (cfg.host, cfg.exchange_name))
    connect_status, err_msg = rq.create_connection()

    if connect_status and rq.channel.is_open:
        log.log_info("Connected to RabbitMQ node")

        # Setup the RabbitMQ Consume callback and start monitoring.
        tag_name = rq.consume(callback)
        rq.start_loop()

    else:
        log.log_err("Failed to connnect to RabbuitMQ -> Msg: %s" % (err_msg))


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Create a program lock to prevent other instantiations from running.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])
    cfg, status_flag = validate_create_settings(cfg)

    if status_flag:
        log = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")
        str_val = "=" * 80
        log.log_info("%s:%s Initialized" % (cfg.host, cfg.exchange_name))
        log.log_info("%s" % (str_val))
        log.log_info("Exchange Name:  %s" % (cfg.exchange_name))
        log.log_info("Queue Name:  %s" % (cfg.queue_name))
        log.log_info("To Email:  %s" % (cfg.to_line))
        log.log_info("Transfer Directory:  %s" % (cfg.transfer_dir))
        log.log_info("ISSE Review Directory:  %s" % (cfg.isse_dir))
        log.log_info("Delta Month:  %s" % (cfg.delta_month))
        log.log_info("Resend:  %s" % (cfg.max_resend))
        log.log_info("File Filter:  %s" % (cfg.file_filter))
        log.log_info("%s" % (str_val))

        try:
            flavor_id = cfg.exchange_name + cfg.queue_name
            prog_lock = gen_class.ProgramLock(sys.argv, flavor_id)

            # Intersect args_array & func_dict to find which functions to call.
            for opt in set(args_array.keys()) & set(func_dict.keys()):
                func_dict[opt](cfg, log, **kwargs)

            del prog_lock

        except gen_class.SingleInstanceException:
            log.log_warn("rmq_2_isse lock in place for: %s" % (flavor_id))

        log.log_close()

    else:
        print("Error:  Problem in configuration file or directory setup.")


def main(**kwargs):

    """Function:  main

    Description:  Initializes program-wide variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary list for the function calls or other options.
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) sys.argv -> Arguments from the command line.
        (input) **kwargs:
            argv_list -> List of arguments from another program.

    """

    sys.argv = kwargs.get("argv_list", sys.argv)
    dir_chk_list = ["-d"]
    func_dict = {"-M": monitor_queue}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
