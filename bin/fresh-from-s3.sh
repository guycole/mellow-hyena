#!/bin/bash
#
# Title: fresh-from-s3.sh
# Description: move fresh s3 files to local for database import
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
SRC_BUCKET=s3://mellow-hyena-uw2-t8833.braingang.net/fresh/
WORK_DIR="/var/mellow/hyena/fresh"
#
echo "start move"
cd $WORK_DIR
aws s3 mv $SRC_BUCKET . --recursive --profile=wombat03rw
gunzip *
echo "end move"
#
