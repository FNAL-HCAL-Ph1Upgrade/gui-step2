#!/bin/bash
# restartNgccmServer.sh
# Caleb Smith --- July 1, 2018
# use port to search for ngccm server process
# kill and then start ngccm server if it is running
# start ngccm server if it is not running

V=true
user=hcalpro
startServer=/home/hcalpro/ngFEC/start_ngccm_hehbfermi_00.sh
port=64000

#check if ngccm server is running

#if pgrep -f ngccm >/dev/null 2>&1 ; then
if pid=$(pgrep -f $port) ; then
    # kill and start ngccm server
    
    # kill ngccm server
    if $V ; then
        echo "ngccm server is already running on port $port with pid $pid"
        echo "using kill to send ngccm server on port $port with pid $pid to the grave"
    fi
    #sudo -u $user kill $pid
    # start ngccm server
    if $V ; then
        echo "starting ngccm server on port "$port"... because the server will always rise again"
    fi
    #sudo -u $user $starServer
else
    # start ngccm server
    if $V ; then
        echo "ngccm server on port $port is not running"
        echo "starting ngccm server on port "$port"... I look forward to our collaboration"
    fi
    #sudo -u $user $starServer
    # > /dev/null 2>&1 &
fi

