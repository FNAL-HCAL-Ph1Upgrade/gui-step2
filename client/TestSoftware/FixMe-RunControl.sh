#!/bin/bash
# Setup python3
source /opt/root6_py3/bin/thisroot.sh
runNum=$1
name=$2
comments=$3
cd /home/hcalpro/hcalraw
./fnal_analyze.sh $runNum master

cd /home/hcalpro/hcalraw-scripts/processPluginsHBQIE
./processPlugins -f /home/hcalpro/hcalraw/output/run$runNum-master.root -n "$name" -c "$comments"
echo Finished processing run control output
