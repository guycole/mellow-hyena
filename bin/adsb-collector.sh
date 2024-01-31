#!/bin/bash
#
# Title: adsb-collector.sh
# Description: dump1090 collection
# Development Environment: Debian 10 (buster)/raspian
# Author: Guy Cole (guycole at gmail dot com)
#
# * * * * * /home/gsc/github/mellow-hyena/bin/adsb-collector.sh > /dev/null 2>&1
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
LD_LIBRARY_PATH=/usr/local/lib/arm-linux-gnueabihf; export LD_LIBRARY_PATH
#
echo "start collection"
#cd /Users/gsc/Documents/github/mellow-hyena/src/collector_rpi
cd /home/gsc/github/mellow-hyena/src/adsb_collect
source venv/bin/activate
python3 ./collector.py
echo "end collection"
#