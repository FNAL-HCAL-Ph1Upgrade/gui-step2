#!/bin/bash
# Hack to run the register test from the gui
# Setup python3
source /opt/root6_py3/bin/thisroot.sh
runNum=$1
name=${18}
comment=${19}
cd /home/hcalpro/GITrepos/Common/
python RunRegisterTest.py $runNum $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} "$name" "$comment"
echo Finished with register test
