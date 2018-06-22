cd /home/hcalpro/hcalraw
./fnal_analyze.sh $1 master

cd /home/hcalpro/hcalraw-scripts/processPluginsHBQIE
./processPlugins -f /home/hcalpro/hcalraw/output/run$1-master.root
