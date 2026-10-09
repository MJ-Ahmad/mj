#!/usr/bin/env bash
set -euo pipefail
INPUT="data/edge_context/edge_all_open_tabs.json"
SCRIPT="scripts/import_edge_tabs.js"
if [ ! -f "$INPUT" ]; then
  echo "Input file not found: $INPUT"
  exit 1
fi
echo "Running import script..."
node "$SCRIPT" "$INPUT"
echo "Done. Summary at data/edge_context/edge_summary.json"
