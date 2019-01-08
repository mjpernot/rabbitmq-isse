#!/bin/bash
# Integration testing program for the rmq_2_isse.py program.
# This will run all the integrations tests for this program.
# Will need to run this from the base directory where the program file
#   is located at.

echo ""
echo "Integration test:  process_msg"
test/integration/rmq_2_isse/process_msg.py

echo ""
echo "Integration test:  process_msg"
test/integration/rmq_2_isse/process_msg2.py

echo ""
echo "Integration test:  validate_create_settings"
test/integration/rmq_2_isse/validate_create_settings.py

echo ""
echo "Integration test:  validate_create_settings"
test/integration/rmq_2_isse/validate_create_settings2.py

echo ""
echo "Integration test:  non_proc_msg"
test/integration/rmq_2_isse/non_proc_msg.py

echo ""
echo "Integration test:  find_files"
test/integration/rmq_2_isse/find_files.py

echo ""
echo "Integration test:  monitor_queue"
test/integration/rmq_2_isse/monitor_queue.py

echo ""
echo "Integration test:  run_program"
test/integration/rmq_2_isse/run_program.py

echo ""
echo "Integration test:  main"
test/integration/rmq_2_isse/main.py

echo ""
echo "Cleanup of RabbitMQ exchange and queues"
test/integration/rmq_2_isse/rmq_cleanup.py

