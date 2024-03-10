#!/bin/bash
#
# Title:add_schema.sh
# Description:
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
# psql -U hyena_loader -d hyena_v1 // bogus
# psql -U hyena_loader -d hyena_v1_test // bogus
#
export PGDATABASE=hyena_v1_test
export PGHOST=localhost
export PGPASSWORD=woofwoof
export PGUSER=hyena
#
psql < adsb_exchange.psql
psql < adsb_ranking.psql
psql < box_score.psql
psql < cooked.psql
psql < device.psql
psql < load_log.psql
psql < observation.psql
#
