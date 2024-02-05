#!/bin/bash
#
# Title: ranker.sh
# Description: run after parse/load to rank most common beacons
# Development Environment: macOS Monterey 12.6.9
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start ranker"
cd /Users/gsc/Documents/github/mellow-hyena/src/back-end
source venv/bin/activate
time python3 ./ranker.py
echo "end ranker"
