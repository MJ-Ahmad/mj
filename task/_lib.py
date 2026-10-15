#!/usr/bin/env python3
"""Shared core for the Stewardship Task System.

Everything that touches data.json / registry.json goes through this module,
so timestamps, ID generation, atomic writes and validation behave the same
everywhere.
"""

import os
import re
import json
import shutil
import hashlib
import mimetypes
import tempfile
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")
REGISTRY_FILE = os.path.join(BASE_DIR, "registry.json")
ATTACHMENTS_DIR = os.path.join(BASE_DIR, "attachments")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

DHAKA_TZ = timezone(timedelta(hours=6))  # Asia/Dhaka: UTC+06:00, no DST
TS_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

VALID_STATUSES = ("active", "completed")
TASK_ID_RE = re.compile(r"^TASK-\d{6}$")
REG_ID_RE = re.compile(r"^REG-\d{6}$")


# ---------------------------------------------------------------- time

def now_stamps():
    """Return the current moment as Dhaka and UTC strings (millisecond precision)."""
    utc_now = datetime.now(timezone.utc)
    return {
        "dhaka": utc_now.astimezone(DHAKA_TZ).strftime(TS_FORMAT)[:-3],
        "utc": utc_now.strftime(TS_FORMAT)[:-3],
    }


# ---------------------------------------------------------------- storage

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    """Write JSON atomically: a crash mid-write never leaves a broken file."""
    directory = os.path.dirname(path)
    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def ensure_structure():
    """Create the folders and empty data files on first run."""
    os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        save_json(DATA_FILE, {"tasks": []})

    if not os.path.exists(REGISTRY_FILE):
        save_json(REGISTRY_FILE, {"last_registry": 0, "last_task": 0})


# ---------------------------------------------------------------- IDs

def generate_ids():
    """Allocate the next TASK-XXXXXX and REG-XXXXXX identifiers."""
    registry = load_json(REGISTRY_FILE)
    registry["last_registry"] += 1
    registry["last_task"] += 1
    save_json(REGISTRY_FILE, registry)

    task_id = f"TASK-{registry['last_task']:06}"
    reg_id = f"REG-{registry['last_registry']:06}"
    return task_id, reg_id


# ---------------------------------------------------------------- attachments

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def store_attachment(task_id, file_path):
    """Copy a file into attachments/ named after its task, with checksum metadata."""
    if not os.path.isfile(file_path):
        return None

    original = os.path.basename(file_path)
    extension = os.path.splitext(original)[1].lower()
    save_name = f"{task_id}{extension}"
    destination = os.path.join(ATTACHMENTS_DIR, save_name)

    shutil.copy2(file_path, destination)

    return {
        "file": f"attachments/{save_name}",
        "original": original,
        "size": os.path.getsize(destination),
        "mime": mimetypes.guess_type(destination)[0] or "application/octet-stream",
        "sha256": sha256_file(destination),
    }


# ---------------------------------------------------------------- steps

def create_steps(step_string):
    """Turn 'a, b, c' into numbered step records."""
    if not step_string:
        return []

    items = [item.strip() for item in step_string.split(",") if item.strip()]

    return [
        {
            "id": index,
            "title": title,
            "completed": False,
            "completed_dhaka": None,
            "completed_utc": None,
        }
        for index, title in enumerate(items, start=1)
    ]


def calculate_progress(task):
    """Recompute task['progress'] from its steps."""
    total = len(task["steps"])
    completed = sum(1 for step in task["steps"] if step["completed"])

    task["progress"] = {
        "completed": completed,
        "remaining": total - completed,
        "percentage": int(completed / total * 100) if total else 0,
    }


def find_task(task_id, data):
    for task in data["tasks"]:
        if task["task_id"] == task_id:
            return task
    return None


def append_history(task, action, stamps):
    task.setdefault("history", []).append({
        "dhaka": stamps["dhaka"],
        "utc": stamps["utc"],
        "action": action,
    })


# ---------------------------------------------------------------- completion

