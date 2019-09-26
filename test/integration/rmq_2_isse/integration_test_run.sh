#!/bin/bash
# Integration testing program for the rmq_2_isse.py program.
# This will run all the integrations tests for this program.
# Will need to run this from the base directory where the program file
#   is located at.

echo ""
echo "Integration test"
test/integration/rmq_2_isse/process_msg.py
test/integration/rmq_2_isse/process_msg2.py
test/integration/rmq_2_isse/validate_create_settings.py
test/integration/rmq_2_isse/validate_create_settings2.py
test/integration/rmq_2_isse/non_proc_msg.py
test/integration/rmq_2_isse/find_files.py
test/integration/rmq_2_isse/monitor_queue.py
test/integration/rmq_2_isse/run_program.py
test/integration/rmq_2_isse/main.py
test/integration/rmq_2_isse/rmq_cleanup.py

