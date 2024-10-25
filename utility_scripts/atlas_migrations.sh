#!/bin/bash

# Related atlas documentation can be found here:
# - Creating a baseline: https://atlasgo.io/versioned/apply#existing-databases
# - Creating a diff: https://atlasgo.io/versioned/diff

MIGRATIONS="${MIGRATIONS:-migrations}"
SQLITEDB="${SQLITEDB:-data.db}"
WORKDIR="${WORKDIR:-.}"

_assert_gt() {
    VAL_A=$1
    VAL_B=$2
    MESSAGE=$3
    if [[ "$VAL_A" -gt "$VAL_B" ]]; then
        echo "${MESSAGE}";
        exit 1;
    fi
}

atlas() {
    docker run \
        --rm \
        --user "`id -u`:`id -g`" \
        --name atlas \
        --volume ./migrations:/opt/migrations \
        --volume ./.tmp:/opt/db \
        --workdir /opt \
        arigaio/atlas $@
}

create_baseline_schema() {
    _assert_gt 1 $# "arguments: <migration-name>"
    MIGRATION_NAME=$1
    atlas migrate diff "${MIGRATION_NAME}" \
        --dir "file://${MIGRATIONS}" \
        --dev-url "sqlite://file?mode=memory" \
        --to "sqlite://db/${SQLITEDB}"
}

apply_baseline() {
    _assert_gt 1 $# "arguments: <migration-id>"
    MIGRATION_ID=$1
    atlas migrate apply \
        --url "sqlite://db/${SQLITEDB}" \
        --dir "file://${MIGRATIONS}" \
        --baseline "${MIGRATION_ID}"
}

create_migration() {
    _assert_gt 1 $# "arguments: <migration-name>"
    MIGRATION_NAME=$1
   atlas migrate diff "${MIGRATION_NAME}" \
        --dir "file://${MIGRATIONS}" \
        --to "sqlite://db/${SQLITEDB}" \
        --dev-url "sqlite://file?mode=memory"
}

apply_migrations() {
    atlas migrate apply \
        --url "sqlite://db/${SQLITEDB}" \
        --dir "file://${MIGRATIONS}"
}

rehash() {
    atlas migrate hash \
        --dir "file://${MIGRATIONS}"
}

status() {
    atlas migrate status \
        --url "sqlite://db/${SQLITEDB}" \
        --dir "file://${MIGRATIONS}"
}

diff() {
    _assert_gt 2 $# "arguments: <dba> <dbb>"
    DB_A=$1
    DB_B=$2
    atlas schema diff \
        --from "sqlite://db/${DB_A}" \
        --to "sqlite://db/${DB_B}" \
        --dev-url "sqlite://file?mode=memory"
}

inspect() {
    _assert_gt 1 $# "arguments: <dba>"
    DB_A=$1
    atlas schema inspect -u "sqlite://db/${DB_A}" 
}

_assert_gt 1 $# "<command-id> [...command arguments]"
"$1" "${@:2:99}"