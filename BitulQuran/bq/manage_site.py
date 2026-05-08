#!/usr/bin/env python3
"""
manage_site.py

Interactive controller for site_config.json used by index.html.

Usage:
    python manage_site.py
"""

import json
from pathlib import Path
from datetime import datetime
import tempfile
import os

BASE = Path(__file__).parent.resolve()
MASTER_JSON = BASE / "bitul_quran.json"
CONFIG_JSON = BASE / "site_config.json"
INDEX_HTML = BASE / "index.html"

def atomic_write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent))
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, str(path))

def load_config():
    if CONFIG_JSON.exists():
        try:
            return json.loads(CONFIG_JSON.read_text(encoding="utf-8"))
        except Exception:
            print("Warning: config JSON invalid. Reinitializing.")
    # default config
    cfg = {
        "menu": [
            {"key":"overview","label":"Overview","label_bn":"ওভারভিউ","subtitle":"Institution summary","password_protected":False},
            {"key":"teachers","label":"Teachers","label_bn":"শিক্ষকবৃন্দ","subtitle":"Staff directory","password_protected":False},
            {"key":"students","label":"Students","label_bn":"শিক্ষার্থী","subtitle":"Master student list","password_protected":False},
            {"key":"attendance","label":"Attendance","label_bn":"হাজিরা","subtitle":"Attendance master","password_protected":False},
            {"key":"curriculum","label":"Curriculum","label_bn":"পাঠ্যক্রম","subtitle":"Curriculum & modules","password_protected":False},
            {"key":"roadmap","label":"Roadmap","label_bn":"রোডম্যাপ","subtitle":"Strategic roadmap","password_protected":False}
        ],
        "footer": {
            "left": "© Baitul Quran International Madrasha",
            "right": "Contact: office@baitulquran.example"
        }
    }
    atomic_write(CONFIG_JSON, json.dumps(cfg, ensure_ascii=False, indent=2))
    return cfg

def save_config(cfg):
    atomic_write(CONFIG_JSON, json.dumps(cfg, ensure_ascii=False, indent=2))
    print("Saved site_config.json")

def list_menu(cfg):
    print("\nMenu items:")
    for i, m in enumerate(cfg.get("menu", []), start=1):
        lock = "[LOCK]" if m.get("password_protected") else ""
        cd = f" (countdown until {m.get('countdown_until')})" if m.get("countdown_until") else ""
        print(f"{i}. {m.get('key')} - {m.get('label')} {lock}{cd}")

def prompt(prompt_text, default=None):
    v = input(f"{prompt_text} " + (f"[{default}] " if default else ""))
    return v.strip() or default

def add_menu_item(cfg):
    key = prompt("Key (unique id):")
    label = prompt("Label (EN):")
    label_bn = prompt("Label (BN):")
    subtitle = prompt("Subtitle:")
    pw = prompt("Password protect? (y/N):", "N")
    password = ""
    if pw.lower().startswith("y"):
        password = prompt("Password (plain text):")
    countdown = prompt("Countdown until (ISO datetime) or leave blank:")
    hide_after = False
    show_countdown = False
    if countdown:
        hide_after = prompt("Hide after countdown ends? (y/N):", "N").lower().startswith("y")
        show_countdown = prompt("Show countdown notice? (y/N):", "N").lower().startswith("y")
    item = {
        "key": key,
        "label": label,
        "label_bn": label_bn,
        "subtitle": subtitle,
        "password_protected": bool(password),
        "password": password,
        "countdown_until": countdown or None,
        "hide_after_countdown": hide_after,
        "show_countdown": show_countdown
    }
    cfg.setdefault("menu", []).append(item)
    save_config(cfg)

def edit_menu_item(cfg):
    list_menu(cfg)
    sel = prompt("Choose item number to edit:")
    try:
        idx = int(sel) - 1
        item = cfg["menu"][idx]
    except Exception:
        print("Invalid selection")
        return
    print("Leave blank to keep current value.")
    item["label"] = prompt("Label (EN):", item.get("label"))
    item["label_bn"] = prompt("Label (BN):", item.get("label_bn"))
    item["subtitle"] = prompt("Subtitle:", item.get("subtitle"))
    pw = prompt("Password protect? (y/N):", "Y" if item.get("password_protected") else "N")
    if pw.lower().startswith("y"):
        item["password_protected"] = True
        item["password"] = prompt("Password (plain text):", item.get("password",""))
    else:
        item["password_protected"] = False
        item["password"] = ""
    cd = prompt("Countdown until (ISO datetime) or blank:", item.get("countdown_until") or "")
    item["countdown_until"] = cd or None
    item["hide_after_countdown"] = prompt("Hide after countdown ends? (y/N):", "Y" if item.get("hide_after_countdown") else "N").lower().startswith("y")
    item["show_countdown"] = prompt("Show countdown notice? (y/N):", "Y" if item.get("show_countdown") else "N").lower().startswith("y")
    save_config(cfg)

def remove_menu_item(cfg):
    list_menu(cfg)
    sel = prompt("Choose item number to remove:")
    try:
        idx = int(sel) - 1
        removed = cfg["menu"].pop(idx)
        print("Removed", removed.get("key"))
        save_config(cfg)
    except Exception:
        print("Invalid selection")

def reorder_menu(cfg):
    list_menu(cfg)
    sel = prompt("Enter new order as comma-separated numbers (e.g., 3,1,2):")
    try:
        parts = [int(x.strip())-1 for x in sel.split(",")]
        new = [cfg["menu"][i] for i in parts]
        cfg["menu"] = new
        save_config(cfg)
    except Exception:
        print("Invalid input")

def edit_footer(cfg):
    left = prompt("Footer left text:", cfg.get("footer",{}).get("left",""))
    right = prompt("Footer right text:", cfg.get("footer",{}).get("right",""))
    cfg.setdefault("footer", {})["left"] = left
    cfg["footer"]["right"] = right
    save_config(cfg)

def touch_index():
    # update index.html timestamp comment to bust caches
    if not INDEX_HTML.exists():
        print("index.html not found; skipping touch.")
        return
    text = INDEX_HTML.read_text(encoding="utf-8")
    marker = "<!-- touched:"
    if marker in text:
        before, after = text.split(marker,1)
        rest = after.split("-->",1)[1] if "-->" in after else ""
        new = before + marker + datetime.utcnow().isoformat() + "-->" + rest
    else:
        new = "<!-- touched:" + datetime.utcnow().isoformat() + "-->\n" + text
    atomic_write(INDEX_HTML, new)
    print("Touched index.html to refresh caches.")

def main():
    cfg = load_config()
    while True:
        print("\nSite manager")
        print("1. List menu")
        print("2. Add menu item")
        print("3. Edit menu item")
        print("4. Remove menu item")
        print("5. Reorder menu")


        print("6. Edit footer")
        print("7. Touch index.html (cache bust)")
        print("0. Exit")
        choice = prompt("Choose option:")
        if choice == "1":
            list_menu(cfg)
        elif choice == "2":
            add_menu_item(cfg)
        elif choice == "3":
            edit_menu_item(cfg)
        elif choice == "4":
            remove_menu_item(cfg)
        elif choice == "5":
            reorder_menu(cfg)
        elif choice == "6":
            edit_footer(cfg)
        elif choice == "7":
            touch_index()
        elif choice == "0":
            break
        else:
            print("Unknown option")

if __name__ == "__main__":
    main()
