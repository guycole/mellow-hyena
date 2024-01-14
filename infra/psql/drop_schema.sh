#!/bin/bash
#
# Title:drop_schema.sh
# Description: remove schema
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
export PGDATABASE=hyena_v1
export PGHOST=localhost
export PGPASSWORD=woofwoof
export PGUSER=hyena_admin
#
psql $PGDATABASE -c "drop table cooked"
psql $PGDATABASE -c "drop table device"
psql $PGDATABASE -c "drop table observation"
psql $PGDATABASE -c "drop table load_log"
psql $PGDATABASE -c "drop table adsb_exchange"
#