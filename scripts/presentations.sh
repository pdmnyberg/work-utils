#!/bin/bash

export HELP_TEXT="This scripts contains \
utility functions that work for presentations:"
source scripts/core.sh

_setup_presentation_actions() {
    build() {
        docker compose run --rm --workdir=/opt/build/presentations document-builder make "$@"
    }

    build-diagrams() {
        docker compose run --rm --workdir=/opt/build/diagrams document-builder make "$@"
    }

    _add_action "build" "Build all presentations"
    _add_action "build-diagrams" "Build diagrams using graphviz"
}

presentations_cmd() {
    _setup_presentation_actions
    _run $@
}