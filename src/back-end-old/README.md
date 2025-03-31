mellow-hyena/back-end
=========================

## Introduction
Python scripts which load raw collection files arom AWS S3 to [postgresql](https://www.postgresql.org/), and produce reports.  Eventually the parsed files are moved back to AWS S3 for archival.  There is a data flow diagram at the bottom of this file.

### parser.sh
Parsing raw collection files and loading into postgresql is performed by [parser.sh](https://github.com/guycole/mellow-hyena/blob/main/bin/parser.sh).

### ranker.sh
Updates collection statistics which are kept within postgresql [ranker.sh](https://github.com/guycole/mellow-hyena/blob/main/bin/ranker.sh).

### reporter.sh
Read statistics from postgres and write HTML files using jinja templates [reporter.sh](https://github.com/guycole/mellow-hyena/blob/main/bin/reporter.sh).

## Installation
You will need a postgresql instance, add the database schema( using [add_schema.sh](https://github.com/guycole/mellow-hyena/blob/main/infra/psql/add_schema.sh).  Tweak the [config.yaml](https://github.com/guycole/mellow-hyena/blob/main/src/back_end/config.yaml) to match your local environment.  The python scripts rely upon virtualenv, so create that and configure it using requirements.txt.  Try your luck by invoking [parser.sh](https://github.com/guycole/mellow-hyena/blob/main/bin/parser.sh).

## Data Flow Diagram
![Data Flow](https://github.com/guycole/mellow-hyena/blob/main/src/back-end/backend_dfd.png)