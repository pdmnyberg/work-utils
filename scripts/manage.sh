#!/bin/bash

export HELP_TEXT="This is a management. It contains a number of \
utility functions that aims to simplify the process of development. \
The available actions are as follows:"
source scripts/core.sh

_setup_manage() {
	DOCKER="docker"
	COMPOSE="${DOCKER} compose"
	SCRIPTS="scripts"
	USE_WORKDIR="${WORKDIR:-.}"

	_require_workdir() {
		if [ ! -d "${USE_WORKDIR}" ]; then
			echo -e "${TC}Error${NC}: The working directory does not exist: ${USE_WORKDIR}";
			exit;
		fi
	}

	node() {
		_require_workdir
		${COMPOSE} run --rm --workdir "/opt/output/${USE_WORKDIR}" node node "$@"
	}

	npm() {
		_require_workdir
		${COMPOSE} run --rm --workdir "/opt/output/${USE_WORKDIR}" node npm "$@"
	}

	npx() {
		_require_workdir
		${COMPOSE} run --rm --workdir "/opt/output/${USE_WORKDIR}" node npx "$@"
	}

	go() {
		_require_workdir
		${COMPOSE} run --rm --workdir "/opt/output/${USE_WORKDIR}" go go "$@"
	}

	vm() {
		source "$SCRIPTS/vms.sh"
		vms "$@"
	}

	wip() {
		mkdir -p "wip/$1"
		WORKDIR="wip/$1" ./manage "${@:2:99}"
	}

	presentations() {
		source "$SCRIPTS/presentations.sh"
		presentations_cmd "$@"
	}

	_add_action "node" "Runs command using node"
	_add_action "npm" "Runs command using npm"
	_add_action "npx" "Runs command using npx"
	_add_action "go" "Runs command using go"
	_add_action "vm" "Runs a VM utility command"
	_add_action "wip" "Run any action in WIP workdir. Ex. wip <subdir> <cmd> [...args]"
	_add_action "presentations" "Run presentations utility command"
}

manage() {
	_setup_manage
	_run $@
}