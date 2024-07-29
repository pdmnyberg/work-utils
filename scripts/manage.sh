#!/bin/bash

manage() {
	local ACTIONS
	local HELP_SECTIONS
	local COMPOSE
	local SCRIPTS
	local TEST_RESULTS="${TEST_RESULTS:-.test-results}"
	local USE_WORKDIR="${WORKDIR:-.}"

	_setup_actions() {
		DOCKER="docker"
		COMPOSE="${DOCKER} compose"
		SCRIPTS="scripts"

		node() {
            ${COMPOSE} run --workdir "/opt/output/${USE_WORKDIR}" node node "$@"
        }

        npm() {
            ${COMPOSE} run --workdir "/opt/output/${USE_WORKDIR}" node npm "$@"
        }

		npx() {
            ${COMPOSE} run --workdir "/opt/output/${USE_WORKDIR}" node npx "$@"
        }

		go() {
            ${COMPOSE} run --workdir "/opt/output/${USE_WORKDIR}" go go "$@"
        }

		help() {
			_setup_actions

			echo "This is a management. It contains a number of \
utility functions that aims to simplify the process of development. \
The available actions are as follows:"
			local AC='\e[0;32m'
			local NC='\e[0m'
			for action_index in "${!ACTIONS[@]}"
			do
				echo -e " - ${AC}${ACTIONS[$action_index]}${NC}: ${HELP_SECTIONS[$action_index]}"
			done
		}

		ACTIONS=()
		HELP_SECTIONS=()

		_add_action() {
			ACTIONS+=("$1")
			HELP_SECTIONS+=("$2")
		}

		_add_action "help" "Display help message and a list of available commands"
		_add_action "node" "Runs command using node"
		_add_action "npm" "Runs command using npm"
		_add_action "npx" "Runs command using npx"
        _add_action "go" "Runs command using go"
	}

	_setup_actions

	local action="$1"
	local TC='\e[0;31m'
	local NC='\e[0m'
	if [ -n "$action" ] && grep -qF -w -e "$action" <<<"${ACTIONS[*]}"
	then
		if [ -d "${USE_WORKDIR}" ]; then
			echo -e "${TC}# Running: $action${NC}"
			"$action" "${@:2:99}"
		else
			echo -e "${TC}Error${NC}: The working directory does not exist: ${USE_WORKDIR}"
		fi
	else
		echo -e "${TC}# Manage script for PLUPP project${NC}"
		help
	fi
}

# When running as standalone we want the autocomplete items
# to be added by default.
if [ "${MANAGE_ENABLE_AUTO_COMPLETE-yes}" = "yes" ]
then
	manage auto-complete
fi