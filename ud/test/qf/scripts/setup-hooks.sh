#!/bin/sh
# Enable the project's Git hooks in this clone. Run once after cloning.
set -e
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit scripts/stamp.py scripts/setup-hooks.sh
echo "Git hooks enabled (.githooks)."
