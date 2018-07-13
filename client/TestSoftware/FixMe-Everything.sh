#!/bin/bash
# Setup python3
source /opt/root6_py3/bin/thisroot.sh
runNum=$1
n=$2
name=$3
comments=$4
cd /home/hcalpro/hcalraw-scripts/processPluginsHBQIE
./RunEverything.sh $runNum $n "$name" "$comments"
echo Finished running everything 
