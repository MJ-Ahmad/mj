# attendance.py
import json
import os
import shutil
import tempfile
from datetime import datetime, date
from pathlib import Path
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

from students import STUDENTS, TEACHERS

BASE_DIR = Path(__file__).parent
OUTPUTS = BASE_DIR / "outputs"
MASTER_DIR = BASE_DIR / "master"
TEMPLATES = BASE_DIR / "templates"
ASSETS = BASE_DIR / "assets"
LOGO_PATH = ASSETS / "logo.png"  # place your logo here

OUTPUTS.mkdir(exist_ok=True)
MASTER_DIR.mkdir(exist_ok=True)
TEMPLATES.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)

MASTER_JSON = MASTER_DIR / "attendance_master.json"
MASTER_HTML = MASTER_DIR / "attendance_master.html"
MASTER_MD = MASTER_DIR / "attendance_master.md"

ATTENDANCE_OPTIONS = {
    "1": {"code": "present", "label": "Present"},
    "2": {"code": "absent", "label": "Absent"},
    "3": {"code": "late", "label": "Late"},
    "4": {"code": "excused", "label": "Excused"},
}

DEFAULT_SCHEDULE_TIMES = ["04:00", "12:15", "14:30", "18:30"]

def now_iso():
    tz = None
    if ZoneInfo:
        try:
            tz = ZoneInfo("Asia/Dhaka")
        except Exception:
            tz = None
    dt = datetime.now(tz) if tz else datetime.now()
    return dt.isoformat(timespec="seconds")

def atomic_write(path: Path, data: str, encoding="utf-8"):
    # write to temp file then rename for atomicity
    fd, tmp = tempfile.mkstemp(dir=str(path.parent))
    with os.fdopen(fd, "w", encoding=encoding) as f:
        f.write(data)
    os.replace(tmp, str(path))

