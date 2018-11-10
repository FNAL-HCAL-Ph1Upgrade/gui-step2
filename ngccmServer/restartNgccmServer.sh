#!/bin/bash
# restartNgccmServer.sh
# Caleb Smith --- July 1, 2018

# use tag to search for ngccm server process
# kill and then start ngccm server if it is running
# start ngccm server if it is not running
# use -k option to kill server and not start or restart

V=true
user="hcalpro"
startServer="/home/hcalpro/ngFEC/start_ngccm_hbfermi_00.sh"
port=64000
tag="hbfermi_00"
action=

if $V ; then
    echo " - start ngccm server script: $startServer"
fi

#check if ngccm server is running
#kill the server if it is running
if pid=$(pgrep -f $tag) ; then
    action="restart"
    # kill ngccm server
    if $V ; then
        echo " - ngccm server (tag $tag) is running (pid $pid)"
        echo " - using kill to send ngccm server to the grave"
    fi
    sudo -u $user kill -11 $pid
    return_value=$?
    if [ $return_value -eq 0 ]; then
        if [ "$1" = "-k" ]; then
            action="kill"
            echo " - success: "$action"ed ngccm server"
            exit 0
        fi
    else
        echo "ERROR: unable to kill ngccm server (tag $tag and pid $pid)"
    fi
else
    action="start"
    if $V ; then
        echo " - ngccm server (tag $tag) is not running"
    fi
fi

# don't continue for -k option
if [ "$1" = "-k" ]; then
    exit 0
fi


# start ngccm server

if $V ; then
    echo " - starting ngccm server (tag "$tag")... because the server will always rise again"
fi

sudo -u $user $startServer
return_value=$?
if [ $return_value -eq 0 ]; then
    echo " - success: "$action"ed ngccm server"
else
    echo "ERROR: the start ngccm server script returned nonzero error code: $return_value"
fi

