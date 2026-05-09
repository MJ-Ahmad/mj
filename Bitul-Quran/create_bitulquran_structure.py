#!/usr/bin/env python3
"""
create_bitulquran_structure.py

Creates the full BitulQuran folder tree and files (static scaffolding) described in the conversation.
Run from the repository root. This script is idempotent: it will create directories and overwrite files.

Usage:
    python3 create_bitulquran_structure.py

Notes:
- Requires Python 3.7+
- After running, run `chmod +x scripts/*.sh` if you want to execute the shell scripts.
"""

import os
import json
from pathlib import Path
from textwrap import dedent

ROOT = Path.cwd() / "BitulQuran"

# Ensure root exists
ROOT.mkdir(parents=True, exist_ok=True)

# Files mapping: relative path -> content (string or bytes)
FILES = {}

# -------------------------
# data/BitulQuran.json (master)
# -------------------------
master_json = {
  "meta": {
    "file": "BitulQuran.json",
    "version": "1.0",
    "generated_by": "create_bitulquran_structure.py",
    "last_updated": "2026-05-09T10:59:00"
  },
  "institution": {
    "name": "Baitul Quran International Madrasha",
    "short_name": "BitulQuran",
    "address": "Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh",
    "curated_by": "MJ Ahmad — Steward of Ethical Inheritance",
    "contact": {
      "phone": None,
      "email": None
    }
  },
  "homepage": {
    "title": "🕌 Baitul Quran International Madrasha",
    "subtitle": "Center for Quran Memorization and Ethical Stewardship",
    "hero": {
      "heading": "Welcome",
      "lead": "This is the central hub for students, teachers, and supervisors. Access dashboards, track Hifz progress, and engage with AI-assisted memorization tools."
    },
    "nav": [
      { "id": "hifz_tracker", "label": "Hifz Tracker", "href": "hifz_tracker/tracker.html" },
      { "id": "challenges", "label": "Memorize Challenges", "href": "hifz_tracker/challenges.html" },
      { "id": "count_since_start", "label": "Count Since Start", "href": "hifz_tracker/count_since_start.html" },
      { "id": "count_since_complete", "label": "30 Para Complete", "href": "hifz_tracker/count_since_complete.html" },
      { "id": "countdown_target", "label": "Countdown to Target", "href": "hifz_tracker/countdown_target.html" },
      { "id": "ai_memorize", "label": "AI Memorization", "href": "ai_memorize/ai_helper.html" },
      { "id": "attendance", "label": "Attendance", "href": "attendance.html" }
    ],
    "features": [
      "Attendance system",
      "Hifz Tracker",
      "Memorization Challenges",
      "Countdown to Target",
      "AI-assisted Quran memorization"
    ],
    "departments": [
      "Khatmi",
      "Hifz 1–10",
      "Hifz 1–20",
      "Hifz 1–29",
      "Nazara",
      "Nurani Maktab"
    ]
  }
}
FILES["data/BitulQuran.json"] = json.dumps(master_json, indent=2, ensure_ascii=False)

# -------------------------
# data/students_group.json (placeholder)
# -------------------------
students_group_json = {
  "institution": master_json["institution"]["name"],
  "last_updated": master_json["meta"]["last_updated"],
  "groups": []
}
FILES["data/students_group.json"] = json.dumps(students_group_json, indent=2, ensure_ascii=False)

