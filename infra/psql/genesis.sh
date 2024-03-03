#!/bin/bash
#
# Title:genesis.sh
# Description:
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
psql -U postgres template1 (or psql -U gsc template1)
create database hyena_v1;

createuser -U gsc -d -e -E -l -P -r -s hyena_admin
woofwoof

create role hyena_py with login;
alter role hyena_py with password 'bogus';


psql (PostgreSQL) 15.6 (Debian 15.6-0+deb12u1)
psql -U wombat -h localhost -d wombat_v1 < dropall.psql

