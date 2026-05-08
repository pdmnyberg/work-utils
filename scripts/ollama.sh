#!/bin/bash

export HELP_TEXT="This scripts contains \
utility functions that start and manage ollama:"
source scripts/core.sh

_setup_ollama_actions() {
    CONTAINER_NAME="ollama"
    CONTAINER_VOLUME="ollama"

    start() {
        ${DOCKER} run -d -v ${CONTAINER_VOLUME}:/root/.ollama -p 11434:11434 --name ${CONTAINER_NAME} ollama/ollama
    }

    stop() {
        ${DOCKER} stop ${CONTAINER_NAME}
        ${DOCKER} rm ${CONTAINER_NAME}
    }

    cmd() {
        ${DOCKER} exec -it ${CONTAINER_NAME} ollama "$@"
    }

    run() {
        cmd run "$@"
    }

    _add_action "start" "Start the ollama container"
    _add_action "stop" "Stop and remove the ollama container"
    _add_action "cmd" "Run a ollama command"
    _add_action "run" "Run a model in ollama"
}

ollama_cmd() {
    _setup_ollama_actions
    _run $@
}