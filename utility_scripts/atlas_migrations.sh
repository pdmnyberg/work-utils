#!/bin/bash

# Related atlas documentation can be found here:
# - Creating a baseline: https://atlasgo.io/versioned/apply#existing-databases
# - Creating a diff: https://atlasgo.io/versioned/diff

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
MANAGE_SCRIPT="${SCRIPT_DIR}/../scripts/manage.sh"
source "${MANAGE_SCRIPT}"

MIGRATIONS="${MIGRATIONS:-migrations}"
SQLITEDB="${SQLITEDB:-data.db}"
WORKDIR="${WORKDIR:-.}"

create_baseline_schema() {
    _assert_equal $# 1 "arguments: <migration-name>"
    MIGRATION_NAME=$1
    WORKDIR="$WORKDIR" manage atlas migrate diff "${MIGRATION_NAME}" \
        --dir "file://${MIGRATIONS}" \
        --dev-url "sqlite://file?mode=memory" \
        --to "sqlite://${SQLITEDB}"
}

apply_baseline() {
    _assert_equal $# 1 "arguments: <migration-id>"
    MIGRATION_ID=$1
    WORKDIR="$WORKDIR" manage atlas migrate apply \
        --url "sqlite://${SQLITEDB}" \
        --dir "file://${MIGRATIONS}" \
        --baseline "${MIGRATION_ID}"
}

create_migration() {
    _assert_equal $# 1 "arguments: <migration-name>"
    MIGRATION_NAME=$1
    manage atlas migrate diff "${MIGRATION_NAME}" \
        --dir "file://${MIGRATIONS}" \
        --to "sqlite://${SQLITEDB}" \
        --dev-url "sqlite://file?mode=memory"
}

apply_migrations() {
    manage atlas migrate apply \
        --url "sqlite://${SQLITEDB}" \
        --dir "file://${MIGRATIONS}"
}

rehash() {
    manage atlas migrate hash \
        --dir "file://${MIGRATIONS}"
}

_assert_gt 1 $# "<command-id> [...command arguments]"
"$1" "${@:2:99}"