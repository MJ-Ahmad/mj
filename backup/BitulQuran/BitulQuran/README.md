### Project Plan — Bitul Quran Institutional Platform (Production Ready)

**সংক্ষিপ্ত সারমর্ম**  
এই পরিকল্পনার উদ্দেশ্য: **Baitul Quran International Madrasha**‑র জন্য একটি প্রোডাকশন‑গ্রেড, ফাইল‑ড্রিভেন প্ল্যাটফর্ম তৈরি করা — যেখানে প্রতিষ্ঠানের সকল ডেটা (স্টাফ, শিক্ষার্থী, কারিকুলাম, হাজিরা, রোডম্যাপ, নীতি) একটি **master JSON**‑এ থাকবে, একটি পেশাদার **index.html** ভিউয়ার থাকবে, এবং পরিচালনা‑কাজের জন্য CLI স্ক্রিপ্ট থাকবে। সবকিছু **বাই‑লিঙ্গুয়াল (EN | BN)** সমর্থন করবে, ব্যাকআপ ও স্ন্যাপশট নীতি থাকবে, এবং ভবিষ্যতে Flask/SQLite‑ভিত্তিক ওয়েব মাইগ্রেশন সহজ হবে।

---

### প্রধান মাইলস্টোন ও রোডম্যাপ (90‑দিনের ট্যাকটিক্যাল প্ল্যান)

| Phase | সময়কাল | প্রধান কাজ |
|---|---:|---|
| **Phase 1 — Foundation** | Day 0–14 | `bitul_quran.json` সম্পূর্ণ করা; `index.html` স্থাপন; `students.py`, `attendance.py`, `manage_site.py` টেস্ট করা; লোকাল সার্ভার টেস্ট। |
| **Phase 2 — Stabilize** | Day 15–45 | Atomic writes, daily snapshot cron, MkDocs ডকস, CSV রিপোর্ট স্ক্রিপ্ট, শিক্ষক প্রশিক্ষণ। |
| **Phase 3 — Web UI (Pilot)** | Day 46–90 | Flask + SQLite প্রোটোটাইপ; শিক্ষক লগইন; কনকারেন্ট রাইট; QR‑চেকইন পাইলট পরিকল্পনা। |
| **Phase 4 — Scale** | 3–9 months | Parent portal (read‑only), রিপোর্টিং ড্যাশবোর্ড, মোবাইল অ্যাপ পরিকল্পনা, AI‑assisted tajweed গবেষণা (রোডম্যাপ)। |

---

### Deliverables (আপনি পাবেন)

- **Master data**: `bitul_quran.json` — প্রতিষ্ঠানের পূর্ণ ডেটা মডেল (staff, students, departments, curriculum, policies, roadmap, goals, contacts, meta)  
- **Public viewer**: `index.html` — পেশাদার হেডার/ফুটার, EN|BN টগল, নেভিগেশন কন্ট্রোল `site_config.json`‑এর মাধ্যমে, password/countdown গেটিং।  
- **CLI controllers**: `manage_site.py` (menu/config), `attendance.py` (attendance master integration)  
- **Operational scripts**: CSV report generator, snapshot rotation guidance, MkDocs config (`mkdocs.yml`)  
- **Deployment guide**: স্ট্যাটিক হোস্টিং (GitHub Pages/Netlify) ও Flask‑মাইগ্রেশন নির্দেশনা  
- **Training plan**: 2‑hour teacher workshop outline (attendance, backups, recovery)

---

### ধাপে ধাপে বাস্তবায়ন (বাংলা নির্দেশনা)

#### ধাপ ১ — পরিবেশ প্রস্তুতি (Day 0)
- **ফোল্ডার স্ট্রাকচার** তৈরি করুন:
  ```
  project-root/
  ├─ assets/logo.png
  ├─ bitul_quran.json
  ├─ site_config.json
  ├─ index.html
  ├─ students.py
  ├─ attendance.py
  ├─ manage_site.py
  ├─ master/
  │  ├─ attendance_master.json
  └─ outputs/
  ```
