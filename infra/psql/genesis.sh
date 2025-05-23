#!/bin/bash
#
# Title:genesis.sh
# Description:
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
psql -U postgres template1 (or psql -U gsc template1)

# (linux) su - postgres
createuser -U postgres -d -e -l -P -r -s hyena_admin
woofwoof
createuser -U postgres -e -l -P hyena_client
batabat

# as pg superuser
# create tablespace hyena location '/mnt/pg_tablespace/hyena';
# create tablespace hyena location '/mnt/pp1/postgres/hyena';

createdb hyena -O hyena_admin -D hyena -E UTF8 -T template0 -l C

# psql -h localhost -p 5432 -U hyena_admin -d hyena
# psql -h localhost -p 5432 -U hyena_client -d hyena

# as hyena_admin
create schema hyena_v1;
grant usage on schema hyena_v1 to hyena_client;

###### old
create database hyena_v1;
create database hyena_v1_test;

createuser -e -l -P -r -s hyena // woofwoof

alter role hyena set client_encoding to 'utf8';
alter role hyena set default_transaction_isolation to 'read committed';
alter role hyena set timezone to 'UTC';

grant all privileges on database hyena_v1 to hyena;
grant all privileges on database hyena_v1_test to hyena;

create role hyena_loader with login;
alter role hyena_loader with password 'bogus';

grant all privileges on database hyena_v1 to hyena_loader;
grant all privileges on database hyena_v1_test to hyena_loader;

psql -U hyena_loader -d hyena_v1_test -h localhost
