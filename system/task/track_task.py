#!/usr/bin/env python3
"""Mark one step of a task as completed (timestamped in Dhaka and UTC).

Usage:
  python3 track_task.py TASK-000001 1
"""

import sys

from _lib import (
    DATA_FILE,
    load_json,
    save_json,
    now_stamps,
    find_task,
    calculate_progress,
    append_history,
)


def fail(message):
    print(f"\n{message}\n")
    sys.exit(1)


def main():
    if len(sys.argv) != 3:
        fail("Usage: python3 track_task.py TASK-000001 <step_id>")

    task_id = sys.argv[1].strip().upper()

    try:
        step_id = int(sys.argv[2])
    except ValueError:
        fail("Step ID must be numeric.")

    data = load_json(DATA_FILE)
    task = find_task(task_id, data)

    if not task:
        fail(f"Task not found: {task_id}")

    if task["status"] == "completed":
        fail("Task already completed; steps can no longer be tracked.")

    step = next((s for s in task["steps"] if s["id"] == step_id), None)
    if step is None:
        fail(f"Step not found: {step_id}")

    if step["completed"]:
        print(f"\nStep {step_id} was already completed: {step['title']}\n")
        sys.exit(0)

    stamps = now_stamps()
    step["completed"] = True
    step["completed_dhaka"] = stamps["dhaka"]
    step["completed_utc"] = stamps["utc"]

    calculate_progress(task)
    append_history(task, f"Completed Step {step_id}: {step['title']}", stamps)
    save_json(DATA_FILE, data)

    progress = task["progress"]
    print()
    print("=" * 60)
    print("STEP COMPLETED")
    print("=" * 60)
    print()
    print(f"Task ID : {task_id}")
    print(f"Step ID : {step_id}")
    print(f"Title   : {step['title']}")
    print(f"Dhaka   : {stamps['dhaka']}")
    print(f"UTC     : {stamps['utc']}")
    print()
    print(f"Progress: {progress['completed']} done, "
          f"{progress['remaining']} remaining ({progress['percentage']}%)")
    print()


if __name__ == "__main__":
    main()
