#!/bin/bash
#
# Title:add_schema.sh
# Description:
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
# psql -U hyena_py -d hyena_v1
#
export PGDATABASE=hyena_v1
export PGHOST=localhost
export PGPASSWORD=woofwoof
export PGUSER=hyena_admin
#
psql < aircraft.psql
psql < load_log.psql
psql < observation.psql
#