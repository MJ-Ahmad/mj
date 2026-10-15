#!/usr/bin/env python3
"""Complete a task once every step is done, and write its archive report.

Usage:
  python3 complete_task.py TASK-000001
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
    build_completion_report,
)


def fail(message):
    print(f"\n{message}\n")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail("Usage: python3 complete_task.py TASK-000001")

    task_id = sys.argv[1].strip().upper()

    data = load_json(DATA_FILE)
    task = find_task(task_id, data)

    if not task:
        fail(f"Task not found: {task_id}")

    if task["status"] == "completed":
        fail("Task already completed.")

    calculate_progress(task)
    progress = task["progress"]

    if progress["remaining"] > 0:
        fail(
            "Task cannot be completed yet.\n"
            f"Completed steps : {progress['completed']}\n"
            f"Remaining steps : {progress['remaining']}"
        )

    stamps = now_stamps()
    overview, evaluation = build_completion_report(task)

    task["status"] = "completed"
    task["completed_dhaka"] = stamps["dhaka"]
    task["completed_utc"] = stamps["utc"]
    task["overview"] = overview
    task["evaluation"] = evaluation
    append_history(task, "Task completed and archived", stamps)

    save_json(DATA_FILE, data)

    print()
    print("=" * 60)
    print("TASK COMPLETED")
    print("=" * 60)
    print()
    print(f"Task ID : {task_id}")
    print(f"Registry: {task['registry']}")
    print(f"Dhaka   : {stamps['dhaka']}")
    print(f"UTC     : {stamps['utc']}")
    print()
    print(overview)
    print()
    print("Evaluation")
    print("-" * 60)
    print(f"Steps total      : {evaluation['steps_total']}")
    print(f"Steps completed  : {evaluation['steps_completed']}")
    print(f"Completion rate  : {evaluation['completion_percentage']}%")
    print(f"Notes            : {evaluation['notes']}")
    print(f"Attachments      : {evaluation['attachments']}")
    print(f"Archive ready    : {evaluation['archive_ready']}")
    print()


if __name__ == "__main__":
    main()
