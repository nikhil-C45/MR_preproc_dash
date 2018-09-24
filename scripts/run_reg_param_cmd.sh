#!/bin/sh
#source /opt/minc/1.9.16/minc-toolkit-config.sh
source /ipl/quarantine/experimental/2013-02-15/init.sh
#tmpfile=$(mktemp /tmp/xfm_invert.XXXXXX)
xfminvert $1 tmp.xfm
reg_param=`xfm2param tmp.xfm`
rm tmp.xfm
echo $reg_param
