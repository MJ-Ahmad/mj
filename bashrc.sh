#!/usr/bin/env bash
#
# ============================================================================
# MJ Shell Framework
# ============================================================================
#
# Purpose   : Modular Shell Environment Loader
# Maintainer: MJ Ahmad
# Version   : 1.0
#
# Design Principles
# -----------------
# 1. .bashrc remains small and stable.
# 2. All logic lives inside ~/.bash/.
# 3. bootstrap.sh controls module loading.
# 4. Fail safely if framework is incomplete.
# 5. Support long-term scalable architecture.
#
# ============================================================================


# ----------------------------------------------------------------------------
# Framework Root
# ----------------------------------------------------------------------------

export MJ_BASH_HOME="$HOME/.bash"


# ----------------------------------------------------------------------------
# Version
# ----------------------------------------------------------------------------

export MJ_BASH_FRAMEWORK_VERSION="1.0"


# ----------------------------------------------------------------------------
# Bootstrap Loader
# ----------------------------------------------------------------------------

if [[ -f "$MJ_BASH_HOME/bootstrap.sh" ]]; then
    source "$MJ_BASH_HOME/bootstrap.sh"
fi


# ----------------------------------------------------------------------------
# Shell History Configuration
# ----------------------------------------------------------------------------

HISTSIZE=100000
HISTFILESIZE=200000

HISTCONTROL=ignoredups:erasedups

shopt -s histappend

PROMPT_COMMAND="history -a; history -c; history -r"


# ----------------------------------------------------------------------------
# Safer Defaults
# ----------------------------------------------------------------------------

set -o notify


# ----------------------------------------------------------------------------
# Common Convenience Aliases
# ----------------------------------------------------------------------------

alias reload='source "$HOME/.bashrc"'

alias bashrc='nano "$HOME/.bashrc"'

alias mjbash='cd "$HOME/.bash"'


# ----------------------------------------------------------------------------
# Framework Information
# ----------------------------------------------------------------------------

mj_framework_info() {

    printf '\n'

    printf 'MJ Shell Framework\n'

    printf 'Version : %s\n' \
        "$MJ_BASH_FRAMEWORK_VERSION"

    printf 'Home    : %s\n' \
        "$MJ_BASH_HOME"

    printf '\n'
}


# ----------------------------------------------------------------------------
# End Of File
# ----------------------------------------------------------------------------
