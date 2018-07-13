#!/bin/bash

cd /home/hcalpro/hcalraw-scripts/processPluginsHBQIE
./MoveFiles.sh $1 $2 $3 
eval ssh hep@cmshcal11 '/home/django/testing_database_hb/uploader/upload_step2.sh '$4''
echo "Finished uploading cards to database"
