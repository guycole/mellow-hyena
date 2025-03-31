#!/bin/bash
#
# Title:drop_schema.sh
# Description: remove schema
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
export PGDATABASE=hyena
export PGHOST=localhost
export PGPASSWORD=woofwoof
export PGUSER=hyena_admin
#
psql $PGDATABASE -c "drop table hyena_v1.box_score"
psql $PGDATABASE -c "drop table hyena_v1.cooked"
psql $PGDATABASE -c "drop table hyena_v1.observation"
psql $PGDATABASE -c "drop table hyena_v1.adsb_exchange"
psql $PGDATABASE -c "drop table hyena_v1.load_log"
psql $PGDATABASE -c "drop table hyena_v1.site"
#psql $PGDATABASE -c "drop table adsb_ranking"
#
