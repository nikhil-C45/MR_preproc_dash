#!/bin/sh
source /opt/minc/1.9.16/minc-toolkit-config.sh
xcorr=`xcorr_vol $1 $2`
echo $xcorr
