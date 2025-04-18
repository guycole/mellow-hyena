#!/bin/bash
#
# Title: scorer.sh
# Description: 
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
HOME_DIR="/home/gsc/Documents/github"
#HOME_DIR="/Users/gsc/Documents/github"
#
echo "start load"
cd $HOME_DIR/mellow-hyena/src/back-end
source venv/bin/activate
time python3 ./scorer.py
echo "end load"
#
