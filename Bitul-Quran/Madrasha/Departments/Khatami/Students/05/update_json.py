# update_json_interactive.py
import json
import os

STUDENT_FILE = "student.json"

def load_json():
    if not os.path.exists(STUDENT_FILE):
        print(f"{STUDENT_FILE} not found. Run generate_json.py first.")
        exit(1)
    with open(STUDENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data):
    with open(STUDENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ student.json updated successfully.")

def parse_pages_input(s):
    s = s.strip()
    if not s:
        return []
    parts = [p.strip() for p in s.split(",") if p.strip()]
    pages = []
    for p in parts:
        try:
            n = int(p)
            if 1 <= n <= 20:
                pages.append(n)
        except:
            pass
    return sorted(set(pages))

def interactive_update():
    data = load_json()
    paras = data["student"].get("hifz_tracker", [])
    print("Interactive updater — Para by Para.")
    print("For each Para, enter comma-separated page numbers for COMPLETED and IN PROGRESS.")
    print("Leave blank to skip a category. Enter 'q' to quit early and save progress.\n")

    for para in paras:
        pnum = para["para_number"]
        print(f"\n--- Para {pnum} ---")
        # show current statuses summary
        completed = [pg["page_number"] for pg in para["pages"] if pg["status"] == "completed"]
        inprog = [pg["page_number"] for pg in para["pages"] if pg["status"] == "in progress"]
        pending = [pg["page_number"] for pg in para["pages"] if pg["status"] == "pending"]
        print(f"Current: completed({len(completed)}), in progress({len(inprog)}), pending({len(pending)})")

        # ask for completed
        comp_in = input("Enter pages to mark COMPLETED (comma separated) or press Enter to skip: ").strip()
        if comp_in.lower() == "q":
            break
        comp_pages = parse_pages_input(comp_in)

        # ask for in progress
        prog_in = input("Enter pages to mark IN PROGRESS (comma separated) or press Enter to skip: ").strip()
        if prog_in.lower() == "q":
            break
        prog_pages = parse_pages_input(prog_in)

        # apply: priority to completed (if a page in both lists, completed wins)
        for pg in para["pages"]:
            if pg["page_number"] in comp_pages:
                pg["status"] = "completed"
            elif pg["page_number"] in prog_pages:
                pg["status"] = "in progress"
            else:
                # leave existing status as-is
                pass

        # quick summary after change
        completed = [pg["page_number"] for pg in para["pages"] if pg["status"] == "completed"]
        inprog = [pg["page_number"] for pg in para["pages"] if pg["status"] == "in progress"]
        pending = [pg["page_number"] for pg in para["pages"] if pg["status"] == "pending"]
        print(f"Updated: completed({len(completed)}), in progress({len(inprog)}), pending({len(pending)})")

    # save back to same student.json
    save_json(data)

if __name__ == "__main__":
    interactive_update()
