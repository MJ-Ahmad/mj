#!/usr/bin/env bash
# Stewardship Task System runner.
# Works from any directory: it always switches to the folder this script lives in.
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"

usage() {
  cat <<'EOF'

Stewardship Task System

Usage:
  ./run.sh init                                   Create folders and data files
  ./run.sh task "Heading" "Description" [opts]    Create a task
        --steps "step one, step two"
        --add-note "note text"          (repeatable)
        --add-file path/to/file         (repeatable)
  ./run.sh track   TASK-000001 <step_id>          Mark a step complete (timestamped)
  ./run.sh complete TASK-000001                   Complete a task (all steps must be done)
  ./run.sh validate                               Check database integrity
  ./run.sh web [port]                             Serve the dashboard (default 8000)

Environment:
  BIND=0.0.0.0 ./run.sh web     Allow other devices on your network (e.g. a phone)

EOF
}

case "${1:-help}" in
  init)
    "$PY" -c "import _lib; _lib.ensure_structure(); print('Ready: data.json, registry.json, attachments/, assets/')"
    ;;
  task)
    shift
    "$PY" add_task.py "$@"
    ;;
  track)
    shift
    "$PY" track_task.py "$@"
    ;;
  complete)
    shift
    "$PY" complete_task.py "$@"
    ;;
  validate)
    "$PY" validate.py
    ;;
  web)
    PORT="${2:-8000}"
    BIND="${BIND:-127.0.0.1}"
    "$PY" -c "import _lib; _lib.ensure_structure()"
    echo "Dashboard: http://${BIND}:${PORT}/"
    exec "$PY" -m http.server "$PORT" --bind "$BIND"
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    usage
    echo "Unknown command: $1" >&2
    exit 1
    ;;
esac
