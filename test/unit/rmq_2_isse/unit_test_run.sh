#!/bin/bash
# Unit testing program for the rmq_2_isse.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test"
test/unit/rmq_2_isse/help_message.py
test/unit/rmq_2_isse/is_valid_msg.py
test/unit/rmq_2_isse/validate_create_settings.py
test/unit/rmq_2_isse/find_files.py
test/unit/rmq_2_isse/non_proc_msg.py
test/unit/rmq_2_isse/process_msg.py
test/unit/rmq_2_isse/is_valid_ext.py
test/unit/rmq_2_isse/monitor_queue.py
test/unit/rmq_2_isse/callback.py
test/unit/rmq_2_isse/run_program.py
test/unit/rmq_2_isse/main.py

