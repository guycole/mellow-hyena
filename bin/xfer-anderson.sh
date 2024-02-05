#!/bin/bash
#
# Title: xfer-anderson.sh
# Description: move local files to s3
# Development Environment: Debian 10 (buster)/raspian
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start transfer"
cd /home/gsc/github/mellow-hyena/aws_export; gzip *; cd ..
aws s3 mv aws_export s3://mellow-hyena.braingang.net/anderson1 --profile=hyena-rpi --recursive
echo "end transfer"
#