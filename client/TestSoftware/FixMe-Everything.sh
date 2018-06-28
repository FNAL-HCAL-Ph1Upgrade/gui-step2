#!/bin/bash

runNum=$1
n=$2
name=$3
comments=$4
cd /home/hcalpro/hcalraw-scripts/processPluginsHBQIE
./RunEverything.sh $runNum $n $name $comments
echo Finished running everything 
