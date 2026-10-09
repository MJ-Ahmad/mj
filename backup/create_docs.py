#!/usr/bin/env python3
"""
generate_docs_hub.py

Creates four files in the current directory:
 - mj.json        (structured documentation data)
 - index.html     (production-ready homepage that loads mj.json)
 - schema.json    (JSON Schema for mj.json)
 - validate.py    (utility to validate mj.json against schema.json)

Run:
    python generate_docs_hub.py
"""

import json
from pathlib import Path
from textwrap import dedent

OUT = Path.cwd()

# -------------------------
# mj.json content (professional)
# -------------------------
mj = {
  "meta": {
    "title": "MJ-Ahmad Documentation Hub — Constitutional Index",
    "curated_by": "MJ Ahmad — Steward of Ethical Inheritance",
    "document_type": "System Index",
    "last_updated": "October 19, 2025",
    "declaration": "This index is not a directory. It is a declaration — that every module, every steward, and every learner deserves clarity, dignity, and traceable inheritance.",
    "quote": {
      "text": "Let no file be lost, no steward forgotten, and no learner left behind.",
      "author": "MJ Ahmad"
    }
  },
  "modules": [
    { "name": "🏛️ Core Modules", "items": ["Constitution", "Whitepaper", "Roadmap", "Glossary", "Contributor Registry"] },
    { "name": "🧠 Logic & Ethics", "items": ["NXN Genesis", "Ethics Manifesto", "Violation Ledger"] },
    { "name": "🧾 Governance", "items": ["Role Activation", "Voting Policy", "Emergency Protocol", "Ratification Ledger"] },
    { "name": "🧠 Behavioral Governance", "items": ["Persona Consistency and Ethical Tone"] },
    { "name": "🛡️ Security Protocols", "items": ["Threat Model", "Incident Response", "Guardian Handbook"] },
    { "name": "💰 Treasury System", "items": ["Purpose Registry", "Disbursement Log"] },
    { "name": "🧮 Merit System", "items": ["Contribution Scorecard and Recognition Logic"] },
    { "name": "📦 Distribution", "items": ["Copy logistics and dissemination protocols"] },
    { "name": "🚀 Deployment Records", "items": ["Setup instructions and activation history"] },
    { "name": "🪙 Tokenomics", "items": ["Value logic and ethical circulation"] },
    { "name": "📚 Quraner Fariwala", "items": ["Research", "Restoration", "Legal Continuity", "Campaign", "Donation Gateway"] },
    { "name": "🧾 Support & Clarity", "items": ["FAQ", "Vision", "Personal Fund Declaration", "Public Support Page"] }
  ],
  "nav": {
    "Home": "index.md",
    "Constitution": "constitution.md",
    "Whitepaper": "whitepaper.md",
    "Roadmap": "roadmap.md",
    "Glossary": "glossary.md",
    "Governance": {
      "Visionary Roles": "visionary-roles.md",
      "Persona Consistency": "behavior/persona-consistency.md",
      "Proposal Template": "governance/proposal-template.md",
      "Decision Tree": "https://github.com/mj-nexara/nexaragov-core/blob/main/decision-tree.md",
      "Voting Policy": "governance/voting-policy.md",
      "Emergency Protocol": "governance/emergency-protocol.md",
      "Ratification Process": "governance/ratification-process.md",
      "Ratified Actions": "governance/ratified-actions.md"
    },
    "Treasury": {
      "Treasury Policy": "https://github.com/mj-nexara/nexara-treasury/blob/main/README.md",
      "Purpose Registry": "treasury/purpose-registry.md",
      "Disbursement Log": "treasury/disbursement-log.md"
    },
    "Merit System": "merit-policy.md",
    "Deployment": {
      "Deployment Guide": "deployment-guide.md",
      "Deployment Record": "deployment-record.md"
    },
    "Tokenomics": "tokenomics.md",
    "Security": {
      "Threat Model": "security/threat-model.md",
      "Audit Log Policy": "audit-policy.md",
      "Incident Response": "security/incident-response.md",
      "Guardian Handbook": "security/guardian-handbook.md"
    },
    "Ethics Manifesto": "ethics.md",
    "Community": {
      "Community Charter": "community-charter.md",
      "FAQ": "faq.md",
      "Contributing": "CONTRIBUTING.md",
      "Vision": "vision.md"
    }
  }
}

