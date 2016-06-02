#!/bin/bash

#check if server.py is running

V=false

if pgrep -f server.py >/dev/null 2>&1
  then
    #do nothing
    if $V
      then
        echo "server.py is already running"
    fi
  else
    #start server
    if $V
      then
        echo "server.py is not running"
        echo "starting server.py..."
    fi
    nohup python /home/pi/server.py > /dev/null 2>&1
fi
