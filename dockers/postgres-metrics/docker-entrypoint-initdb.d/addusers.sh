#!/usr/bin/env bash

set -eux

export PGPASSWORD=$POSTGRES_PASSWORD

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER sdl WITH ENCRYPTED PASSWORD '$SDL_POSTGRES_PASSWORD';
    CREATE DATABASE runmetrics WITH OWNER sdl TEMPLATE template0 ENCODING UTF8 LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8';
    GRANT ALL PRIVILEGES ON DATABASE runmetrics TO sdl;
    \c runmetrics;
    CREATE TABLE IF NOT EXISTS commmit_metrics
(
    uid          BIGSERIAL PRIMARY KEY          NOT NULL,
    repo_path    varchar(1000)               NOT NULL,
    commit_id    varchar(1000)               NOT NULL,
    metrics_file varchar(1000)               NOT NULL,
    metrics      jsonb                       DEFAULT '{}',
    author       varchar(1000)               DEFAULT '',
    committer    varchar(1000)               DEFAULT '',
    committed_time  timestamp without time zone NOT NULL,
    authored_date timestamp without time zone NULL,
    co_authors   varchar(1000)               DEFAULT '',
    state        varchar(100)                NOT NULL,
    created_at   timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    parsed_at    timestamp without time zone NULL
);
EOSQL
