#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/process_list.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/help_message.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/non_proc_msg.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/monitor_queue.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/is_valid_name.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/is_valid_msg.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/is_valid_ext.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/find_files.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/callback.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/process_msg.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/validate_create_settings.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/run_program.py
coverage run -a --source=rmq_2_isse test/unit/rmq_2_isse/main.py
coverage run -a --source=daemon_rmq_2_isse test/unit/daemon_rmq_2_isse/main.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i

