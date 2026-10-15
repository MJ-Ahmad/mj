#!/usr/bin/env bash

# ==========================================
# Safe Bash Script Template
# ==========================================

# Exit immediately on errors
set -e

# Exit on undefined variables
set -u

# Fail pipelines if any command fails
set -o pipefail

# Restrictive file permissions for created files
umask 027

# Script metadata
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cleanup function
cleanup() {
    echo "[INFO] Cleaning up..."
}

# Error handler
error_handler() {
    local exit_code=$?
    echo "[ERROR] ${SCRIPT_NAME} failed on line ${BASH_LINENO[0]} with exit code ${exit_code}" >&2
    cleanup
    exit "$exit_code"
}

trap error_handler ERR
trap cleanup EXIT

# Logging helpers
log_info() {
    echo "[INFO] $*"
}

log_warn() {
    echo "[WARN] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

# Check required commands
require_command() {
    command -v "$1" >/dev/null 2>&1 || {
        log_error "Required command not found: $1"
        exit 1
    }
}

# Example dependency checks
require_command bash
require_command grep
require_command sed

# Validate arguments
if [[ $# -lt 1 ]]; then
    echo "Usage: $SCRIPT_NAME <input>"
    exit 1
fi

INPUT="$1"

# Validate input
if [[ -z "$INPUT" ]]; then
    log_error "Input cannot be empty."
    exit 1
fi

log_info "Starting script..."
log_info "Script directory: $SCRIPT_DIR"
log_info "Input: $INPUT"

# ==========================================
# Main Logic
# ==========================================

main() {
    log_info "Processing..."

    # Example safe file test
    if [[ -f "$INPUT" ]]; then
        log_info "File exists."
    else
        log_warn "File not found: $INPUT"
    fi

    log_info "Completed successfully."
}

main

exit 0
