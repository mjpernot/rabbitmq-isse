#!/bin/sh
# chkconfig: 345 26 74
# description: RabbitMQ to ISSE Guard transfer process
### BEGIN INIT INFO
# Provides:		rmq_2_isse.py
# Required-Start:	$local_fs
# Required-Stop:
# X-Start-Before:	
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	Start and stop the RabbitMQ to Isse Guard transfer reviewed directory
# Description:		Processes messages from RabbitMQ, locate the file in the completed directory,
#			and then copy the file to the ISSE Guard reviewed directory.
### END INIT INFO

BASE_PATH="{Python_Project}/rabbitmq-isse"
MOD_LIBRARY="rabbitmq"
USER_ACCOUNT="rabbitmq"

case $1 in
   start)
      su - ${USER_ACCOUNT} -c "${BASE_PATH}/daemon_rmq_2_isse.py -a start -c ${MOD_LIBRARY} -d ${BASE_PATH}/config -M"
      touch /var/lock/subsys/$MOD_LIBRARY
      ;;

   stop)
      su - ${USER_ACCOUNT} -c "${BASE_PATH}/daemon_rmq_2_isse.py -a stop -c ${MOD_LIBRARY} -d ${BASE_PATH}/config -M"
      rm -f /var/lock/subsys/$MOD_LIBRARY
      ;;

   restart)
      rm -f /var/lock/subsys/$MOD_LIBRARY
      su - ${USER_ACCOUNT} -c "${BASE_PATH}/daemon_rmq_2_isse.py -a restart -c ${MOD_LIBRARY} -d ${BASE_PATH}/config -M"
      touch /var/lock/subsys/$MOD_LIBRARY
      ;;

   *)
      echo $"Usage: $0 {start|stop|restart}"

esac

