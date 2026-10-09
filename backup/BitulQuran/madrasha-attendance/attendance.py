# attendance.py
import json
import os
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

from students import STUDENTS, TEACHERS

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ATTENDANCE_OPTIONS = {
    "1": {"code": "present", "label": "Present"},
    "2": {"code": "absent", "label": "Absent"},
    "3": {"code": "late", "label": "Late"},
    "4": {"code": "excused", "label": "Excused"},
}

SCHEDULES = {
    "1": {"label": "Daily (main)", "times": ["04:00", "12:15", "14:30", "18:30"]},
    "2": {"label": "Class-based", "times": []},
    "3": {"label": "Group-based", "times": []},
}

def now_iso():
    tz = None
    if ZoneInfo:
        try:
            tz = ZoneInfo("Asia/Dhaka")
        except Exception:
            tz = None
    dt = datetime.now(tz) if tz else datetime.now()
    return dt.isoformat(timespec="seconds")

def prompt_choice(prompt, choices):
    print(prompt)
    for k, v in choices.items():
        print(f"  {k}. {v['label']}")
    choice = input("Choose option number: ").strip()
    return choice

def select_students_by_department():
    print("Select department or 'all'")
    depts = sorted({s["department"] for s in STUDENTS})
    for i, d in enumerate(depts, start=1):
        print(f"  {i}. {d}")
    print(f"  {len(depts)+1}. All students")
    sel = input("Choose number: ").strip()
    try:
        idx = int(sel)
        if 1 <= idx <= len(depts):
            dept = depts[idx-1]
            return [s for s in STUDENTS if s["department"] == dept], dept
        elif idx == len(depts)+1:
            return STUDENTS, "All"
    except Exception:
        pass
    return STUDENTS, "All"

def collect_attendance(mode_label):
    selected_students, dept_label = select_students_by_department()
    attendance = []
    print(f"Recording attendance for: {dept_label}")
    for s in selected_students:
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

def render_html(meta, attendance):
    rows = ""
    for a in attendance:
        rows += f"<tr><td>{a['roll']}</td><td>{a['student_id']}</td><td>{a['name']}</td><td>{a['department']}</td><td>{a['status_label']}</td><td>{a['note']}</td></tr>\n"
    html = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Attendance {meta['timestamp']}</title>
<style>table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px}}</style>
</head>
<body>
<h1>Attendance — {meta['mode']} — {meta['timestamp']}</h1>
<p><strong>Department:</strong> {meta['department']}</p>
<table>
<thead><tr><th>Roll</th><th>Student ID</th><th>Name</th><th>Department</th><th>Status</th><th>Note</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>"""
    return html

def render_markdown(meta, attendance):
    md = f"# Attendance — {meta['mode']} — {meta['timestamp']}\n\n"
    md += f"**Department:** {meta['department']}\n\n"
    md += "| Roll | Student ID | Name | Department | Status | Note |\n"
    md += "|------|------------|------|------------|--------|------|\n"
    for a in attendance:
        md += f"| {a['roll']} | {a['student_id']} | {a['name']} | {a['department']} | {a['status_label']} | {a['note']} |\n"
    return md

def save_outputs(meta, attendance):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"attendance_{meta['mode'].replace(' ','_')}_{ts}"
    json_path = os.path.join(OUTPUT_DIR, base + ".json")
    html_path = os.path.join(OUTPUT_DIR, base + ".html")
    md_path = os.path.join(OUTPUT_DIR, base + ".md")
    payload = {"meta": meta, "attendance": attendance}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(meta, attendance))
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_markdown(meta, attendance))
    print(f"Saved: {json_path}, {html_path}, {md_path}")

def main():
    print("Attendance system")
    print("1. Daily (main)\n2. Class-based\n3. Group-based")
    mode_choice = input("Choose attendance mode (1/2/3): ").strip()
    mode_label = SCHEDULES.get(mode_choice, {"label": "Daily (main)"})["label"]
    timestamp = now_iso()
    department = "Selected at prompt"
    attendance = collect_attendance(mode_label)
    meta = {
        "madrasha": "Baitul Quran International Madrasha",
        "address": "Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh",
        "curated_by": "MJ Ahmad",
        "mode": mode_label,
        "timestamp": timestamp,
        "department": department,
        "teachers": TEACHERS,
    }
    save_outputs(meta, attendance)

if __name__ == "__main__":
    main()
