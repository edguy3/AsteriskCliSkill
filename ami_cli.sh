#!/bin/sh

### BEGIN INIT INFO
# Provides:          callerid
# Required-Start:    $local_fs $remote_fs $network
# Required-Stop:     $local_fs $remote_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start AMI CLI.
# Description:       Start the AMI CLI engine.
### END INIT INFO

# Author: Ed Guy <edguy@eguy.org>
# Copyright (C) 2017 Ed Guy <edguy@eguy.org> 
#

DESC="Announce CallerID from asterisk on mycroft"
#DAEMON=/usr/sbin/daemonexecutablename

D=/var/log
B=`basename $0 .sh`
PROG=/home/pi/ami_cli/ami_cli.py

L=/var/log/$B.log
P=/var/run/$B.pid


# background. 
doIt() {

    cd $D

    echo "Running $0 in ".$(pwd)

    while :
    do
	python $PROG
        sleep 4
    done
}


case "$1" in
    start)
	nohup $0 run >> $L 2>&1&
	echo $! > $P
	;;
    run)
	doIt
	;;
    stop)
	kill `cat $P`
	;;
    status)
	echo status
	ps aux | grep `cat $P`
	;;
    reload|restart)
        $0 stop
        $0 start
        ;;
    *)
	echo "Usage: $0 start|stop|status|restart "
	;;
esac
