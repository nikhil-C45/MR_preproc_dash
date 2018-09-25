#!/bin/sh
#source /opt/minc/1.9.16/minc-toolkit-config.sh
#source /ipl/quarantine/experimental/2013-02-15/init.sh
source $1
xcorr=$(xcorr_vol $2 $3)
echo $xcorr
