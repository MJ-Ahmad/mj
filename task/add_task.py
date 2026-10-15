#!/usr/bin/env python3
"""Create a new task.

Usage:
  python3 add_task.py "Heading" "Description" \
      [--steps "step one, step two"] [--add-note "..."] [--add-file path] \
      [--heading-en "..."] [--heading-bn "..."] [--description-en "..."] [--description-bn "..."]
"""

import os
import argparse

from _lib import (
    ensure_structure,
    load_json,
    save_json,
    DATA_FILE,
    generate_ids,
    now_stamps,
    create_steps,
    store_attachment,
    calculate_progress,
    append_history,
)


def main():
    ensure_structure()

    parser = argparse.ArgumentParser(description="Create a new task.")
    parser.add_argument("heading")
    parser.add_argument("description")
    parser.add_argument("--steps", default="", help="comma-separated step titles")
    parser.add_argument("--add-note", action="append", default=[])
    parser.add_argument("--add-file", action="append", default=[])
    parser.add_argument("--heading-en", default="", help="optional English heading")
    parser.add_argument("--heading-bn", default="", help="optional Bengali heading")
    parser.add_argument("--description-en", default="", help="optional English description")
    parser.add_argument("--description-bn", default="", help="optional Bengali description")
    args = parser.parse_args()

    heading = args.heading.strip()
    description = args.description.strip()

    # Validate everything before allocating IDs, so failed inputs never burn a number.
    if not heading:
        parser.error("heading must not be empty")
    if not description:
        parser.error("description must not be empty")

    missing = [p for p in args.add_file if not os.path.isfile(p)]
    if missing:
        parser.error("file not found: " + ", ".join(missing))

    task_id, reg_id = generate_ids()
    stamps = now_stamps()

    attachments = [
        att for att in (store_attachment(task_id, p) for p in args.add_file) if att
    ]

    translations = {
        "heading_en": args.heading_en.strip(),
        "heading_bn": args.heading_bn.strip(),
        "description_en": args.description_en.strip(),
        "description_bn": args.description_bn.strip(),
    }

    task = {
        "task_id": task_id,
        "registry": reg_id,
        "status": "active",
        "heading": heading,
        "description": description,
        "created_dhaka": stamps["dhaka"],
        "created_utc": stamps["utc"],
        "notes": [n.strip() for n in args.add_note if n.strip()],
        "attachments": attachments,
        "steps": create_steps(args.steps),
        "history": [],
    }

    # Optional per-language fields; the dashboard falls back to heading/description when empty.
    task.update({key: value for key, value in translations.items() if value})

    calculate_progress(task)
    append_history(task, "Task created", stamps)

    data = load_json(DATA_FILE)
    data["tasks"].insert(0, task)
    save_json(DATA_FILE, data)

    print()
    print("Task added successfully")
    print()
    print(f"Task ID  : {task_id}")
    print(f"Registry : {reg_id}")
    print(f"Heading  : {heading}")
    print(f"Created  : {stamps['dhaka']} (Dhaka) / {stamps['utc']} (UTC)")
    print(f"Steps    : {len(task['steps'])}")
    print(f"Files    : {len(attachments)}")
    print()


if __name__ == "__main__":
    main()