# -------------------------
# schema.json (JSON Schema for mj.json)
# -------------------------
schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MJ Documentation Hub Schema",
  "type": "object",
  "required": ["meta", "modules", "nav"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["title", "curated_by", "document_type", "last_updated", "declaration", "quote"],
      "properties": {
        "title": {"type": "string"},
        "curated_by": {"type": "string"},
        "document_type": {"type": "string"},
        "last_updated": {"type": "string"},
        "declaration": {"type": "string"},
        "quote": {
          "type": "object",
          "required": ["text", "author"],
          "properties": {
            "text": {"type": "string"},
            "author": {"type": "string"}
          }
        }
      }
    },
    "modules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "items"],
        "properties": {
          "name": {"type": "string"},
          "items": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    },
    "nav": {
      "type": "object",
      "additionalProperties": True
    }
  }
}

# -------------------------
# index.html (production-ready, loads mj.json, includes search)
# -------------------------
index_html = dedent("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>MJ-Ahmad Documentation Hub</title>
  <style>
    :root{
      --bg:#f6f8fa; --card:#ffffff; --muted:#6b7280; --accent:#0b5fff; --border:#e6e9ee;
      --maxw:1100px;
    }
    html,body{height:100%;margin:0;background:var(--bg);font-family:Inter,Segoe UI,Arial,sans-serif;color:#111827}
    .wrap{max-width:var(--maxw);margin:28px auto;padding:24px}
    header{display:flex;align-items:flex-start;gap:18px}
    .brand{background:linear-gradient(135deg,#0b5fff,#6c8cff);color:#fff;padding:14px;border-radius:10px;min-width:72px;text-align:center}
    .brand h1{font-size:18px;margin:0;line-height:1.05}
    .meta{flex:1}
    .meta p{margin:4px 0;color:var(--muted);font-size:14px}
    .declaration{margin:18px 0;padding:16px;border-radius:8px;background:linear-gradient(180deg,rgba(11,95,255,0.03),transparent);border:1px solid var(--border);color:#1f2937}
    .grid{display:grid;grid-template-columns:1fr 320px;gap:20px}
    .card{background:var(--card);border:1px solid var(--border);padding:16px;border-radius:10px;box-shadow:0 1px 2px rgba(16,24,40,0.03)}
    .modules h2{margin:0 0 10px 0}
    .module{margin-bottom:14px}
    .module h3{margin:0 0 6px 0;font-size:15px}
    .module ul{margin:0;padding-left:18px;color:var(--muted)}
    nav ul{list-style:none;padding:0;margin:0}
    nav li{margin:6px 0}
    a{color:var(--accent);text-decoration:none}
    a:hover{text-decoration:underline}
    .search{display:flex;gap:8px;margin-bottom:12px}
    .search input{flex:1;padding:10px;border:1px solid var(--border);border-radius:8px}
    .search button{padding:10px 12px;border-radius:8px;border:1px solid var(--border);background:#fff;cursor:pointer}
    footer{margin-top:20px;color:var(--muted);font-size:13px}
    @media (max-width:900px){.grid{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brand">
        <h1>MJ-Ahmad<br/>Documentation Hub</h1>
      </div>
      <div class="meta">
        <h2 id="title">Loading…</h2>
        <p><strong>Curated by</strong> <span id="curated_by"></span></p>
        <p><strong>Type</strong> <span id="document_type"></span> · <strong>Updated</strong> <span id="last_updated"></span></p>
      </div>
    </header>

    <div class="declaration card" id="declaration">Loading declaration…</div>

    <div class="grid">
      <main class="card modules" id="main">
        <div class="search">
          <input id="searchInput" placeholder="Search modules, pages, or nav items" aria-label="Search documentation">
          <button id="clearBtn">Clear</button>
        </div>
        <div id="modules">Loading modules…</div>
      </main>

      <aside class="card">
        <h3>Navigation</h3>
        <nav id="nav">Loading navigation…</nav>
        <footer>
          <p id="quote" style="margin-top:12px;font-style:italic"></p>
        </footer>
      </aside>
    </div>
  </div>

  <script>
    async function load() {
      const res = await fetch('mj.json', {cache: 'no-store'});
      if (!res.ok) {
        document.getElementById('title').textContent = 'Documentation Hub (mj.json not found)';
        return;
      }
      const data = await res.json();
      const meta = data.meta || {};
      document.getElementById('title').textContent = meta.title || '';
      document.getElementById('curated_by').textContent = meta.curated_by || '';
      document.getElementById('document_type').textContent = meta.document_type || '';
      document.getElementById('last_updated').textContent = meta.last_updated || '';
      document.getElementById('declaration').textContent = meta.declaration || '';
      document.getElementById('quote').textContent = meta.quote ? `"${meta.quote.text}" — ${meta.quote.author}` : '';

      // Render modules
      const modulesEl = document.getElementById('modules');
      modulesEl.innerHTML = '';
      (data.modules || []).forEach(m => {
        const div = document.createElement('div');
        div.className = 'module';
        div.dataset.name = m.name || '';
        const itemsHtml = (m.items || []).map(i => `<li>${escapeHtml(i)}</li>`).join('');
        div.innerHTML = `<h3>${escapeHtml(m.name)}</h3><ul>${itemsHtml}</ul>`;
        modulesEl.appendChild(div);
      });

      // Render nav (recursive)
      const navEl = document.getElementById('nav');
      navEl.innerHTML = '';
      function renderNav(obj) {
        const ul = document.createElement('ul');
        for (const key in obj) {
          const value = obj[key];
          const li = document.createElement('li');
          if (typeof value === 'string') {
            li.innerHTML = `<a href="${escapeAttr(value)}" target="_blank" rel="noopener noreferrer">${escapeHtml(key)}</a>`;
            li.dataset.search = key + ' ' + value;
          } else {
            li.innerHTML = `<strong>${escapeHtml(key)}</strong>`;
            li.appendChild(renderNav(value));
            li.dataset.search = key;
          }
          ul.appendChild(li);
        }
        return ul;
      }
      navEl.appendChild(renderNav(data.nav || {}));

      // Search/filter
      const input = document.getElementById('searchInput');
      const clearBtn = document.getElementById('clearBtn');
      input.addEventListener('input', () => applyFilter(input.value.trim().toLowerCase()));
      clearBtn.addEventListener('click', () => { input.value=''; applyFilter(''); });

      function applyFilter(q) {
        // modules
        document.querySelectorAll('.module').forEach(node => {
          const name = node.dataset.name.toLowerCase();
          const items = Array.from(node.querySelectorAll('li')).map(li => li.textContent.toLowerCase()).join(' ');
          const match = !q || name.includes(q) || items.includes(q);
          node.style.display = match ? '' : 'none';
        });
        // nav
        document.querySelectorAll('#nav li').forEach(li => {
          const text = (li.textContent || '').toLowerCase();
          const match = !q || text.includes(q);
          li.style.display = match ? '' : 'none';
        });
      }

      // small helper escapes
      function escapeHtml(s){ return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
      function escapeAttr(s){ return String(s).replace(/"/g, '&quot;'); }
    }

    load().catch(err => {
      console.error(err);
      document.getElementById('title').textContent = 'Error loading mj.json';
    });
  </script>
</body>
</html>
""").strip()

# -------------------------
# validate.py (utility)
# -------------------------
validate_py = dedent("""
#!/usr/bin/env python3
\"\"\"validate.py

Validate mj.json against schema.json.

Usage:
    python validate.py mj.json schema.json

If 'jsonschema' package is not installed, the script will attempt a minimal structural check.
\"\"\"

import json
import sys
from pathlib import Path

def load(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        sys.exit(2)

def minimal_check(data, schema):
    # Basic required keys check
    missing = []
    for key in schema.get('required', []):
        if key not in data:
            missing.append(key)
    if missing:
        print('Minimal validation failed. Missing required keys:', ', '.join(missing))
        return False
    print('Minimal validation passed (required keys present).')
    return True

def main():
    if len(sys.argv) < 3:
        print('Usage: python validate.py mj.json schema.json')
        sys.exit(2)
    mj_path, schema_path = sys.argv[1], sys.argv[2]
    mj = load(mj_path)
    schema = load(schema_path)

    try:
        import jsonschema
        resolver = jsonschema.RefResolver(base_uri='file://' + str(Path(schema_path).resolve()), referrer=schema)
        jsonschema.validate(instance=mj, schema=schema, resolver=resolver)
        print('Validation successful: mj.json conforms to schema.json')
        sys.exit(0)
    except ImportError:
        print('jsonschema not installed; running minimal structural checks.')
        ok = minimal_check(mj, schema)
        sys.exit(0 if ok else 1)
    except jsonschema.ValidationError as e:
        print('Validation error:', e.message)
        sys.exit(1)

if __name__ == '__main__':
    main()
""").strip()

# -------------------------
# Write files
# -------------------------
def write_file(path: Path, content, mode='w', encoding='utf-8'):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)
    print(f'Wrote {path.name}')

write_file(OUT / 'mj.json', json.dumps(mj, indent=2, ensure_ascii=False))
write_file(OUT / 'schema.json', json.dumps(schema, indent=2, ensure_ascii=False))
write_file(OUT / 'index.html', index_html)
write_file(OUT / 'validate.py', validate_py)
print('All files created. To validate run: python validate.py mj.json schema.json')
