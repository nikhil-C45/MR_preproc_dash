#!/bin/sh
#source /opt/minc/1.9.16/minc-toolkit-config.sh
#source /ipl/quarantine/experimental/2013-02-15/init.sh
source $1
tmpfile=$(mktemp /tmp/xfm_invert.XXXXXX)
xfminvert $2 $tmpfile -clobber
reg_param=$(xfm2param $tmpfile)
rm -f $tmpfile
echo $reg_param
