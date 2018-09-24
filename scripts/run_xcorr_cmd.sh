#!/bin/sh
#source /opt/minc/1.9.16/minc-toolkit-config.sh
source /ipl/quarantine/experimental/2013-02-15/init.sh
xcorr=`xcorr_vol $1 $2`
echo $xcorr
