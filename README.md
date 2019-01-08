# Python project for the processing RabbitMQ messages and sending files to the ISSE Guard reviewed directory.
# Classification (U)

# Description:
  This program is used to process a RabbitMQ message by looking for a file as listed in the message and if the file is valid, then send the file to the reviewed directory for the ISSE Guard to process.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Running
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox

# Features:
  * Process RabbitMQ messages and resend documents to the ISSE Guard Transfer program.
  * Run the monitor program as a service/daemon.
  * Allow messages to be filtered based on a file criteria setting.
  * Setup the program up as a service.

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/gen_class
    - lib/arg_parser
    - lib/gen_libs
    - rabbit_lib/rabbitmq_class

  * Setup a local account and group: rabbitmq:rabbitmq

  * Add rabbitmq account to the JACDXSD group on the server.


# Installation:

Install the program.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rabbitmq-isse.git
```

Install/upgrade system modules.

```
cd rabbitmq-isse
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Create configuration file.
  * NOTE:  If running multiple instances, each instance will have its own configuration file and you will need to change the name appropriately as listed throughout this file.  Example:  cp rabbitmq.py.TEMPLATE rabbitmq-sipr.py

```
chmod 777 logs message_dir tmp
cd config
cp rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the environment.
  * Make the appropriate changes to connect to RabbitMQ.
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"
    - queue_name = "QUEUE_NAME"
    - to_line = "EMAIL_ADDRESS@DOMAIN_NAME"
    - transfer_dir = "BASE_PATH/SEARCH_DIR"
    - isse_dir = "BASE_PATH/ISSE_DIR"

```
vim rabbitmq.py
chmod 600 rabbitmq.py
sudo chown rabbitmq:rabbitmq rabbitmq.py
cd ..
```

(Optional)  Enable program to be ran as a service.  Modify the service script to change the variables to reflect the environment setup.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * The MOD_LIBRARY variable is referencing the configuration file setup above.
    - NOTE:  The MOD_LIBRARY variable will only be required to be changed if running multiple instances.  Example:  MOD_LIBRARY="rabbitmq-sipr"
  * Make the appropriate changes to run a service.
    - BASE_PATH="{Python_Project}/rabbitmq-isse"
    - MOD_LIBRARY="rabbitmq"

```
vim rmq_2_isse_service.sh
sudo ln -s {Python_Project}/rabbitmq-isse/rmq_2_isse_service.sh /etc/init.d/rmq_2_isse
sudo chkconfig --add rmq_2_isse
```

If running multiple instances, then each instance will have its own service script, service name, and link.  Example of setting service to a unique name:

```
cp rmq_2_isse_service.sh rmq_2_isse_service-sipr.sh
vim rmq_2_isse_service-sipr.sh
sudo ln -s {Python_Project}/rabbitmq-isse/rmq_2_isse_service-sipr.sh /etc/init.d/rmq_2_isse-sipr
sudo chkconfig --add rmq_2_isse-sipr
```


# Running
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Run this program as the rabbitmq account.

### Running as a service.
Starting the service.

```
service rmq_2_isse start
```

Stopping the service.

```
service rmq_2_isse stop
```

### Running as a daemon.
Starting the daemon.

```
{Python_Project}/rabbitmq-isse/daemon_rmq_2_isse.py -a start -c rabbitmq -d {Python_Project}/rabbitmq-isse/config -M
```

Stopping the daemon.

```
{Python_Project}/rabbitmq-isse/daemon_rmq_2_isse.py -a stop -c rabbitmq -d {Python_Project}/rabbitmq-isse/config -M
```

### Running from the command line.
Stating the program.

```
{Python_Project}/rabbitmq-isse/rmq_2_isse.py -c rabbitmq -d {Python_Project}/rabbitmq-isse/config -M
```

Stopping the program.
```
<Ctrl-C>
```


# Program Description:
### Program:  rmq_2_isse.py
##### Description:  Process a RabbitMQ message and send it to the ISSE Guard Transfer program.

### Program:  daemon_rmq_2_isse.py
##### Description:  Runs the rmq_2_isse program as a daemon/service.

### Program:  rmq_2_isse_service.sh
##### Description:  Init script for use with the Linux service command.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/rabbitmq-isse/rmq_2_isse.py -h
```


# Help Message:
  Below is the help message for the program.  Recommend running the -h option on the command line to see the latest help message.

    Program:  rmq_2_isse.py

    Description:  Process a RabbitMQ message, locate the document referenced
        in the message and copy the document to the ISSE review directory.

    Usage:
        rmq_2_isse.py -c file -d path/config [-M] [-v | -h]

    Arguments:
        -M => Monitor and process messages from a RabbitMQ queue.
        -c file => ISSE Guard configuration file.  Required argument.
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
            # File name must contain one of the strings in the list to be processed.
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


    Program:  daemon_rmq_2_isse.py

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


# Testing:


# Unit Testing:

### Description: Testing consists of unit testing for the functions in the rmq_2_isse.py program.

### Installation:

