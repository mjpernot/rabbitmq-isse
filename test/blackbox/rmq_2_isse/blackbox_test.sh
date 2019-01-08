#!/bin/bash
# Blackbox testing program for the rmq_2_isse.py program.

BASE_PATH=$PWD

# Setup the test files for all blackbox tests.
test/blackbox/rmq_2_isse/blackbox_setup.py

echo "Scenario 1:  rmq_2_isse blackbox testing...Startup with no RabbitMQ exchange and empty queue"
test/blackbox/rmq_2_isse/rmq_cleanup.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a start
test/blackbox/rmq_2_isse/blackbox_test.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a stop
test/blackbox/rmq_2_isse/blackbox_cleanup.py
test/blackbox/rmq_2_isse/rmq_cleanup.py

echo "Scenario 2:  rmq_2_isse blackbox testing...Startup with data in RabbitMQ queue"
test/blackbox/rmq_2_isse/rmq_cleanup.py
test/blackbox/rmq_2_isse/blackbox_publish.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a start
test/blackbox/rmq_2_isse/blackbox_test2.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a stop
test/blackbox/rmq_2_isse/blackbox_cleanup.py
test/blackbox/rmq_2_isse/rmq_cleanup.py

echo "Scenario 3:  rmq_2_isse blackbox testing...Restart of rmq_2_isse service"
test/blackbox/rmq_2_isse/rmq_cleanup.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a start
test/blackbox/rmq_2_isse/blackbox_test3.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a restart
test/blackbox/rmq_2_isse/blackbox_test4.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a stop
test/blackbox/rmq_2_isse/blackbox_cleanup.py
test/blackbox/rmq_2_isse/rmq_cleanup.py

echo "Scenario 4:  rmq_2_isse blackbox testing...Multiple rmq_2_isse service instances"
test/blackbox/rmq_2_isse/rmq_cleanup.py
test/blackbox/rmq_2_isse/rmq_cleanup2.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a start
daemon_rmq_2_isse.py -c rabbitmq2 -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a start
test/blackbox/rmq_2_isse/blackbox_test5.py
test/blackbox/rmq_2_isse/blackbox_test6.py
daemon_rmq_2_isse.py -c rabbitmq -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a stop
daemon_rmq_2_isse.py -c rabbitmq2 -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a stop
test/blackbox/rmq_2_isse/blackbox_cleanup.py
test/blackbox/rmq_2_isse/rmq_cleanup.py
test/blackbox/rmq_2_isse/rmq_cleanup2.py

echo "Scenario 5:  rmq_2_isse blackbox testing...Process message with the file filter setting on"
test/blackbox/rmq_2_isse/rmq_cleanup.py
daemon_rmq_2_isse.py -c rabbitmq3 -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a start
test/blackbox/rmq_2_isse/blackbox_test7.py
daemon_rmq_2_isse.py -c rabbitmq3 -d ${BASE_PATH}/test/blackbox/rmq_2_isse/config -M -a stop
test/blackbox/rmq_2_isse/blackbox_cleanup.py
test/blackbox/rmq_2_isse/rmq_cleanup.py

# Clear out all test files for the blackbox tests.
test/blackbox/rmq_2_isse/blackbox_teardown.py

