#!/bin/bash
#
# Title: dump978.sh
# Description: dump978 listener
# Development Environment: Debian 10 (buster)/raspian
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#LD_LIBRARY_PATH=/usr/local/lib/arm-linux-gnueabihf; export LD_LIBRARY_PATH
#
cd /home/gsc/Documents/github/dump978
#
/usr/local/bin/rtl_sdr -f 978000000 -s 2083334 - | ./dump978 | ./uat2json /tmp
#
