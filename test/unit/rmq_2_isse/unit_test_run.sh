#!/bin/bash
# Unit testing program for the rmq_2_isse.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  help_message"
test/unit/rmq_2_isse/help_message.py

echo ""
echo "Unit test:  is_valid_msg"
test/unit/rmq_2_isse/is_valid_msg.py

echo ""
echo "Unit test:  validate_create_settings"
test/unit/rmq_2_isse/validate_create_settings.py

echo ""
echo "Unit test:  find_files"
test/unit/rmq_2_isse/find_files.py

echo ""
echo "Unit test:  non_proc_msg"
test/unit/rmq_2_isse/non_proc_msg.py

echo ""
echo "Unit test:  process_msg"
test/unit/rmq_2_isse/process_msg.py

echo ""
echo "Unit test:  is_valid_ext"
test/unit/rmq_2_isse/is_valid_ext.py

echo ""
echo "Unit test:  monitor_queue"
test/unit/rmq_2_isse/monitor_queue.py

echo ""
echo "Unit test:  callback"
test/unit/rmq_2_isse/callback.py

echo ""
echo "Unit test:  run_program"
test/unit/rmq_2_isse/run_program.py

echo ""
echo "Unit test:  main"
test/unit/rmq_2_isse/main.py

