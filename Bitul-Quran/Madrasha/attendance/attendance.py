#!/usr/bin/env python3
"""
attendance.py

Production-ready CLI attendance recorder for Baitul Quran International Madrasha.

Features
- Menu-driven: choose mode (Daily/Class/Group), date, department, scheduled time.
- Records student attendance and teacher presence; records who recorded the session.
- Appends a new record to master/attendance_master.json (atomic write).
- Updates master/attendance_master.md by inserting a Markdown section under "Attendance Records (master)".
- Writes timestamped snapshots to outputs/ (json, md, html).
- Robust recovery if master JSON is missing, empty, or corrupted (backups corrupt file).
- Uses only Python standard library.
- Expects students.py in same folder providing STUDENTS and TEACHERS lists.

Usage
    python attendance.py
"""

from __future__ import annotations
import json
import os
import shutil
import tempfile
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Any

# Attempt to use zoneinfo for Asia/Dhaka timestamps when available
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Asia/Dhaka")
except Exception:
    TZ = None

# Project paths
BASE = Path(__file__).parent.resolve()
MASTER_DIR = BASE / "master"
OUTPUTS_DIR = BASE / "outputs"
TEMPLATES_DIR = BASE / "templates"
ASSETS_DIR = BASE / "assets"

MASTER_JSON = MASTER_DIR / "attendance_master.json"
MASTER_MD = MASTER_DIR / "attendance_master.md"
MASTER_HTML = MASTER_DIR / "attendance_master.html"  # optional viewer (static)
RECOVERY_LOG = MASTER_DIR / "recovery.log"

# Ensure directories exist
MASTER_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Import students and teachers from students.py (single source of truth)
try:
    from students import STUDENTS, TEACHERS  # type: ignore
except Exception:
    # Fallback empty lists if students.py missing; user should provide students.py
    STUDENTS: List[Dict[str, str]] = []
    TEACHERS: List[Dict[str, str]] = []

# Attendance options
ATTENDANCE_OPTIONS = {
    "1": {"code": "present", "label": "Present"},
    "2": {"code": "absent", "label": "Absent"},
    "3": {"code": "late", "label": "Late"},
    "4": {"code": "excused", "label": "Excused"},
}

DEFAULT_SCHEDULE_TIMES = ["04:00", "12:15", "14:30", "18:30"]


# -------------------------
# Utility helpers
# -------------------------
def now_iso() -> str:
    dt = datetime.now(TZ) if TZ else datetime.now()
    # include offset if TZ available
    if TZ:
        return dt.isoformat(timespec="seconds")
    return dt.isoformat(timespec="seconds")


def timestamp_for_filename() -> str:
    dt = datetime.now(TZ) if TZ else datetime.now()
    return dt.strftime("%Y%m%d_%H%M%S")


