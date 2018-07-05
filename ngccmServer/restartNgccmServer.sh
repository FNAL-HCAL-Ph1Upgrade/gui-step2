#!/bin/bash
# restartNgccmServer.sh
# Caleb Smith --- July 1, 2018
# use tag to search for ngccm server process
# kill and then start ngccm server if it is running
# start ngccm server if it is not running

V=true
user="hcalpro"
startServer="/home/hcalpro/ngFEC/start_ngccm_hbfermi_00.sh"
#startServer=/home/hcalpro/ngFEC/ngccm-0.0.12-63.el7/opt/ngccm/scripts/start_ngccm_hbfermi_00.sh
port=64000
tag="hbfermi_00"

echo "start server script: $startServer"

#check if ngccm server is running
#kill the server if it is running

#if pgrep -f ngccm >/dev/null 2>&1 ; then
if pid=$(pgrep -f $tag) ; then
    # kill ngccm server
    if $V ; then
        echo "ngccm server with tag $tag is already running with pid $pid"
        echo "using kill to send ngccm server with tag $tag and pid $pid to the grave"
    fi
    kill $pid
else
    echo "ngccm server with tag $tag is not running"
fi

# start ngccm server

if $V ; then
    echo "starting ngccm server with tag "$tag"... because the server will always rise again"
fi
# bash $startServer > /dev/null 2>&1 &
$startServer
return_value=$?
if [ $return_value -eq 0 ]; then
    echo "Success: started ngccm server"
else
    echo "ERROR: the start ngccm server script returned nonzero error code: $return_value"
fi

