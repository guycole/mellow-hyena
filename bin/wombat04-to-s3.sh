#!/bin/bash
#
# Title: wombat04-to-s3.sh
# Description: move hyena files from local file system to s3
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
TODAY=$(date '+%Y-%m-%d')
FILE_NAME="hyena-${TODAY}.tgz"
#
DEST_BUCKET=s3://mellow-hyena-uw2-t8833.braingang.net/fresh/
#
SOURCE_DIR="archive"
WORK_DIR="/var/mellow/hyena/fresh"
#
echo "start move"
cd ${WORK_DIR}; gzip *
#
echo "start s3 transfer" 
aws s3 mv . $DEST_BUCKET --recursive --profile=wombat04
#
echo "end move"
#
