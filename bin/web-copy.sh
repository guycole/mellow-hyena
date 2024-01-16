#!/bin/bash
#
# Title: web-copy.sh
# Description: update web contents
# Development Environment: macOS Monterey 12.6.9
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start web copy" 
cd /var/mellow/hyena-web
aws s3 cp . s3://braingang.net/mellow-hyena --recursive --profile=cli_braingang
echo "end web copy" 
#