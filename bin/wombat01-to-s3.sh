#!/bin/bash
#
# Title: wombat01-to-s3.sh
# Description: move hyena files local file system to s3
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
DEST_BUCKET=s3://mellow-hyena-uw2-t8833.braingang.net/fresh/
#
echo "start move"
cd /var/mellow/hyena/fresh; gzip *
aws s3 mv . $DEST_BUCKET --recursive --profile=wombat01
echo "end move"
