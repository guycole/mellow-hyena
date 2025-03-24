#!/bin/bash
#
# Title: xfer-wombat.sh
# Description: move local files to wombat, needs ssh authorized_keys for $DEST
# Development Environment: Debian 10 (buster)/raspian
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin:~/.local/bin; export PATH
#
DEST="gsc@rpi5a:/mnt/pp1/gsc/mellow"
SRC="/var/mellow"
#
echo "start transfer"
cd $SRC
rsync --ignore-existing --remove-source-files -avhe ssh . $DEST
echo "end transfer"
#