def atomic_write(path: Path, text: str, encoding: str = "utf-8") -> None:
    """Write text to path atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(text)
        os.replace(tmp, str(path))
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass


def append_recovery_log(message: str) -> None:
    try:
        with open(RECOVERY_LOG, "a", encoding="utf-8") as f:
            f.write(f"{now_iso()} - {message}\n")
    except Exception:
        pass


# -------------------------
# Master JSON load & recovery
# -------------------------
def load_master() -> Dict[str, Any]:
    """
    Load master JSON. If missing or corrupted, back it up and return a fresh master structure.
    """
    default_master = {
        "madrasha": {
            "name": "Baitul Quran International Madrasha",
            "address": "Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh",
            "curated_by": "MJ Ahmad — Steward of Ethical Inheritance",
            "document_type": "Institutional Record",
            "logo": str((ASSETS_DIR / "logo.png").as_posix()),
            "last_updated": now_iso(),
        },
        "teachers": TEACHERS,
        "records": []
    }

    if not MASTER_JSON.exists():
        # create initial master file
        atomic_write(MASTER_JSON, json.dumps(default_master, ensure_ascii=False, indent=2))
        return default_master

    try:
        text = MASTER_JSON.read_text(encoding="utf-8").strip()
        if not text:
            raise ValueError("Master JSON is empty")
        data = json.loads(text)
        # ensure expected keys
        if "records" not in data:
            data.setdefault("records", [])
        return data
    except Exception as exc:
        # backup corrupt file
        ts = timestamp_for_filename()
        backup = MASTER_JSON.with_name(f"attendance_master_corrupt_{ts}.json")
        try:
            shutil.move(str(MASTER_JSON), str(backup))
            append_recovery_log(f"Backed up corrupt master to {backup.name}: {exc}")
        except Exception:
            # fallback: copy then truncate original
            try:
                shutil.copy2(str(MASTER_JSON), str(backup))
                MASTER_JSON.unlink(missing_ok=True)
                append_recovery_log(f"Copied corrupt master to {backup.name}: {exc}")
            except Exception as e2:
                append_recovery_log(f"Failed to backup corrupt master: {e2}")
        # write fresh master with recovery note
        default_master["recovery"] = {
            "recovered_at": now_iso(),
            "note": f"Previous master was corrupt or invalid JSON. Backup: {backup.name}"
        }
        atomic_write(MASTER_JSON, json.dumps(default_master, ensure_ascii=False, indent=2))
        return default_master


# -------------------------
# Master update & snapshot
# -------------------------
def append_record_to_master(master: Dict[str, Any], meta: Dict[str, Any], attendance: List[Dict[str, Any]]) -> Dict[str, Any]:
    record = {"meta": meta, "attendance": attendance}
    master.setdefault("records", []).append(record)
    # update last_updated
    master.setdefault("madrasha", {})["last_updated"] = now_iso()
    return master


def save_master_json(master: Dict[str, Any]) -> None:
    atomic_write(MASTER_JSON, json.dumps(master, ensure_ascii=False, indent=2))


def render_record_markdown(meta: Dict[str, Any], attendance: List[Dict[str, Any]]) -> str:
    header = (
        f"### Record: {meta.get('date','')} — {meta.get('department','')} ({meta.get('scheduled_time','')})\n"
        f"**Record ID:** `{meta.get('id','')}`  \n"
        f"**Mode:** {meta.get('mode','')}  \n"
        f"**Date:** {meta.get('date','')}  \n"
        f"**Scheduled time:** {meta.get('scheduled_time','')}  \n"
        f"**Recorded by:** {meta.get('recorder','')}  \n"
        f"**Teachers present:** {', '.join(meta.get('teachers_present', []))}  \n"
        f"**Timestamp:** {meta.get('timestamp','')}\n\n"
    )
    table = "| Roll | Student ID | Name | Department | Status | Note |\n|------|------------|------|------------|--------|------|\n"
    for a in attendance:
        note = a.get("note", "").replace("\n", " ")
        table += f"| {a.get('roll','')} | {a.get('student_id','')} | {a.get('name','')} | {a.get('department','')} | {a.get('status_label','')} | {note} |\n"
    return header + table + "\n"


def update_master_markdown_append(meta: Dict[str, Any], attendance: List[Dict[str, Any]]) -> None:
    """
    Insert the new record section under the "Attendance Records (master)" heading.
    If the heading is not found, append at the end.
    """
    new_section = render_record_markdown(meta, attendance)
    if not MASTER_MD.exists():
        # create a minimal master md with a placeholder
        initial = (
            "# 🕌 Baitul Quran International Madrasha\n"
            f"**Address:** {meta.get('address','')}  \n"
            f"**Curated by:** {meta.get('curated_by','')}  \n"
            f"**Document Type:** {meta.get('document_type','Institutional Record')}  \n"
            f"**Last Updated:** {meta.get('timestamp','')}\n\n"
            "---\n\n"
            "## Attendance Records (master)\n\n"
        )
        atomic_write(MASTER_MD, initial + new_section)
        return

    text = MASTER_MD.read_text(encoding="utf-8")
    marker = "## Attendance Records (master)"
    if marker in text:
        parts = text.split(marker, 1)
        before = parts[0] + marker + "\n\n"
        after = parts[1]
        # insert new section at top of records area
        new_text = before + new_section + after
        atomic_write(MASTER_MD, new_text)
    else:
        # append at end
        new_text = text + "\n\n## Attendance Records (master)\n\n" + new_section
        atomic_write(MASTER_MD, new_text)


def append_snapshot(meta: Dict[str, Any], attendance: List[Dict[str, Any]]) -> None:
    ts = timestamp_for_filename()
    base = f"attendance_snapshot_{ts}"
    snapshot = {"meta": meta, "attendance": attendance}
    # JSON snapshot
    with open(OUTPUTS_DIR / (base + ".json"), "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    # Markdown snapshot
    with open(OUTPUTS_DIR / (base + ".md"), "w", encoding="utf-8") as f:
        f.write(render_record_markdown(meta, attendance))
    # Optional: render a simple HTML snapshot (minimal)
    html = render_simple_html_snapshot(meta, attendance)
    with open(OUTPUTS_DIR / (base + ".html"), "w", encoding="utf-8") as f:
        f.write(html)


def render_simple_html_snapshot(meta: Dict[str, Any], attendance: List[Dict[str, Any]]) -> str:
    rows = ""
    for a in attendance:
        rows += "<tr>"
        rows += f"<td>{a.get('roll','')}</td>"
        rows += f"<td>{a.get('student_id','')}</td>"
        rows += f"<td>{a.get('name','')}</td>"
        rows += f"<td>{a.get('department','')}</td>"
        rows += f"<td>{a.get('status_label','')}</td>"
        rows += f"<td>{a.get('note','')}</td>"
        rows += "</tr>\n"
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Attendance Snapshot {meta.get('id','')}</title>
<style>body{{font-family:Arial,Helvetica,sans-serif}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:8px}}</style>
</head><body>
<h2>{meta.get('madrasha_name','Baitul Quran International Madrasha')}</h2>
<p><strong>Date:</strong> {meta.get('date','')} &nbsp; <strong>Time:</strong> {meta.get('scheduled_time','')}</p>
<table><thead><tr><th>Roll</th><th>Student ID</th><th>Name</th><th>Department</th><th>Status</th><th>Note</th></tr></thead><tbody>
{rows}
</tbody></table>
<p>Recorded by: {meta.get('recorder','')}</p>
</body></html>"""
    return html