def build_completion_report(task):
    total = len(task["steps"])
    completed = sum(1 for step in task["steps"] if step["completed"])
    percent = task["progress"]["percentage"]

    overview = (
        "Task execution completed successfully.\n\n"
        f"Task:\n{task['heading']}\n\n"
        "All planned implementation activities\n"
        "have been completed and validated.\n\n"
        "Supporting documentation, evidence files, notes,\n"
        "and execution records have been successfully archived.\n\n"
        f"Completion Rate: {percent}%\n\n"
        "This task is now considered ready for archival,\n"
        "inheritance, future reference, and stewardship review."
    )

    evaluation = {
        "steps_total": total,
        "steps_completed": completed,
        "completion_percentage": percent,
        "notes": len(task.get("notes", [])),
        "attachments": len(task.get("attachments", [])),
        "archive_ready": True,
    }

    return overview, evaluation


# ---------------------------------------------------------------- integrity

def validate_database(data, registry):
    """Return (errors, summary). An empty error list means the database is sound."""
    errors = []

    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        return ["'tasks' must be a list"], {}

    seen_task_ids, seen_reg_ids = set(), set()
    max_task_no = max_reg_no = 0
    total_steps = completed_steps = active = completed = 0

    for task in tasks:
        tid = str(task.get("task_id", "<missing>"))
        rid = str(task.get("registry", "<missing>"))

        if not TASK_ID_RE.match(tid):
            errors.append(f"{tid}: bad task_id format")
        if not REG_ID_RE.match(rid):
            errors.append(f"{tid}: bad registry format ({rid})")

        if tid in seen_task_ids:
            errors.append(f"{tid}: duplicate task_id")
        seen_task_ids.add(tid)

        if rid in seen_reg_ids:
            errors.append(f"{tid}: duplicate registry ({rid})")
        seen_reg_ids.add(rid)

        if TASK_ID_RE.match(tid):
            max_task_no = max(max_task_no, int(tid.split("-")[1]))
        if REG_ID_RE.match(rid):
            max_reg_no = max(max_reg_no, int(rid.split("-")[1]))

        status = task.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{tid}: invalid status '{status}'")

        if not str(task.get("heading", "")).strip():
            errors.append(f"{tid}: empty heading")

        steps = task.get("steps", [])
        step_ids = [s.get("id") for s in steps]
        if len(step_ids) != len(set(step_ids)):
            errors.append(f"{tid}: duplicate step ids")

        for step in steps:
            if step.get("completed"):
                if not step.get("completed_utc") or not step.get("completed_dhaka"):
                    errors.append(f"{tid} step {step.get('id')}: completed without timestamps")
            elif step.get("completed_utc") or step.get("completed_dhaka"):
                errors.append(f"{tid} step {step.get('id')}: timestamps on an incomplete step")

        done = sum(1 for s in steps if s.get("completed"))
        progress = task.get("progress", {})
        if progress.get("completed") != done:
            errors.append(f"{tid}: progress.completed={progress.get('completed')} but {done} steps done")

        if status == "completed" and done != len(steps):
            errors.append(f"{tid}: marked completed with unfinished steps")

        for att in task.get("attachments", []):
            if not os.path.isfile(os.path.join(BASE_DIR, att.get("file", ""))):
                errors.append(f"{tid}: missing attachment file {att.get('file')}")

        total_steps += len(steps)
        completed_steps += done
        if status == "active":
            active += 1
        elif status == "completed":
            completed += 1

    if registry.get("last_task", 0) < max_task_no:
        errors.append("registry.last_task is behind the highest TASK id")
    if registry.get("last_registry", 0) < max_reg_no:
        errors.append("registry.last_registry is behind the highest REG id")

    summary = {
        "total_tasks": len(tasks),
        "active_tasks": active,
        "completed_tasks": completed,
        "total_steps": total_steps,
        "completed_steps": completed_steps,
        "last_registry": registry.get("last_registry", 0),
        "last_task": registry.get("last_task", 0),
    }

    return errors, summary