- `assets/logo.png` রাখুন (লোগো)।  
- Python 3.9+ ইনস্টল নিশ্চিত করুন।

#### ধাপ ২ — master JSON পূরণ (Day 1–3)
- `bitul_quran.json`‑এ **serial_master_list** আপডেট করুন — প্রতিটি শিক্ষার্থীর জন্য একটি অনন্য `serial` দিন।  
- `students.py`‑এ একই তালিকা রাখুন (attendance স্ক্রিপ্টের জন্য)।  
- **নোট:** `bitul_quran.json` হবে authoritative; `students.py`‑এ পরিবর্তন করলে JSON‑ও আপডেট করুন।

#### ধাপ ৩ — লোকাল টেস্ট ও হাজিরা রুটিন (Day 4–7)
- `python attendance.py` চালিয়ে একটি সেশন রেকর্ড করুন। নিশ্চিত করুন:
  - `master/attendance_master.json`‑এ রেকর্ড যোগ হচ্ছে।
  - `outputs/`‑এ টাইমস্ট্যাম্পেড স্ন্যাপশট তৈরি হচ্ছে (`.json`, `.md`, `.html`)।
- প্রতিদিন শেষে `outputs/`‑এর ব্যাকআপ ক্লাউডে কপি করার জন্য ক্রন/Task Scheduler সেট করুন।

#### ধাপ ৪ — পেজ ভিউয়ার ও কনফিগার (Day 8–12)
- `index.html`‑এ `bitul_quran.json` ও `site_config.json` লোড করে দেখুন।  
- `manage_site.py` চালিয়ে মেনু আইটেম যোগ/সম্পাদনা করুন; `index.html`‑এ মেনু প্রতিফলিত হচ্ছে কিনা পরীক্ষা করুন।  
- EN|BN টগল টেস্ট করুন; `site_config.json`‑এ `label_bn` ব্যবহার করুন।

#### ধাপ ৫ — রিপোর্টিং ও অটোমেশন (Day 13–21)
- **CSV report script** চালু করুন: মাসিক উপস্থিতি শতাংশ, শিক্ষার্থী‑ভিত্তিক সারাংশ।  
- MkDocs কনফিগার (`mkdocs.yml`) দিয়ে নীতিমালা ও ডকুমেন্টেশন প্রকাশ করুন।  
- `master/recovery.log` মনিটরিং চালু করুন।

#### ধাপ ৬ — Pilot Web UI (Flask) (Day 22–60)
- Flask single‑file অ্যাপ তৈরি করুন (প্রটোটাইপ) — endpoints:
  - `GET /api/master` → `bitul_quran.json`
  - `POST /api/attendance` → append record (authenticated)
  - `GET /api/attendance` → read master attendance
- Authentication: শুরুতে **basic token** বা teacher password; পরে JWT/DB‑based auth।  
- Pilot: 1‑2 শিক্ষক দিয়ে 2 সপ্তাহ টেস্ট; concurrency ও race condition পর্যবেক্ষণ করুন।

#### ধাপ ৭ — QR Pilot ও Scale (Day 61–90+)
- QR‑চেকইন পাইলট: প্রতিটি শিক্ষার্থীর জন্য QR (student id) জেনারেট করুন; স্ক্যান করে Flask endpoint‑এ POST করুন।  
- রিপোর্টিং: দৈনিক/সাপ্তাহিক/মাসিক ড্যাশবোর্ড (CSV → Excel/PDF)।  
- নিরাপত্তা: production‑grade auth, HTTPS, offsite backups।

---

### Sample `bitul_quran.json` (production template — trimmed example)

