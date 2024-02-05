#!/bin/bash
#
# Title: reporter.sh
# Description: produce web reports
# Development Environment: macOS Monterey 12.6.9
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start reporter"
cd /Users/gsc/Documents/github/mellow-hyena/src/back-end
source venv/bin/activate
time python3 ./reporter.py
echo "end reporter"
