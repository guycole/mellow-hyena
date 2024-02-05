#!/bin/bash
#
# Title: full_cycle.sh
# Description: download collection files, parse and load to DB and generate report
# Development Environment: macOS Monterey 12.6.9
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start full_cycle"
/Users/gsc/Documents/github/mellow-hyena/bin/s3-move.sh
/Users/gsc/Documents/github/mellow-hyena/bin/parser.sh
/Users/gsc/Documents/github/mellow-hyena/bin/ranker.sh
/Users/gsc/Documents/github/mellow-hyena/bin/reporter.sh
/Users/gsc/Documents/github/mellow-hyena/bin/web-copy.sh
echo "end full_cycle"
#