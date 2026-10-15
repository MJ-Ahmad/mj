#!/bin/bash

cd "$(dirname "$0")"

python3 validate.py

echo ""
echo "Dashboard:"
echo "http://127.0.0.1:8000"
echo ""

python3 -m http.server 8000
