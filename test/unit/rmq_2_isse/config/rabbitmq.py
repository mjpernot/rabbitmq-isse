# RabbitMQ Configuration file
# Classification (U)
# Unclassified until filled.
user = "USER"
passwd = "PASSWORD"
host = "HOSTNAME"
# RabbitMQ Exchange name being monitored.
exchange_name = "rmq_2_isse_unit_test"
# RabbitMQ Queue name being monitored.
queue_name = "rmq_2_isse_unit_test"
# Email address(es) to send non-processed messages to or None.
# None state no emails are required to be sent.
to_line = None
# Base path and transfer directory for searching.
transfer_dir = "/www/intelink/highpoint/JWICStoSIPRtransfer/complete"
# Base path and ISSE Guard Transfer directory.
isse_dir = "/www/intelink/highpoint/JWICStoSIPRtransfer/reviewed"
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