```json
{
  "institution": {
    "name": "Baitul Quran International Madrasha",
    "short_name": "Bitul Quran",
    "address": "Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh",
    "phone": "+8801824401812",
    "email": "info@baitulquran.example",
    "logo": "assets/logo.png",
    "curated_by": "MJ Ahmad — Steward of Ethical Inheritance",
    "established": "2018-09-01",
    "mission": "To combine classical hifz pedagogy with modern learning technology.",
    "vision": "A globally recognized center of excellence for Quran memorization.",
    "last_updated": "2026-05-03T03:04:06+06:00"
  },
  "staff": {
    "teachers": [
      {"id":"T01","name":"Ustad Arif","phone":"01824401812","role":"Senior Ustad","department":"Khatmi / Recitation"},
      {"id":"T02","name":"Ustad Arif Robbani","phone":"01631940605","role":"Nurani Instructor","department":"Nurani Maktab"},
      {"id":"T03","name":"Ustad Jafor","phone":"01892051303","role":"Hifz Instructor","department":"Hifz 1–29"}
    ]
  },
  "students": {
    "serial_master_list": [
      {"serial":1,"name":"Faysal (1)","roll":"03","id":"BQSHK01","department":"Khatmi / Recitation"},
      {"serial":2,"name":"Sown","roll":"04","id":"BQSHK02","department":"Khatmi / Recitation"},
      {"serial":3,"name":"Jubayer","roll":"01","id":"BQSHS01","department":"Hifz 1–29"},
      {"serial":4,"name":"Anamul Haqe","roll":"02","id":"BQSHS18","department":"Hifz 1–29"},
      {"serial":5,"name":"Jidan","roll":"01","id":"BQSNU01","department":"Nurani Maktab"}
    ],
    "by_department": {
      "Nurani Maktab": ["BQSNU01","BQSNU02"],
      "Pre-Hifz Nazara": ["BQSNA01","BQSNA02"],
      "Hifz 1–29": ["BQSHS01","BQSHS18"],
      "Khatmi / Recitation": ["BQSHK01","BQSHK02"]
    }
  },
  "curriculum": {
    "principles":["Spaced repetition","Daily micro-practice","Teacher-led correction"],
    "modules":[
      {"code":"C01","title":"Nurani Foundations","hours":120},
      {"code":"C02","title":"Nazara Preparation","hours":200},
      {"code":"C03","title":"Hifz Core","hours":2000}
    ]
  },
  "attendance_integration": {
    "master_file":"master/attendance_master.json",
    "snapshots_dir":"outputs/",
    "policies":{"retention_years":3,"backup":"daily"}
  },
  "roadmap": {
    "2026-Q2":["Deploy web UI (Flask)","Add SQLite history","Teacher login"],
    "2026-Q3":["QR check-in pilot","Automated reports","Parent portal (read-only)"]
  },
  "meta":{"generated_at":"2026-05-03T03:04:06+06:00","version":"1.0.0"}
}
```

---

### Sample `index.html` usage notes (quick)

- `index.html` reads `bitul_quran.json` and `site_config.json`.  
- **Menu control**: `manage_site.py` edits `site_config.json` to show/hide items, set passwords, set countdowns.  
- **Attendance**: viewer links to `master/attendance_master.json` (or embed `attendance_master` inside `bitul_quran.json` if preferred).  
- **EN | BN**: `site_config.json` supports `label` and `label_bn`; `index.html` toggles language.

---

### Security, backups, and governance (সংক্ষেপে)

- **Backups**: daily snapshots to `outputs/` + weekly offsite copy (Google Drive/OneDrive).  
- **Access control**: master files write‑access limited to admin accounts; for multi‑user writes use Flask + DB with auth.  
- **Audit**: keep `recovery.log` and snapshot retention policy (3 years).  
- **Training**: 2‑hour session for teachers covering CLI usage, backups, and recovery.

---

### Immediate next steps I will do for you (if you confirm)
1. **Generate final `bitul_quran.json`** with the full student roster you already provided (I will merge all names into `serial_master_list`).  
2. **Produce final `index.html`** preloaded with that JSON and `site_config.json` default menu.  
3. **Provide CSV report script** and a short Flask starter app (single file) for pilot deployment.

আপনি যদি এখন “**Proceed**” বলেন, আমি প্রথমে আপনার সম্পূর্ণ শিক্ষার্থী তালিকা (যদি আপনি চান, আমি পূর্বের তালিকা ব্যবহার করব) নিয়ে **final `bitul_quran.json`** তৈরি করে দেব এবং সঙ্গে **index.html** ও **site_config.json**‑এর প্রস্তুত কপি দেব।