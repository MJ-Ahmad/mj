#!/usr/bin/env python3

import json

try:

    with open(
        "data.json"
    ) as f:

        data = json.load(f)

    with open(
        "registry.json"
    ) as f:

        registry = json.load(f)

    print(
        "Database Valid"
    )

    print(
        "Entries:",
        len(data["entries"])
    )

    print(
        "Latest Registry:",
        registry["last_registry"]
    )

except Exception as e:

    print(e)
