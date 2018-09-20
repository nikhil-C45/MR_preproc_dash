#!/bin/sh
source /opt/minc/1.9.16/minc-toolkit-config.sh
xfminvert $1 tmp.xfm
reg_param=`xfm2param tmp.xfm`
rm tmp.xfm
echo $reg_param
