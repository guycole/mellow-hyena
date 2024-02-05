mellow-hyena
=============

Collect and process [ADSB](https://en.wikipedia.org/wiki/Automatic_Dependent_Surveillance%E2%80%93Broadcast) observations

## Introduction
I want to know more about the aircraft around me such as what a "normal" level of activity might be or the types of aircraft.  Since I am only interested in aircraft which operate locally, and I don't need geographic displays etc. (already well supported by websites such as https://https://adsbexchange.com/).

In addition, I want to know more about the aircraft than is reported via ADSB (i.e. aircraft model and registration).  To learn more, I use [ADSBexchange](https://rapidapi.com/adsbx/api/adsbexchange-com1) which offers an inexpensive REST API.  For best results, I collect from ADSBexchange on each observation.

## Collection
ADSB Collection runs on a standard [Raspberry Pi](https://www.raspberrypi.org/) using a [rtl-sdr](https://osmocom.org/projects/rtl-sdr/wiki/rtl-sdr) running [dump1090](https://github.com/antirez/dump1090) or [dump978](https://github.com/mutability/dump978).

Collection runs once per minute from cron(8).  The collected output is written to json formatted file and uploaded to [AWS S3](https://aws.amazon.com/pm/serv-s3) for later processing.

There can be multiple collection stations writing to AWS S3.

## Processing

Processing consists of moving collected ADSB observations from S3 to a machine for parsing and loading into postgres.  

For processing, create a postgresql database and populate with the script "add_schema.sh".

Then run the script "parser.sh" to parse collected files and load into postgresql.

## Reporting

mellow-hyena produces simple reports about upload and observations.  

xxx
