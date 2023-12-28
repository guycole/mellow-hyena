#!/bin/bash
#
# Title: rpi-xfer-vallejo.sh
# Description: move local files to s3
# Development Environment: Debian 10 (buster)/raspian
# Author: Guy Cole (guycole at gmail dot com)
#
# 29 * * * * /home/gsc/github/mellow-heeler/bin/rpi-xfer-vallejo.sh > /dev/null 2>&1
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start transfer"
cd /home/gsc/github/mellow-hyena
aws s3 mv aws_export s3://mellow-hyena.braingang.net/vallejo1 --profile=hyena-rpi --recursive
echo "end transfer"