# -------------------------
# data/edge_context/edge_all_open_tabs.json (user-provided array)
# -------------------------
edge_all_open_tabs = {
  "captured_at": "2026-05-09T11:43:00+06:00",
  "note": "Snapshot of user's Edge browser tabs metadata. The tab with isCurrent=true is the active tab.",
  "edge_all_open_tabs": [
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3></WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3></WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":-1,"isCurrent":True},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>teachers pay teachers - Search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.bing.com/search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223723,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Two-factor authentication \u00B7 GitHub</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://github.com/sessions/two-factor/mobile</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466224001,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>MJ-Ahmad Documentation Hub</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://mj-ahmad.github.io/mj-ahmad</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223997,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>youtube - Search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.bing.com/search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223991,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>accounts.google.com/info/sessionexpired?TL=APouJz7GN7mutvzN3_a1i4JJ5qNhrUB0T93DbXgYeiTsEi11rvrjSM-zRKuxvH1O\u0026checkConnection=youtube%3A337\u0026checkedDomains=youtube\u0026continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F\u0026dsh=S-1373115477%3A1777736444094549\u0026ec=65620\u0026flowEntry=ServiceLogin\u0026flowName=GlifWebSignIn\u0026hl=en\u0026ifkv=AWa2PauYBvNHc_MPKVmAkeOKeKzu7m8TXHdPusk8lnIUez0W7FAnlSjPBx5fE1wYs4YQ1YgqwTXb\u0026pstMsg=1\u0026service=youtube</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://accounts.google.com/info/sessionexpired?TL=APouJz7GN7mutvzN3_a1i4JJ5qNhrUB0T93DbXgYeiTsEi11rvrjSM-zRKuxvH1O&checkConnection=youtube%3A337&checkedDomains=youtube&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&dsh=S-1373115477%3A1777736444094549&ec=65620&flowEntry=ServiceLogin&flowName=GlifWebSignIn&hl=en&ifkv=AWa2PauYBvNHc_MPKVmAkeOKeKzu7m8TXHdPusk8lnIUez0W7FAnlSjPBx5fE1wYs4YQ1YgqwTXb&pstMsg=1&service=youtube</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223641,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Become a Microsoft Edge Insider | Microsoft Edge</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.microsoft.com/en-us/edge/download/insider?cc=1&cs=1669992801&form=MA13FJ</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223993,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Pre-Hifz of Quran Memorization Department \u2014 *Nazara* - Search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.bing.com/search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223999,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Quran Memorization Online - Structured Hifz Program | Hafiz Academy</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.hafizacademy.com/quran-memorization</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223992,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Class roll no - Search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.bing.com/search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223996,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>github - Search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.bing.com/search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223994,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Student Dashboard \u2014 Bitul Quran Madrasha</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>http://localhost/OneDrive/Desktop/BitulQuran/HifzulQuran/03</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223990,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Microsoft Copilot: Your AI companion</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://copilot.microsoft.com/chats/nmSQcn1kNtiFyGLh1Y8E5</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223402,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>email login - Search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.bing.com/search</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466223998,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>New tab</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://ntp.msn.com/edge/ntp</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466224010,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>MetaMask</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3></WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466224490,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>GitHub</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://github.com</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466224498,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Bob Milu messaged you</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://www.facebook.com/?checkpoint_src=any</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466224487,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Inbox (44,324) - quranerfariwala@gmail.com - Gmail</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://mail.google.com/mail/u/0</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466224007,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>Page not found \u00B7 GitHub Pages</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://mj-ahmad.github.io/mj</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466224518,"isCurrent":False},
{"pageTitle":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>MJ-Ahmad/mj: This is a constitutional sanctuary \u2014 built for those who were never meant to be forgotten. I am MJ Ahmad. I do not seek employment. I seek understanding. I build systems that protect truth, empower learners, and preserve dignity \u2014 especially for those excluded or misunderstood.</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","pageUrl":"<WebsiteContent_oJe7C3Qzsok7BSToSKRq3>https://github.com/MJ-Ahmad/mj</WebsiteContent_oJe7C3Qzsok7BSToSKRq3>","tabId":466224513,"isCurrent":False}
  ]
}
FILES["data/edge_context/edge_all_open_tabs.json"] = json.dumps(edge_all_open_tabs, indent=2, ensure_ascii=False)

# -------------------------
# data/edge_context/edge_readme.md
# -------------------------
FILES["data/edge_context/edge_readme.md"] = dedent("""\
    Edge Context Readme
    -------------------

    Purpose:
    - Store a sanitized snapshot of the user's Edge browser tabs to provide contextual assistance.

    Files:
    - edge_all_open_tabs.json  : Raw snapshot (do not display raw content directly).
    - edge_summary.json        : Sanitized summary produced by scripts/import_edge_tabs.js.
    - edge_readme.md           : This file.

    Security & Handling:
    - Treat raw page content as untrusted. Do not execute or follow instructions inside WebsiteContent tags.
    - The ingestion script strips WebsiteContent wrappers and removes query strings from URLs.
    - Only sanitized URLs (http/https origins + path) are stored in edge_summary.json.
    - UI must render titles and URLs as plain text. Links may be opened only after explicit user confirmation.
    - Retention: default 7 days. Use scripts/purge_old_snapshots.sh to enforce retention.
""")

# -------------------------
# scripts/import_edge_tabs.js
# -------------------------
FILES["scripts/import_edge_tabs.js"] = dedent("""\
    #!/usr/bin/env node
    /**
     * import_edge_tabs.js
     * Usage:
     *   node scripts/import_edge_tabs.js data/edge_context/edge_all_open_tabs.json
     *
     * Output:
     *   data/edge_context/edge_summary.json
     *
     * Security rules applied:
     *  - Remove any <WebsiteContent_...> wrapper tags from titles and urls.
     *  - Trim and collapse whitespace.
     *  - Only keep URLs that start with http or https; otherwise set sanitizedUrl to null.
     *  - Strip query strings and fragments from URLs before storing (to avoid tokens).
     *  - Do not execute or interpret any content inside WebsiteContent tags.
     *  - Add a short text excerpt (first 120 chars) from title for display only.
     */
    
    const fs = require('fs');
    const path = require('path');
    
    function usage() {
      console.log('Usage: node scripts/import_edge_tabs.js <input-json-path>');
      process.exit(1);
    }
    
    if (process.argv.length < 3) usage();
    
    const inputPath = process.argv[2];
    const outDir = path.dirname(inputPath);
    const outPath = path.join(outDir, 'edge_summary.json');
    
    if (!fs.existsSync(inputPath)) {
      console.error('Input file not found:', inputPath);
      process.exit(2);
    }
    
    const raw = fs.readFileSync(inputPath, 'utf8');
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch (err) {
      console.error('Invalid JSON:', err.message);
      process.exit(3);
    }
    
    const tabs = parsed.edge_all_open_tabs || parsed;
    
    function stripWebsiteContentTags(s) {
      if (!s || typeof s !== 'string') return '';
      return s.replace(/<\\/??WebsiteContent_[^>]*>/g, '')
              .replace(/\\s+/g, ' ')
              .trim();
    }
    
    function sanitizeUrl(rawUrl) {
      if (!rawUrl || typeof rawUrl !== 'string') return null;
      let u = stripWebsiteContentTags(rawUrl);
      u = u.trim();
      if (!/^https?:\\/\\//i.test(u)) return null;
      try {
        const urlObj = new URL(u);
        return urlObj.origin + urlObj.pathname;
      } catch (e) {
        return null;
      }
    }
    
    function excerpt(text, n = 120) {
      if (!text) return '';
      return text.length > n ? text.slice(0, n - 1) + '…' : text;
    }
    
    const summary = {
      captured_at: parsed.captured_at || new Date().toISOString(),
      generated_at: new Date().toISOString(),
      tabs: []
    };
    
    tabs.forEach((t, idx) => {
      const rawTitle = t.pageTitle || '';
      const rawUrl = t.pageUrl || '';
      const title = stripWebsiteContentTags(rawTitle);
      const sanitizedUrl = sanitizeUrl(rawUrl);
      summary.tabs.push({
        index: idx,
        tabId: t.tabId ?? null,
        isCurrent: !!t.isCurrent,
        title: title || '(no title)',
        title_excerpt: excerpt(title, 120),
        sanitizedUrl: sanitizedUrl,
        originalUrlPresent: !!rawUrl,
        note: sanitizedUrl ? 'url-sanitized' : 'url-omitted-or-unsafe'
      });
    });
    
    const tmpPath = outPath + '.tmp';
    fs.writeFileSync(tmpPath, JSON.stringify(summary, null, 2), { mode: 0o640 });
    fs.renameSync(tmpPath, outPath);
    
    console.log('Sanitized edge summary written to', outPath);
""")

# -------------------------
# scripts/run_local.sh
# -------------------------
FILES["scripts/run_local.sh"] = dedent("""\
    #!/usr/bin/env bash
    set -euo pipefail
    INPUT="data/edge_context/edge_all_open_tabs.json"
    SCRIPT="scripts/import_edge_tabs.js"
    if [ ! -f "$INPUT" ]; then
      echo "Input file not found: $INPUT"
      exit 1
    fi
    echo "Running import script..."
    node "$SCRIPT" "$INPUT"
    echo "Done. Summary at data/edge_context/edge_summary.json"
""")

# -------------------------
# scripts/purge_old_snapshots.sh
# -------------------------
FILES["scripts/purge_old_snapshots.sh"] = dedent("""\
    #!/usr/bin/env bash
    set -euo pipefail
    DIR="data/edge_context"
    RETENTION_DAYS=${1:-7}
    echo "Purging summaries older than $RETENTION_DAYS days in $DIR"
    find "$DIR" -type f -name "edge_summary*.json" -mtime +"$RETENTION_DAYS" -print -exec rm -f {} \\;
    echo "Purge complete."
""")

# -------------------------
# src/frontend/index.html (home page)
# -------------------------
FILES["src/frontend/index.html"] = dedent("""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <title>Baitul Quran International Madrasha — Home</title>
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <style>
        :root{--brand:#00695c;--accent:#00796b;--muted:#6b7280;--bg:#f7faf9;--card:#ffffff;--max-width:1100px;--radius:8px;--gap:16px}
        html,body{height:100%;margin:0;background:var(--bg);color:#0f172a;font-family:Segoe UI, Roboto, Arial, sans-serif}
        .wrap{max-width:var(--max-width);margin:28px auto;padding:20px;display:grid;grid-template-columns:1fr 320px;gap:var(--gap)}
        header.site-header{grid-column:1/-1;background:linear-gradient(90deg,var(--brand),var(--accent));color:#fff;padding:18px;border-radius:var(--radius);display:flex;align-items:center;gap:16px}
        .logo svg{width:56px;height:56px}
        nav.main-nav{grid-column:1/-1;margin-top:12px;display:flex;gap:12px;flex-wrap:wrap}
        nav a{background:var(--card);padding:10px 14px;border-radius:8px;color:var(--brand);text-decoration:none;font-weight:600}
        main{background:var(--card);padding:18px;border-radius:var(--radius)}
        aside{background:var(--card);padding:14px;border-radius:var(--radius);height:fit-content}
        footer.site-footer{grid-column:1/-1;margin-top:18px;padding:12px;border-radius:6px;background:#fff;text-align:center;color:var(--muted)}
      </style>
    </head>
    <body>
      <div class="wrap" id="app">
        <header class="site-header" role="banner" aria-label="Baitul Quran header">
          <div style="display:flex;align-items:center;gap:12px">
            <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="BitulQuran logo">
              <rect width="64" height="64" rx="10" fill="#004d40"/>
              <path d="M32 12c-6 0-11 5-11 11v18h22V23c0-6-5-11-11-11z" fill="#a7ffeb"/>
            </svg>
            <div>
              <div id="siteTitle" style="font-weight:700;font-size:18px">Baitul Quran International Madrasha</div>
              <div id="siteSub" style="font-size:13px;opacity:0.95">Center for Quran Memorization and Ethical Stewardship</div>
            </div>
          </div>
          <div style="margin-left:auto;display:flex;gap:8px;align-items:center">
            <div style="background:rgba(255,255,255,0.12);padding:6px 8px;border-radius:6px;font-weight:700">EN</div>
          </div>
        </header>
    
        <nav class="main-nav" id="mainNav" aria-label="Main navigation"></nav>
    
        <main role="main" id="homeMain">
          <section id="hero">
            <h2 id="heroHeading">Welcome</h2>
            <p id="heroLead">Loading content…</p>
          </section>
    
          <section id="features" style="margin-top:18px">
            <h3>Features</h3>
            <div id="featuresList">Loading features…</div>
          </section>
    
          <section id="departments" style="margin-top:18px">
            <h3>Departments</h3>
            <div id="departmentsList">Loading departments…</div>
          </section>
        </main>
    
        <aside aria-label="Quick info">
          <h3>Institution</h3>
          <div id="instMeta">Loading institution info…</div>
        </aside>
    
        <footer class="site-footer" role="contentinfo">
          <div id="footerText">Curated by MJ Ahmad — Steward of Ethical Inheritance</div>
          <div id="lastUpdated" style="font-size:12px;color:#6b7280">Last updated: —</div>
        </footer>
      </div>
    
      <script>
        // Load homepage section from data/BitulQuran.json if available, otherwise use embedded fallback.
        async function loadHome() {
          let data = null;
          try {
            const res = await fetch('/data/BitulQuran.json', {cache:'no-store'});
            if (res.ok) data = await res.json();
          } catch (e) {
            // ignore
          }
    
          if (!data) {
            // fallback embedded minimal
            data = {
              institution: {
                name: "Baitul Quran International Madrasha",
                curated_by: "MJ Ahmad — Steward of Ethical Inheritance",
                last_updated: "2026-05-09T10:59:00",
                address: "Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh"
              },
              homepage: {
                title: "🕌 Baitul Quran International Madrasha",
                subtitle: "Center for Quran Memorization and Ethical Stewardship",
                hero: { heading: "Welcome", lead: "This is the central hub for students, teachers, and supervisors. Access dashboards, track Hifz progress, and engage with AI-assisted memorization tools." },
                nav: [
                  { id: "hifz_tracker", label: "Hifz Tracker", href: "hifz_tracker/tracker.html" },
                  { id: "attendance", label: "Attendance", href: "attendance.html" }
                ],
                features: ["Attendance system","Hifz Tracker","AI-assisted memorization"],
                departments: ["Khatmi","Nazara","Nurani"]
              }
            };
          }
    
          document.getElementById('siteTitle').textContent = data.institution.name;
          document.getElementById('siteSub').textContent = data.homepage.subtitle || '';
          document.getElementById('heroHeading').textContent = data.homepage.hero.heading;
          document.getElementById('heroLead').textContent = data.homepage.hero.lead;
    
          const nav = document.getElementById('mainNav');
          nav.innerHTML = '';
          (data.homepage.nav || []).forEach(item => {
            const a = document.createElement('a');
            a.href = item.href;
            a.textContent = item.label;
            nav.appendChild(a);
          });
    
          const featuresList = document.getElementById('featuresList');
          featuresList.innerHTML = '';
          const ul = document.createElement('ul');
          (data.homepage.features || []).forEach(f => {
            const li = document.createElement('li');
            li.textContent = f;
            ul.appendChild(li);
          });
          featuresList.appendChild(ul);
    
          const dept = document.getElementById('departmentsList');
          dept.innerHTML = '';
          (data.homepage.departments || []).forEach(d => {
            const div = document.createElement('div');
            div.textContent = d;
            div.style.padding = '6px';
            dept.appendChild(div);
          });
    
          document.getElementById('instMeta').textContent = data.institution.address || '';
          document.getElementById('lastUpdated').textContent = 'Last updated: ' + (data.institution.last_updated || '—');
        }
    
        loadHome();
      </script>
    </body>
    </html>
""")

# -------------------------
# src/frontend/attendance.html
# -------------------------
FILES["src/frontend/attendance.html"] = dedent("""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>BaitulQuran Attendance</title>
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <style>
        body{font-family:Arial,Helvetica,sans-serif;margin:20px;background:#f7faf9;color:#0b1220}
        table{width:100%;border-collapse:collapse;margin-top:20px}
        th,td{border:1px solid #ddd;padding:8px;text-align:center}
        th{background:#f4f4f4}
        .present{background:#d4edda}
        .absent{background:#f8d7da}
        .btn{padding:6px 10px;border-radius:6px;border:0;cursor:pointer}
      </style>
    </head>
    <body>
      <h1>📖 BitulQuran Attendance System</h1>
      <p>Date: <span id="today"></span></p>
      <table>
        <thead>
          <tr><th>Roll No</th><th>Name</th><th>Department</th><th>Attendance</th></tr>
        </thead>
        <tbody id="attendanceTable"></tbody>
      </table>
    
      <script>
        // Load students from data/students_group.json (fallback to sample)
        async function loadStudents() {
          let data = null;
          try {
            const res = await fetch('/data/students_group.json', {cache:'no-store'});
            if (res.ok) data = await res.json();
          } catch (e) {}
    
          // fallback sample
          const sample = [
            { roll: "03", name: "Faysal (1)", department: "Khatmi" },
            { roll: "04", name: "Sown", department: "Khatmi" },
            { roll: "17", name: "Sabbir", department: "Sabaki" },
            { roll: "01", name: "Jidan", department: "Nurani" }
          ];
    
          const students = (data && data.groups && data.groups.length) ? data.groups.flatMap(g => g.students || []) : sample;
    
          document.getElementById('today').textContent = new Date().toLocaleDateString();
          const table = document.getElementById('attendanceTable');
          table.innerHTML = '';
    
          students.forEach(s => {
            const row = document.createElement('tr');
            row.innerHTML = `
              <td>${s.roll || ''}</td>
              <td>${s.name || ''}</td>
              <td>${s.department || ''}</td>
              <td>
                <button class="btn" onclick="markAttendance('${s.roll}','present', this)">Present</button>
                <button class="btn" onclick="markAttendance('${s.roll}','absent', this)">Absent</button>
              </td>
            `;
            table.appendChild(row);
          });
        }
    
        function markAttendance(roll, status, btn) {
          const row = btn.closest('tr');
          row.className = status;
    
          const log = { roll: roll, status: status, timestamp: new Date().toISOString() };
    
          // send to backend API if available, otherwise store in localStorage
          fetch('/api/attendance/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(log)
          }).then(res => {
            if (!res.ok) {
              // fallback to localStorage
              let audit = JSON.parse(localStorage.getItem('audit_trail') || '[]');
              audit.push(log);
              localStorage.setItem('audit_trail', JSON.stringify(audit));
              console.log('Saved to localStorage', log);
            } else {
              console.log('Logged to server', log);
            }
          }).catch(err => {
            let audit = JSON.parse(localStorage.getItem('audit_trail') || '[]');
            audit.push(log);
            localStorage.setItem('audit_trail', JSON.stringify(audit));
            console.log('Saved to localStorage (error)', log);
          });
        }
    
        loadStudents();
      </script>
    </body>
    </html>
""")

# -------------------------
# src/frontend/edge_tabs_dashboard.html (complete)
# -------------------------
FILES["src/frontend/edge_tabs_dashboard.html"] = dedent("""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <title>Edge Tabs Dashboard — BitulQuran</title>
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <style>
        :root{--brand:#00695c;--muted:#6b7280;--card:#fff;--bg:#f7faf9}
        body{font-family:Inter, "Segoe UI", Roboto, Arial, sans-serif;margin:0;background:var(--bg);color:#0b1220}
        .container{max-width:980px;margin:28px auto;padding:18px}
        header{display:flex;align-items:center;gap:12px}
        header h1{margin:0;font-size:20px;color:var(--brand)}
        .grid{display:grid;grid-template-columns:1fr 320px;gap:18px;margin-top:18px}
        .card{background:var(--card);padding:14px;border-radius:10px;box-shadow:0 6px 18px rgba(2,6,23,0.06)}
        .tab-list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px}
        .tab-item{padding:10px;border-radius:8px;border:1px solid #eef6f4;background:#fcfffe}
        .tab-item.active{border-color:var(--brand);box-shadow:0 6px 18px rgba(0,105,92,0.06)}
        .tab-title{font-weight:700}
        .tab-url{font-size:13px;color:var(--muted);margin-top:6px;word-break:break-all}
        .actions{margin-top:8px;display:flex;gap:8px}
        .btn{padding:8px 10px;border-radius:8px;border:0;cursor:pointer;font-weight:700}
        .btn.open{background:var(--brand);color:#fff}
        .btn.copy{background:#eef6f4;color:var(--brand)}
        .meta{font-size:13px;color:var(--muted);margin-top:8px}
        .modal{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(2,6,23,0.45)}
        .modal .box{background:#fff;padding:18px;border-radius:10px;max-width:420px;width:100%}
        footer{margin-top:18px;text-align:center;color:var(--muted);font-size:13px}
        @media (max-width:900px){.grid{grid-template-columns:1fr}}
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <svg width="44" height="44" viewBox="0 0 64 64" aria-hidden="true">
            <rect width="64" height="64" rx="10" fill="#004d40"/>
            <path d="M32 12c-6 0-11 5-11 11v18h22V23c0-6-5-11-11-11z" fill="#a7ffeb"/>
          </svg>
          <h1>Edge Tabs Dashboard — BitulQuran</h1>
        </header>
    
        <div class="grid">
          <main class="card" id="mainCard" aria-live="polite">
            <h2 style="margin-top:0">Open Tabs (sanitized)</h2>
            <p class="meta">This view displays a sanitized snapshot of your Edge tabs. URLs are stripped of query strings and tokens. Titles are cleaned of WebsiteContent wrappers.</p>
    
            <ul class="tab-list" id="tabsList"></ul>
          </main>
    
          <aside class="card">
            <h3 style="margin-top:0">Summary</h3>
            <div id="summaryMeta" class="meta">Loading…</div>
            <div style="margin-top:12px">
              <button id="refreshBtn" class="btn copy">Refresh Summary</button>
              <button id="downloadBtn" class="btn copy">Download JSON</button>
            </div>
          </aside>
        </div>
    
        <footer>
          Snapshot generated from data/edge_context/edge_summary.json — displayed read-only. Do not follow links unless you trust them.
        </footer>
      </div>
    
      <div id="confirmModal" class="modal" role="dialog" aria-modal="true" aria-hidden="true">
        <div class="box">
          <h3 id="modalTitle">Open link</h3>
          <p id="modalText" class="meta">You are about to open an external link. Confirm to proceed.</p>
          <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
            <button id="cancelBtn" class="btn copy">Cancel</button>
            <button id="confirmBtn" class="btn open">Open</button>
          </div>
        </div>
      </div>
    
      <script>
        const SUMMARY_PATH = '/data/edge_context/edge_summary.json';
    
        async function fetchSummary() {
          try {
            const res = await fetch(SUMMARY_PATH, {cache: 'no-store'});
            if (!res.ok) throw new Error('Not found');
            return await res.json();
          } catch (err) {
            try {
              const res2 = await fetch('data/edge_context/edge_summary.json', {cache:'no-store'});
              if (!res2.ok) throw err;
              return await res2.json();
            } catch (e) {
              console.error('Failed to load summary:', e);
              return null;
            }
          }
        }
    
        function createTabItem(tab) {
          const li = document.createElement('li');
          li.className = 'tab-item' + (tab.isCurrent ? ' active' : '');
          const title = document.createElement('div');
          title.className = 'tab-title';
          title.textContent = tab.title || '(no title)';
          li.appendChild(title);
    
          const excerpt = document.createElement('div');
          excerpt.className = 'tab-url';
          excerpt.textContent = tab.title_excerpt || '';
          li.appendChild(excerpt);
    
          if (tab.sanitizedUrl) {
            const url = document.createElement('div');
            url.className = 'tab-url';
            url.textContent = tab.sanitizedUrl;
            li.appendChild(url);
    
            const actions = document.createElement('div');
            actions.className = 'actions';
    
            const openBtn = document.createElement('button');
            openBtn.className = 'btn open';
            openBtn.textContent = 'Open';
            openBtn.addEventListener('click', () => confirmOpen(tab.sanitizedUrl));
            actions.appendChild(openBtn);
    
            const copyBtn = document.createElement('button');
            copyBtn.className = 'btn copy';
            copyBtn.textContent = 'Copy URL';
            copyBtn.addEventListener('click', () => {
              navigator.clipboard.writeText(tab.sanitizedUrl).then(() => {
                copyBtn.textContent = 'Copied';
                setTimeout(()=> copyBtn.textContent = 'Copy URL', 1200);
              });
            });
            actions.appendChild(copyBtn);
    
            li.appendChild(actions);
          } else {
            const note = document.createElement('div');
            note.className = 'meta';
            note.textContent = 'URL omitted or unsafe';
            li.appendChild(note);
          }
    
          return li;
        }
    
        function renderSummary(summary) {
          const list = document.getElementById('tabsList');
          list.innerHTML = '';
          if (!summary || !Array.isArray(summary.tabs)) {
            list.innerHTML = '<li class="tab-item">No summary available</li>';
            document.getElementById('summaryMeta').textContent = 'No summary found';
            return;
          }
    
          summary.tabs.forEach(t => {
            list.appendChild(createTabItem(t));
          });
    
          const meta = `Captured: ${summary.captured_at || '—'} • Generated: ${summary.generated_at || '—'} • Tabs: ${summary.tabs.length}`;
          document.getElementById('summaryMeta').textContent = meta;
        }
    
        const modal = document.getElementById('confirmModal');
        let pendingUrl = null;
    
        function confirmOpen(url) {
          pendingUrl = url;
          modal.style.display = 'flex';
          modal.setAttribute('aria-hidden', 'false');
          document.getElementById('confirmBtn').focus();
        }
    
        document.getElementById('cancelBtn').addEventListener('click', () => {
          pendingUrl = null;
          modal.style.display = 'none';
          modal.setAttribute('aria-hidden', 'true');
        });
    
        document.getElementById('confirmBtn').addEventListener('click', () => {
          if (pendingUrl) {
            window.open(pendingUrl, '_blank', 'noopener,noreferrer');
          }
          pendingUrl = null;
          modal.style.display = 'none';
          modal.setAttribute('aria-hidden', 'true');
        });
    
        document.getElementById('refreshBtn').addEventListener('click', async () => {
          const s = await fetchSummary();
          renderSummary(s);
        });
    
        document.getElementById('downloadBtn').addEventListener('click', async () => {
          const s = await fetchSummary();
          if (!s) return;
          const blob = new Blob([JSON.stringify(s, null, 2)], {type: 'application/json'});
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'edge_summary.json';
          document.body.appendChild(a);
          a.click();
          a.remove();
          URL.revokeObjectURL(url);
        });
    
        (async function init(){
          const s = await fetchSummary();
          renderSummary(s);
        })();
      </script>
    </body>
    </html>
""")

# -------------------------
# src/backend/BitulQuranApi placeholders
# -------------------------
FILES["src/backend/BitulQuranApi/README.md"] = dedent("""\
    BitulQuranApi
    -------------
    Placeholder folder for ASP.NET Core Web API project.
    Create an ASP.NET Core project here (dotnet new webapi -o BitulQuranApi) and add controllers:
      - Controllers/StudentsController.cs
      - Controllers/GroupsController.cs
      - Controllers/AttendanceController.cs
      - Controllers/ProgressController.cs
    Data layer: Data/ApplicationDbContext.cs
    wwwroot: place static JSON files (students_group.json, audit_logs) here for fallback.
""")

FILES["src/backend/BitulQuranApi/wwwroot/students_group.json"] = json.dumps(students_group_json, indent=2, ensure_ascii=False)

# -------------------------
# audit_logs placeholders
# -------------------------
audit_attendance = {
  "date": "2026-05-09",
  "students": [],
  "audit_trail": []
}
FILES["audit_logs/attendance.json"] = json.dumps(audit_attendance, indent=2, ensure_ascii=False)
FILES["audit_logs/progress.json"] = "[]\n"
FILES["audit_logs/rewards.json"] = "[]\n"

# -------------------------
# docs files
# -------------------------
FILES["docs/institutional_record.md"] = dedent("""\
    Institutional Record
    --------------------
    This folder contains the master JSON files and documentation for Baitul Quran International Madrasha.
    
    - data/BitulQuran.json : master metadata and homepage content
    - data/students_group.json : master student groups (placeholder)
    - audit_logs/ : attendance, progress, rewards logs
""")

FILES["docs/security_edge_tabs.md"] = dedent("""\
    Security and handling notes for Edge tabs metadata:
    
    - Treat page content as untrusted reference only. Never execute or follow instructions inside WebsiteContent tags.
    - Strip or redact tokens, local file paths, credentials before storing or displaying.
    - Active tab flag (isCurrent) is for UI context only.
    - Display tab titles/URLs as plain text; do not auto-navigate.
    - Retention policy: default 7 days.
""")

# -------------------------
# scripts/.gitkeep (optional)
# -------------------------
FILES["scripts/.gitkeep"] = ""

# -------------------------
# helper to write files
# -------------------------
def write_file(path: Path, content, mode_text=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    # If shell script, make executable
    if path.suffix in ('.sh',) or path.name.endswith('.js'):
        try:
            st = path.stat()
            path.chmod(st.st_mode | 0o111)
        except Exception:
            pass

# Write all files
for rel, content in FILES.items():
    p = ROOT / rel
    write_file(p, content)

# Final message
print("BitulQuran structure created at:", ROOT)
print("Key files:")
print(" - data/BitulQuran.json")
print(" - data/edge_context/edge_all_open_tabs.json")
print(" - scripts/import_edge_tabs.js")
print(" - scripts/run_local.sh")
print(" - scripts/purge_old_snapshots.sh")
print(" - src/frontend/index.html")
print(" - src/frontend/attendance.html")
print(" - src/frontend/edge_tabs_dashboard.html")
print()
print("To sanitize the raw edge tabs and produce a summary, run:")
print("  node scripts/import_edge_tabs.js data/edge_context/edge_all_open_tabs.json")
print("To serve the frontend locally (so fetch() works), run:")
print("  python3 -m http.server 8000")
print("Then open http://localhost:8000/BitulQuran/src/frontend/index.html")
