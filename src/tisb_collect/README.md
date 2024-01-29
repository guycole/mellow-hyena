mellow-hyena/tisb_collect
=========================

## Introduction
Python script to read json from dump1090 and write to a json formatted file.  Runs from cron every minute.  Eventually the output files will be moved to AWS S3 for later processing.

## Bill Of Materials
1. Raspberry Pi 3 w/power supply
1. RTL-SDR w/antenna

## dump1090
stuff

### dump978 installation

https://github.com/mutability/dump978.git

rtl_sdr -f 978000000 -s 2083334 -g 48 - | ./dump978 | ./uat2text

https://github.com/flightaware/dump978 (this has much baggage)

