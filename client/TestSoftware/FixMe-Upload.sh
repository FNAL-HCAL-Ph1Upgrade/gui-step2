#!/bin/bash
cd /home/hcalpro/hcalraw-scripts/processPluginsHBQIE
./MoveFiles.sh $1
ssh hep@cmshcal11 '/home/django/testing_database_hb/uploader/upload_step2.sh'
echo Finished with upload

