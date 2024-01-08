#!/bin/bash
#
# Title: s3-move.sh
# Description: move files from s3 to local file system
# Development Environment: macOS Monterey 12.6.9
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start move"
cd /var/mellow/hyena-raw
aws s3 mv s3://mellow-hyena.braingang.net/anderson1 . --recursive --profile=cli_braingang
aws s3 mv s3://mellow-hyena.braingang.net/vallejo1 . --recursive --profile=cli_braingang
echo "end move"
