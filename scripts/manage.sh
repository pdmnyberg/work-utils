#!/bin/bash

export HELP_TEXT="This script contains a number of \
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

	_run_with_workdir() {
		_require_workdir
		${COMPOSE} run --rm --workdir "/opt/output/${USE_WORKDIR}" "$@"
	}

	node() {
		_run_with_workdir node node "$@"
	}

	node-shell() {
		_run_with_workdir --entrypoint bash node
	}

	npm() {
		_run_with_workdir node npm "$@"
	}

	npx() {
		_run_with_workdir node npx "$@"
	}

	go() {
		_run_with_workdir go go "$@"
	}

	python() {
		_run_with_workdir python python "$@"
	}

	python-shell() {
		_run_with_workdir python bash "$@"
	}

	atlas() {
		_run_with_workdir atlas "$@"
	}

	swagger-cli() {
		_run_with_workdir swagger-cli "$@"
	}

	vm() {
		source "$SCRIPTS/vms.sh"
		vms "$@"
	}

	ollama() {
		source "$SCRIPTS/ollama.sh"
		ollama_cmd "$@"
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
	_add_action "node-shell" "Starts a node shell"
	_add_action "atlas" "Runs atlas database migrationt tool"
	_add_action "npm" "Runs command using npm"
	_add_action "npx" "Runs command using npx"
	_add_action "go" "Runs command using go"
	_add_action "python" "Runs command using python"
	_add_action "ollama" "Runs an ollama command"
	_add_action "python-shell" "Run using shell in python container"
	_add_action "swagger-cli" "Run using swagger cli container"
	_add_action "vm" "Runs a VM utility command"
	_add_action "wip" "Run any action in WIP workdir. Ex. wip <subdir> <cmd> [...args]"
	_add_action "presentations" "Run presentations utility command"
}

manage() {
	_setup_manage
	_run $@
}
