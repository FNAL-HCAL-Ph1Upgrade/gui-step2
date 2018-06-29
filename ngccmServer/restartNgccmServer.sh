#!/bin/bash

#check if ngccm server is running

V=true

if pgrep -f ngccm >/dev/null 2>&1 ; then
    # kill and start ngccm server
    
    # kill ngccm server
    if $V ; then
        echo "ngccm server is already running"
        echo "using kill to send ngccm server into the grave"
    fi
    # start ngccm server
    if $V ; then
        echo "starting ngccm server... because the server will always rise again"
    fi
else
    # start ngccm server
    if $V ; then
        echo "ngccm server is not running"
        echo "starting ngccm server..."
    fi
    #source /home/pi/NGCCMeFEC/server/configPath.sh
    #nohup python /home/pi/NGCCMeFEC/server/ngccm server > /dev/null 2>&1 &
fi