# -------------------------
# CLI helpers
# -------------------------
def choose_mode() -> str:
    print("Choose attendance mode:")
    print("  1. Daily")
    print("  2. Class-based")
    print("  3. Group-based")
    sel = input("Mode (1/2/3) [1]: ").strip() or "1"
    return {"1": "Daily", "2": "Class-based", "3": "Group-based"}.get(sel, "Daily")


def choose_date() -> str:
    s = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not s:
        return date.today().isoformat()
    try:
        d = datetime.fromisoformat(s)
        return d.date().isoformat()
    except Exception:
        print("Invalid date format, using today.")
        return date.today().isoformat()


def choose_department() -> str:
    depts = sorted({s.get("department", "Unknown") for s in STUDENTS})
    for i, d in enumerate(depts, start=1):
        print(f"  {i}. {d}")
    print(f"  {len(depts)+1}. All")
    sel = input(f"Choose department number [All]: ").strip()
    try:
        idx = int(sel)
        if 1 <= idx <= len(depts):
            return depts[idx - 1]
        if idx == len(depts) + 1:
            return "All"
    except Exception:
        pass
    return "All"


def choose_scheduled_time() -> str:
    print("Choose scheduled time or enter custom:")
    for i, t in enumerate(DEFAULT_SCHEDULE_TIMES, start=1):
        print(f"  {i}. {t}")
    print(f"  {len(DEFAULT_SCHEDULE_TIMES)+1}. Custom")
    sel = input("Choose: ").strip()
    try:
        idx = int(sel)
        if 1 <= idx <= len(DEFAULT_SCHEDULE_TIMES):
            return DEFAULT_SCHEDULE_TIMES[idx - 1]
        if idx == len(DEFAULT_SCHEDULE_TIMES) + 1:
            custom = input("Enter time (HH:MM): ").strip()
            return custom
    except Exception:
        pass
    return DEFAULT_SCHEDULE_TIMES[0]


