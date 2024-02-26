#!/bin/bash
#
# Title: xfer-anderson.sh
# Description: move local files to s3
# Development Environment: Debian 10 (buster)/raspian
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin:~/.local/bin; export PATH
#
echo "start transfer"
cd /var/mellow/hyena/raw; gzip *; cd ..
aws s3 mv raw s3://mellow-hyena.braingang.net/anderson1 --profile=wombat01 --recursive
echo "end transfer"
#
