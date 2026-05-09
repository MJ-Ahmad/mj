#!/usr/bin/env bash
set -euo pipefail
DIR="data/edge_context"
RETENTION_DAYS=${1:-7}
echo "Purging summaries older than $RETENTION_DAYS days in $DIR"
find "$DIR" -type f -name "edge_summary*.json" -mtime +"$RETENTION_DAYS" -print -exec rm -f {} \;
echo "Purge complete."
