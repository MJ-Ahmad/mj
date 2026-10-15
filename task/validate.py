#!/usr/bin/env python3
"""Check data.json and registry.json for consistency. Exit 1 if anything is wrong."""

import sys

from _lib import DATA_FILE, REGISTRY_FILE, load_json, validate_database


def main():
    try:
        data = load_json(DATA_FILE)
        registry = load_json(REGISTRY_FILE)
    except (OSError, ValueError) as exc:
        print(f"\nValidation failed: cannot read database files: {exc}\n")
        sys.exit(1)

    errors, summary = validate_database(data, registry)

    if errors:
        print("\nValidation failed\n")
        for error in errors:
            print(f"  - {error}")
        print(f"\n{len(errors)} problem(s) found.\n")
        sys.exit(1)

    print("\nDatabase validation successful\n")
    print(f"Total tasks      : {summary['total_tasks']}")
    print(f"Active tasks     : {summary['active_tasks']}")
    print(f"Completed tasks  : {summary['completed_tasks']}")
    print(f"Total steps      : {summary['total_steps']}")
    print(f"Completed steps  : {summary['completed_steps']}")
    print(f"Last registry ID : {summary['last_registry']}")
    print(f"Last task ID     : {summary['last_task']}")
    print()


if __name__ == "__main__":
    main()
