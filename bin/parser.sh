#!/bin/bash
#
# Title: parser.sh
# Description: parse and load collection files
# Development Environment: macOS Monterey 12.6.9
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start parser"
cd /Users/gsc/Documents/github/mellow-hyena/src/back-end
source venv/bin/activate
time python3 ./parser.py
echo "end parser"
#