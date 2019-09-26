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


# Program Descriptions:
### Program:  rmq_2_isse.py:  Process a RabbitMQ message and send it to the ISSE Guard Transfer program.

### Program:  daemon_rmq_2_isse.py:  Runs the rmq_2_isse program as a daemon/service.

### Program:  rmq_2_isse_service.sh:  Init script for use with the Linux service command.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/rabbitmq-isse/rmq_2_isse.py -h
```


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

