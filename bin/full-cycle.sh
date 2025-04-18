#!/bin/bash
#
# Title: full-cycle.sh
# Description: download collection files, parse and load to DB and generate report
# Development Environment: macOS Monterey 12.6.9
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start full-cycle"
/home/gsc/Documents/github/mellow-hyena/bin/fresh-from-s3.sh
/home/gsc/Documents/github/mellow-hyena/bin/loader.sh
#/home/gsc/Documents/github/mellow-hyena/bin/scorer.sh
#/home/gsc/Documents/github/mellow-hyena/bin/reporter.sh
echo "end full-cycle"
#
