mellow-hyena
=============

Collect and process [ADSB](https://en.wikipedia.org/wiki/Automatic_Dependent_Surveillance%E2%80%93Broadcast) observations

## Introduction
I want to know more about the aircraft around me such as what a "normal" level of activity might be or the types of aircraft.  Since I am only interested in aircraft which operate locally, and I don't need geographic displays etc. (already well supported by websites such as https://https://adsbexchange.com/)  

## Collection
ADSB Collection runs on a standard [Raspberry Pi 4](https://www.raspberrypi.org/) using a [rtl-sdr](https://osmocom.org/projects/rtl-sdr/wiki/rtl-sdr) running [dump1090](https://github.com/antirez/dump1090)

dump1090 will return a json formatted report of all ADSB broadcasts.

Twice a minute, I ask dump1090 to report on current ADSB broadcasts and write these to files which are uploaded to [AWS S3][https://aws.amazon.com/pm/serv-s3] for later processing.

## Processing
Move collected ADSB observations from S3 to local machine for parsing and loading into postgres.

I want to know more about the aircraft than is reported via ADSB.

FlightRadar/AirLabs offers a free REST API, but I could not get it to filter by hex code (or anything) so that isn't helpful.

ADSBexchange offers an inexpensive REST API  