def load_master():
    if MASTER_JSON.exists():
        with open(MASTER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    # initialize master structure
    return {"madrasha": "Baitul Quran International Madrasha", "records": []}

def save_master_json(master):
    atomic_write(MASTER_JSON, json.dumps(master, ensure_ascii=False, indent=2))

def append_snapshot(meta, attendance):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"attendance_snapshot_{ts}"
    snapshot = {"meta": meta, "attendance": attendance}
    with open(OUTPUTS / (base + ".json"), "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    with open(OUTPUTS / (base + ".md"), "w", encoding="utf-8") as f:
        f.write(render_markdown(meta, attendance))
    with open(OUTPUTS / (base + ".html"), "w", encoding="utf-8") as f:
        f.write(render_html(meta, attendance))

def render_html(meta, attendance):
    # header and footer templates (if present)
    header_html = ""
    footer_html = ""
    header_file = TEMPLATES / "header.html"
    footer_file = TEMPLATES / "footer.html"
    css_file = TEMPLATES / "template.css"
    css = ""
    if css_file.exists():
        css = "<style>\n" + css_file.read_text(encoding="utf-8") + "\n</style>"
    if header_file.exists():
        header_html = header_file.read_text(encoding="utf-8")
    else:
        # default header with logo
        logo_tag = f'<img src="../assets/logo.png" alt="logo" style="height:60px;vertical-align:middle;margin-right:12px">' if LOGO_PATH.exists() else ""
        header_html = f"<div style='display:flex;align-items:center'>{logo_tag}<div><h2>{meta['madrasha']}</h2><div>{meta['address']}</div></div></div><hr>"
    if footer_file.exists():
        footer_html = footer_file.read_text(encoding="utf-8")
    else:
        footer_html = f"<hr><div style='font-size:0.9em;color:#666'>Generated: {meta['timestamp']} | Curated by: {meta.get('curated_by','')}</div>"

    rows = ""
    for a in attendance:
        rows += "<tr>"
        rows += f"<td>{a['roll']}</td>"
        rows += f"<td>{a['student_id']}</td>"
        rows += f"<td>{a['name']}</td>"
        rows += f"<td>{a['department']}</td>"
        rows += f"<td>{a['status_label']}</td>"
        rows += f"<td>{a.get('note','')}</td>"
        rows += "</tr>\n"

    teachers_html = "<ul>"
    for t in meta.get("teachers", []):
        teachers_html += f"<li>{t['name']} ({t.get('id','')}) — {t.get('phone','')}</li>"
    teachers_html += "</ul>"

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Attendance Master</title>
{css}
</head>
<body>
{header_html}
<h3>Attendance — {meta['mode']} — {meta['date']}</h3>
<p><strong>Department:</strong> {meta['department']} &nbsp; | &nbsp; <strong>Scheduled time:</strong> {meta['scheduled_time']} &nbsp; | &nbsp; <strong>Recorded by:</strong> {meta.get('recorder','')}</p>
<h4>Teachers</h4>
{teachers_html}
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%">
<thead><tr><th>Roll</th><th>Student ID</th><th>Name</th><th>Department</th><th>Status</th><th>Note</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
{footer_html}
</body>
</html>
"""
    return html

def render_markdown(meta, attendance):
    md = f"# Attendance — {meta['mode']} — {meta['date']}\n\n"
    md += f"**Department:** {meta['department']}\n\n"
    md += f"**Scheduled time:** {meta['scheduled_time']}\n\n"
    md += f"**Recorded by:** {meta.get('recorder','')}\n\n"
    md += "| Roll | Student ID | Name | Department | Status | Note |\n"
    md += "|------|------------|------|------------|--------|------|\n"
    for a in attendance:
        note = a.get("note","")
        md += f"| {a['roll']} | {a['student_id']} | {a['name']} | {a['department']} | {a['status_label']} | {note} |\n"
    md += f"\nGenerated: {meta['timestamp']}\n"
    return md

def update_master(master, meta, attendance):
    # append a new record to master
    record = {"meta": meta, "attendance": attendance}
    master["records"].append(record)
    return master

def save_master_files(master):
    # save JSON master
    save_master_json(master)
    # render combined HTML master (concatenate records)
    html_parts = []
    for rec in master["records"]:
        html_parts.append(render_html(rec["meta"], rec["attendance"]))
    combined_html = "<!-- Master Attendance File -->\n" + "\n<hr/>\n".join(html_parts)
    atomic_write(MASTER_HTML, combined_html)
    # render combined markdown
    md_parts = []
    for rec in master["records"]:
        md_parts.append(render_markdown(rec["meta"], rec["attendance"]))
    atomic_write(MASTER_MD, "\n\n---\n\n".join(md_parts))

def save_master_json(master):
    atomic_write(MASTER_JSON, json.dumps(master, ensure_ascii=False, indent=2))

def choose_date():
    print("Enter date for attendance (YYYY-MM-DD) or press Enter for today:")
    s = input("Date: ").strip()
    if not s:
        return date.today().isoformat()
    try:
        d = datetime.fromisoformat(s)
        return d.date().isoformat()
    except Exception:
        print("Invalid format, using today.")
        return date.today().isoformat()

def choose_department():
    depts = sorted({s["department"] for s in STUDENTS})
    for i, d in enumerate(depts, start=1):
        print(f"{i}. {d}")
    print(f"{len(depts)+1}. All")
    sel = input("Choose department number: ").strip()
    try:
        idx = int(sel)
        if 1 <= idx <= len(depts):
            return depts[idx-1]
        if idx == len(depts)+1:
            return "All"
    except Exception:
        pass
    return "All"

def choose_scheduled_time():
    print("Choose scheduled time or enter custom (HH:MM):")
    for i, t in enumerate(DEFAULT_SCHEDULE_TIMES, start=1):
        print(f"{i}. {t}")
    print(f"{len(DEFAULT_SCHEDULE_TIMES)+1}. Custom")
    sel = input("Choose: ").strip()
    try:
        idx = int(sel)
        if 1 <= idx <= len(DEFAULT_SCHEDULE_TIMES):
            return DEFAULT_SCHEDULE_TIMES[idx-1]
        if idx == len(DEFAULT_SCHEDULE_TIMES)+1:
            custom = input("Enter time (HH:MM): ").strip()
            return custom
    except Exception:
        pass
    return DEFAULT_SCHEDULE_TIMES[0]

def select_students(department):
    if department == "All":
        return STUDENTS
    return [s for s in STUDENTS if s["department"] == department]

def collect_attendance_for_students(students):
    attendance = []
    for s in students:
        while True:
            print(f"\nStudent: {s['name']}  Roll: {s['roll']}  ID: {s['id']}")
            for k, opt in ATTENDANCE_OPTIONS.items():
                print(f"  {k}. {opt['label']}")
            choice = input("Status (number): ").strip()
            if choice in ATTENDANCE_OPTIONS:
                note = input("Optional note (press Enter to skip): ").strip()
                attendance.append({
                    "name": s["name"],
                    "roll": s["roll"],
                    "student_id": s["id"],
                    "department": s["department"],
                    "status": ATTENDANCE_OPTIONS[choice]["code"],
                    "status_label": ATTENDANCE_OPTIONS[choice]["label"],
                    "note": note,
                })
                break
            else:
                print("Invalid option. Try again.")
    return attendance

def collect_teacher_attendance():
    print("\nRecord teacher attendance (who is present among teachers):")
    teacher_att = []
    for i, t in enumerate(TEACHERS, start=1):
        print(f"{i}. {t['name']} ({t.get('phone','')})")
    print("Enter numbers separated by commas for present teachers (e.g., 1,3) or press Enter if none:")
    sel = input("Present teachers: ").strip()
    present = []
    if sel:
        for part in sel.split(","):
            try:
                idx = int(part.strip()) - 1
                if 0 <= idx < len(TEACHERS):
                    present.append(TEACHERS[idx])
            except Exception:
                continue
    return present

def choose_recorder():
    print("\nWho is recording this attendance?")
    for i, t in enumerate(TEACHERS, start=1):
        print(f"{i}. {t['name']}")
    sel = input("Choose recorder number: ").strip()
    try:
        idx = int(sel) - 1
        if 0 <= idx < len(TEACHERS):
            return TEACHERS[idx]["name"]
    except Exception:
        pass
    return ""

def main():
    print("=== Baitul Quran International Madrasha — Attendance (Production) ===")
    print("Modes: 1. Daily  2. Class-based  3. Group-based")
    mode = input("Choose mode (1/2/3): ").strip()
    mode_label = {"1": "Daily", "2": "Class-based", "3": "Group-based"}.get(mode, "Daily")
    att_date = choose_date()
    department = choose_department()
    scheduled_time = choose_scheduled_time()
    recorder = choose_recorder()
    students = select_students(department)
    print(f"\nRecording attendance for {department} on {att_date} at {scheduled_time}")
    attendance = collect_attendance_for_students(students)
    teacher_present = collect_teacher_attendance()
    meta = {
        "madrasha": "Baitul Quran International Madrasha",
        "address": "Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh",
        "curated_by": "MJ Ahmad — Steward of Ethical Inheritance",
        "mode": mode_label,
        "date": att_date,
        "timestamp": now_iso(),
        "department": department,
        "scheduled_time": scheduled_time,
        "recorder": recorder,
        "teachers": TEACHERS,
        "teachers_present": teacher_present,
    }
    # append to master
    master = load_master()
    master = update_master(master, meta, attendance)
    save_master_files(master)
    # snapshot for audit
    append_snapshot(meta, attendance)
    print("\nSaved master files and snapshot. Master files are in 'master/' and snapshots in 'outputs/'.")

if __name__ == "__main__":
    main()
