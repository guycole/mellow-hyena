#!/bin/bash
#
# Title:genesis.sh
# Description:
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
# psql -h localhost -p 5432 -U hyena_py -d hyena_v1
#
psql -U postgres template1 (or psql -U gsc template1)
create database hyena_v1;

createuser -U gsc -d -e -E -l -P -r -s hyena_admin
woofwoof

create role hyena_py with login;
alter role hyena_py with password 'bogus';

psql -U hyena_py -d hyena_v1
