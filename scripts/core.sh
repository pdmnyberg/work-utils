#!/bin/bash

HELP_TEXT=${HELP_TEXT:-"This is a management script."}

_setup_actions() {
    ACTIONS=()
    HELP_SECTIONS=()

    help() {
        echo "$HELP_TEXT"
        local AC='\e[0;32m'
        local NC='\e[0m'
        for action_index in "${!ACTIONS[@]}"
        do
            echo -e " - ${AC}${ACTIONS[$action_index]}${NC}: ${HELP_SECTIONS[$action_index]}"
        done
    }

    _add_action() {
        ACTIONS+=("$1")
        HELP_SECTIONS+=("$2")
    }

    _run() {
        local action="$1"
        local TC='\e[0;31m'
        local NC='\e[0m'
        if [ -n "$action" ] && grep -qF -w -e "$action" <<<"${ACTIONS[*]}"
        then
            echo -e "${TC}# Running: $action${NC}"
            "$action" "${@:2:99}"
        else
            echo -e "${TC}# Manage script${NC}"
            help
        fi
    }

    _add_action "help" "Display help message and a list of available commands"
}

_setup_actions
