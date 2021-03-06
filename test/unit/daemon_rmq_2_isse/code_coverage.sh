#!/bin/bash
# Unit test code coverage for daemon_rmq_2_isse.py module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=daemon_rmq_2_isse test/unit/daemon_rmq_2_isse/main.py 

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
 
