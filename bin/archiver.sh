#!/bin/bash
#
# Title: archiver.sh
# Description: move processesed files to archive
# Development Environment: macOS Monterey 12.6.9
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
today=$(date '+%Y-%m-%d')
file_name="hyena-${today}.tgz"
source_dir="hyena-success"
#
echo "start archive"
#
cd /var/mellow
tar -cvzf ${file_name} ${source_dir}
#
echo "start s3 transfer" 
aws s3 mv ${file_name} s3://mellow-archive.braingang.net/hyena/${file_name} --profile=cli_braingang
#
echo "cleanup"
rm -rf ${source_dir}
mkdir ${source_dir}
#
echo "end archive"
#