Install these programs using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rabbitmq-isse.git
```

Install/upgrade system modules.

```
cd rabbitmq-isse
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Unit test runs for rmq_2_isse.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rabbitmq-isse
```


### Unit:  help_message
```
test/unit/rmq_2_isse/help_message.py
```

### Unit:  validate_create_settings
```
test/unit/rmq_2_isse/validate_create_settings.py
```

### Unit:  is_valid_msg
```
test/unit/rmq_2_isse/is_valid_msg.py
```

### Unit:  non_proc_msg
```
test/unit/rmq_2_isse/non_proc_msg.py
```

### Unit:  find_files
```
test/unit/rmq_2_isse/find_files.py
```

### Unit:  is_valid_ext
```
test/unit/rmq_2_isse/is_valid_ext.py
```

### Unit:  is_valid_name
```
test/unit/rmq_2_isse/is_valid_name.py
```

### Unit:  process_msg
```
test/unit/rmq_2_isse/process_msg.py
```

### Unit:  monitor_queue
```
test/unit/rmq_2_isse/monitor_queue.py
```

### Unit:  callback
```
test/unit/rmq_2_isse/callback.py
```

### Unit:  run_program
```
test/unit/rmq_2_isse/run_program.py
```

### Unit:  main
```
test/unit/rmq_2_isse/main.py
```

### All unit testing
```
test/unit/rmq_2_isse/unit_test_run.sh
```

### Unit test code coverage
```
test/unit/rmq_2_isse/code_coverage.sh
```

# Unit test runs for daemon_rmq_2_isse.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rabbitmq-isse
```

### Unit:  main
```
test/unit/daemon_rmq_2_isse/main.py
```

### Unit test code coverage
```
test/unit/daemon_rmq_2_isse/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the rmq_2_isse.py program.

### Installation:

Install these programs using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rabbitmq-isse.git
```

Install/upgrade system modules.

```
cd rabbitmq-isse
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create configuration file.

```
cd test/integration/rmq_2_isse/config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the environment.
  * Make the appropriate changes to connect to RabbitMQ.
    - user = "USER"
    - passwd = "USER_PASSWORD"
    - host = "HOST_NAME"
    - exchange_name = "EXCHANGE_NAME"        -> Change to:  exchange_name = "isse-guard-test"
    - queue_name = "QUEUE_NAME"              -> Change to:  queue_name = "isse-guard-test"
    - to_line = "EMAIL_ADDRESS@DOMAIN_NAME"  -> Change to:  to_line = "user_email@domain_name"
    - transfer_dir = "BASE_PATH/SEARCH_DIR"  -> Change to:  transfer_dir = "transfer_dir"
    - isse_dir = "BASE_PATH/ISSE_DIR"        -> Change to:  isse_dir = "isse_dir"

```
vim rabbitmq.py
chmod 600 rabbitmq.py
```

# Integration test runs for rmq_2_isse.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rabbitmq-isse
```


### Integration:  process_msg
```
test/integration/rmq_2_isse/process_msg.py
```

### Integration:  process_msg
```
test/integration/rmq_2_isse/process_msg2.py
```

### Integration:  validate_create_settings
```
test/integration/rmq_2_isse/validate_create_settings.py
```

### Integration:  validate_create_settings
```
test/integration/rmq_2_isse/validate_create_settings2.py
```

### Integration:  non_proc_msg
```
test/integration/rmq_2_isse/non_proc_msg.py
```

### Integration:  find_files
```
test/integration/rmq_2_isse/find_files.py
```

### Integration:  monitor_queue
```
test/integration/rmq_2_isse/monitor_queue.py
```

### Integration:  run_program
```
test/integration/rmq_2_isse/run_program.py
```

### Integration:  main
```
test/integration/rmq_2_isse/main.py
```

### Cleanup of RabbitMQ exchange and queues
```
test/integration/rmq_2_isse/rmq_cleanup.py
```

### All integration testing
```
test/integration/rmq_2_isse/integration_test_run.sh
```

### Integration test code coverage
```
test/integration/daemon_rmq_2_isse/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the rmq_2_isse.py program.

### Installation:

Install these programs using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/rabbitmq-isse.git
```

Install/upgrade system modules.

```
cd rabbitmq-isse
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:
  * Please note that the blackbox testing will require access to a rabbitmq system to run the tests.

Create configuration file.

```
cd test/blackbox/rmq_2_isse/config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the environment.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * The to_line variable must be a valid email address which can be monitored during testing.
  * Make the appropriate changes to connect to RabbitMQ.
    - user = "USER"
    - passwd = "USER_PASSWORD"
    - host = "HOST_NAME"
    - to_line = "EMAIL_ADDRESS@DOMAIN_NAME"
    - exchange_name = "EXCHANGE_NAME"        -> Change to:  exchange_name = "blackbox-test"
    - queue_name = "QUEUE_NAME"              -> Change to:  queue_name = "blackbox-test"
    - transfer_dir = "BASE_PATH/SEARCH_DIR"  -> Change to:  transfer_dir = "{Python_Project}/rabbitmq-isse/test/blackbox/rmq_2_isse/transfer_dir"
    - isse_dir = "BASE_PATH/ISSE_DIR"        -> Change to:  isse_dir = "{Python_Project}/rabbitmq-isse/test/blackbox/rmq_2_isse/isse_dir"
    - delta_month = 6                        -> Change to:  delta_month = 2

```
vim rabbitmq.py
chmod 600 rabbitmq.py
```

Create second configuration file for multiple daemon instances.
```
cp rabbitmq.py rabbitmq2.py
```
Make the appropriate changes to the environment.
  * Make the appropriate changes to connect to RabbitMQ.
    - exchange_name = "blackbox-test"        -> Change to:  exchange_name = "blackbox-test-2"
    - queue_name = "blackbox-test"           -> Change to:  queue_name = "blackbox-test-2"

```
vim rabbitmq2.py
chmod 600 rabbitmq2.py
```

Create third configuration file for testing the file filter criteria setting.
```
cp rabbitmq2.py rabbitmq3.py
```

Make the appropriate changes to the environment.
  * Make the appropriate changes to connect to RabbitMQ.
    - file_filter = []                       -> Change to:  file_filter = ["SCI-CW"]

```
vim rabbitmq3.py
chmod 600 rabbitmq3.py
```


# Blackbox test run for rmq_2_isse.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/rabbitmq-isse
```

### Blackbox:  rmq_2_isse.py
```
test/blackbox/rmq_2_isse/blackbox_test.sh
```

