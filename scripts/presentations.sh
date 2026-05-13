#!/bin/bash

export HELP_TEXT="This scripts contains \
utility functions that work for presentations:"

_setup_presentation_actions() {
    source "${SCRIPTS}/core.sh"

    DOCKER="${DOCKER:-docker}"
    DOCUMENT_BUILDER_NAME="document-builder"

    _run_container() {
        ${DOCKER} build --tag "${DOCUMENT_BUILDER_NAME}" -f "${SCRIPTS}/containers/document-builder.Dockerfile" "${SCRIPTS}"
		${DOCKER} run \
			-it \
			--rm \
			--user $(id -u):$(id -g) \
			-v ./:/opt/output \
            -v ./presentations:/opt/build/presentations \
            -v ./diagrams:/opt/build/diagrams \
			"$@"
	}

    build() {
        _run_container --workdir=/opt/build/presentations "${DOCUMENT_BUILDER_NAME}" make "$@"
    }

    build-diagrams() {
        _run_container --workdir=/opt/build/diagrams "${DOCUMENT_BUILDER_NAME}" make "$@"
    }

    _add_action "build" "Build all presentations"
    _add_action "build-diagrams" "Build diagrams using graphviz"
}

presentations_cmd() {
    _setup_presentation_actions
    _run $@
}