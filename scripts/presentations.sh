#!/bin/bash

export HELP_TEXT="This scripts contains \
utility functions that work for presentations:"
source scripts/core.sh

_setup_presentation_actions() {
    build() {
        CURDIR="presentations"

        pushd "$CURDIR"  # Entering presentations working directory

        make all

        popd  # Exiting presentations working directory
    }

    setup() {
        _require_distro "Debian GNU/Linux"
        sudo apt install pandoc texlive-xetex make
    }

    _add_action "build" "Build all presentations"
    _add_action "setup" "Setup environment for presentations"
}

presentations_cmd() {
    _setup_presentation_actions
    _run $@
}