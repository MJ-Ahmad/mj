#!/usr/bin/env python3
"""validate.py

Validate mj.json against schema.json.

Usage:
    python validate.py mj.json schema.json

If 'jsonschema' package is not installed, the script will attempt a minimal structural check.
"""

import json
import sys
from pathlib import Path

def load(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        sys.exit(2)

def minimal_check(data, schema):
    # Basic required keys check
    missing = []
    for key in schema.get('required', []):
        if key not in data:
            missing.append(key)
    if missing:
        print('Minimal validation failed. Missing required keys:', ', '.join(missing))
        return False
    print('Minimal validation passed (required keys present).')
    return True

def main():
    if len(sys.argv) < 3:
        print('Usage: python validate.py mj.json schema.json')
        sys.exit(2)
    mj_path, schema_path = sys.argv[1], sys.argv[2]
    mj = load(mj_path)
    schema = load(schema_path)

    try:
        import jsonschema
        resolver = jsonschema.RefResolver(base_uri='file://' + str(Path(schema_path).resolve()), referrer=schema)
        jsonschema.validate(instance=mj, schema=schema, resolver=resolver)
        print('Validation successful: mj.json conforms to schema.json')
        sys.exit(0)
    except ImportError:
        print('jsonschema not installed; running minimal structural checks.')
        ok = minimal_check(mj, schema)
        sys.exit(0 if ok else 1)
    except jsonschema.ValidationError as e:
        print('Validation error:', e.message)
        sys.exit(1)

if __name__ == '__main__':
    main()