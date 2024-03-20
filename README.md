mellow-hyena
=============

Collect and process aviation related emitters such as [ACARS](https://en.wikipedia.org/wiki/ACARS), [aircrat transponders](https://en.wikipedia.org/wiki/Aviation_transponder_interrogation_modes), UAT and [ADSB](https://en.wikipedia.org/wiki/Automatic_Dependent_Surveillance%E2%80%93Broadcast).

## Introduction
I want to know more about the aircraft around me such as what a "normal" level of activity might be or the types of aircraft.  Since I am only interested in aircraft which operate locally, and I don't need geographic displays etc. (already well supported by websites such as [ADSBexchange](https://adsbexchange.com/)).

In addition, I want to know more about the aircraft than is reported via ADSB (i.e. aircraft model and registration).  To learn more, I use [ADSBexchange](https://rapidapi.com/adsbx/api/adsbexchange-com1) which offers an inexpensive REST API.  For best results, I collect from ADSBexchange on each observation.

To learn about nearby aircraft, I have set up multiple collection stations to observe ADS-B and UAT broadcasts.  The observed broadcasts are collected into a PostGres instance for analysis and simple reports are generated.

UML Component Diagram [here](https://github.com/guycole/mellow-hyena/blob/main/uml/hyena-component.png)

## Collection
ADSB Collection runs on a standard [Raspberry Pi](https://www.raspberrypi.org/) using a [rtl-sdr](https://osmocom.org/projects/rtl-sdr/wiki/rtl-sdr) running [dump1090](https://github.com/antirez/dump1090) or [dump978](https://github.com/mutability/dump978).

Collection runs once per minute from cron(8).  The collected output is written to json formatted file and uploaded to [AWS S3](https://aws.amazon.com/pm/serv-s3) for later processing.

There can be multiple collection stations writing to AWS S3.

More on ADSB collection [here](https://github.com/guycole/mellow-hyena/tree/main/src/adsb-collect/README.md) and UAT collection [here](https://github.com/guycole/mellow-hyena/blob/main/src/uat-collect/README.md)

## Processing

Processing consists of moving collected ADSB observations from S3 to a machine for parsing and loading into postgres.  

More on observation processing [here](https://github.com/guycole/mellow-hyena/blob/main/src/back-end/README.md)

## Reporting

mellow-hyena produces simple reports about upload and observations.  

More on reporting [here](https://github.com/guycole/mellow-hyena/blob/main/src/back-end/README.md)

## Relevant Links

1. [Mode-S.org](https://mode-s.org)
1. [ADSB exploit](https://journals.open.tudelft.nl/joas/article/view/7229/5774)
1. [ICAO UAT Tech Manual](https://www.icao.int/safety/acp/Inactive%20working%20groups%20library/ACP-WG-C-UAT-4/UAT-SWG04-WP05%20-%20Draft%20Tech%20Manual-V0-4%20.pdf#search=UAT%20Tech%20Manual)