def select_students_for_department(department: str) -> List[Dict[str, str]]:
    if department == "All":
        return STUDENTS
    return [s for s in STUDENTS if s.get("department") == department]


def collect_attendance_for_students(students: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    attendance = []
    for s in students:
        while True:
            print(f"\nStudent: {s.get('name','')}  Roll: {s.get('roll','')}  ID: {s.get('id','')}")
            for k, opt in ATTENDANCE_OPTIONS.items():
                print(f"  {k}. {opt['label']}")
            choice = input("Status (number): ").strip()
            if choice in ATTENDANCE_OPTIONS:
                note = input("Optional note (press Enter to skip): ").strip()
                attendance.append({
                    "name": s.get("name",""),
                    "roll": s.get("roll",""),
                    "student_id": s.get("id",""),
                    "department": s.get("department",""),
                    "status": ATTENDANCE_OPTIONS[choice]["code"],
                    "status_label": ATTENDANCE_OPTIONS[choice]["label"],
                    "note": note,
                })
                break
            else:
                print("Invalid option. Try again.")
    return attendance


def collect_teacher_presence() -> List[str]:
    print("\nRecord teacher attendance (who is present among teachers):")
    for i, t in enumerate(TEACHERS, start=1):
        print(f"  {i}. {t.get('name','')} ({t.get('phone','')})")
    sel = input("Enter numbers separated by commas for present teachers (e.g., 1,3) or press Enter if none: ").strip()
    present_ids = []
    if sel:
        for part in sel.split(","):
            try:
                idx = int(part.strip()) - 1
                if 0 <= idx < len(TEACHERS):
                    present_ids.append(TEACHERS[idx].get("id", TEACHERS[idx].get("name","")))
            except Exception:
                continue
    return present_ids


def choose_recorder() -> str:
    print("\nWho is recording this attendance?")
    for i, t in enumerate(TEACHERS, start=1):
        print(f"  {i}. {t.get('name','')}")
    sel = input("Choose recorder number or press Enter to leave blank: ").strip()
    try:
        idx = int(sel) - 1
        if 0 <= idx < len(TEACHERS):
            return TEACHERS[idx].get("name","")
    except Exception:
        pass
    return ""


# -------------------------
# Main flow
# -------------------------
def main() -> None:
    print("=== Baitul Quran International Madrasha — Attendance (Production) ===")
    mode = choose_mode()
    att_date = choose_date()
    department = choose_department()
    scheduled_time = choose_scheduled_time()
    recorder = choose_recorder()
    students = select_students_for_department(department)
    if not students:
        print("No students found for the selected department. Exiting.")
        return

    print(f"\nRecording attendance for {department} on {att_date} at {scheduled_time}")
    attendance = collect_attendance_for_students(students)
    teachers_present = collect_teacher_presence()

    # Build meta
    rec_id = f"rec_{timestamp_for_filename()}"
    meta = {
        "id": rec_id,
        "madrasha_name": "Baitul Quran International Madrasha",
        "address": "Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh",
        "curated_by": "MJ Ahmad — Steward of Ethical Inheritance",
        "document_type": "Institutional Record",
        "mode": mode,
        "date": att_date,
        "timestamp": now_iso(),
        "department": department,
        "scheduled_time": scheduled_time,
        "recorder": recorder,
        "teachers_present": teachers_present,
    }

    # Load master, append record, save master JSON
    master = load_master()
    master = append_record_to_master(master, meta, attendance)
    save_master_json(master)

    # Update master markdown (append new section)
    try:
        update_master_markdown_append(meta, attendance)
    except Exception as e:
        append_recovery_log(f"Failed to update master markdown: {e}")

    # Append snapshot files for audit
    try:
        append_snapshot(meta, attendance)
    except Exception as e:
        append_recovery_log(f"Failed to write snapshot: {e}")

    print("\nSaved master record and snapshot.")
    print(f"Master JSON: {MASTER_JSON}")
    print(f"Master Markdown: {MASTER_MD}")
    print(f"Snapshots: {OUTPUTS_DIR}")

if __name__ == "__main__":
    main()
