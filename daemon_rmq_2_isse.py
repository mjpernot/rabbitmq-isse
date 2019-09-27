#!/usr/bin/python
# Classification (U)

"""Program:  daemon_rmq_2_isse.py

    Description:  Runs the rmq_2_isse program as a daemon/service.

    Usage:
        daemon_rmq_2_isse.py -a {start|stop|restart} {rmq_2_isse options}

    Arguments:
        -a {start|stop|restart} => Start, stop, restart the rmq_2_isse daemon.
        rmq_2_isse options => See rmq_2_isse for options.
            -c module option from rmq_2_isse is required to make the daemon
                pidfile unique for running multiple instances.

    Example:
        daemon_rmq_2_isse.py -a start -c rabbitmq -d config -M

"""

# Libraries and Global Variables

# Standard
import sys
import time
import os

# Third-party

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rmq_2_isse
import version

__version__ = version.__version__


class Rmq2IsseDaemon(gen_class.Daemon):

    """Class:  Rmq2IsseDaemon

    Description:  Daemon class to runn the rmq_2_isse program.

    Methods:
        run -> Daemon instance will execute this code when called.

    """

    def run(self):

        """Method:  run

        Description:  Will contain/point to the code to execute when the
            daemon start() or restart() options are executed.

        Variables:
            self.argv_list -> List of command line options and values.

        Arguments:

        """

        while True:
            rmq_2_isse.main(argv_list=self.argv_list)
            time.sleep(1)


def main():

    """Function:  main

    Description:  Initializes program-wide variables, processes command line
        arguments, sets up pidfile, and contols the running of the
        service/daemon.

    Variables:
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) sys.argv -> Arguments from the command line.

    """

    opt_val_list = ["-a", "-c", "-d"]
    opt_req_list = ["-a", "-c", "-d"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)

    f_name = "rmq2isse_daemon_" + args_array.get("-c", "") + ".pid"
    pid_file = os.path.join(gen_libs.get_base_dir(__file__), "tmp", f_name)
    daemon = Rmq2IsseDaemon(pid_file, argv_list=sys.argv)

    if not arg_parser.arg_require(args_array, opt_req_list):

        if "start" == args_array["-a"]:
            daemon.start()

        elif "stop" == args_array["-a"]:
            daemon.stop()

        elif "restart" == args_array["-a"]:
            daemon.restart()

        else:
            print("Unknown command")
            sys.exit(2)

        sys.exit(0)

    else:
        print(("Usage: %s -a start|stop|restart -c module -d directory/config "
               "{rmq_2_isse options}") % sys.argv[0])
        sys.exit(2)


if __name__ == "__main__":
    sys.exit(main())
