Help me to setup nav menu all as correctly and activate


---

BQ\
 - index.html
 - bq.json
 - bq_config.json

---

index.html

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Baitul Quran International Madrasha — Master</title>
<meta name="description" content="Baitul Quran International Madrasha — institutional master viewer, attendance, curriculum, staff and roadmap." />
<style>
  :root{--accent:#0b5a3a;--muted:#666;--bg:#fafafa;--card:#fff}
  html,body{height:100%}
  body{font-family:Inter,system-ui,Segoe UI,Roboto,Arial,sans-serif;margin:0;color:#222;background:#fff;display:flex;flex-direction:column}
  header{display:flex;align-items:center;gap:14px;padding:18px;background:linear-gradient(90deg,#f7fff9,#f0fff4);border-bottom:1px solid #e9f3ec}
  header img{height:64px;width:auto;border-radius:6px;object-fit:contain}
  header .title{font-size:18px;font-weight:700}
  header .subtitle{font-size:0.95rem;color:var(--muted)}
  .layout{display:flex;flex:1;min-height:0}
  nav{width:320px;border-right:1px solid #eee;padding:14px;background:var(--bg);overflow:auto}
  main{flex:1;padding:20px;overflow:auto}
  footer{padding:12px;border-top:1px solid #eee;background:#fafafa;font-size:0.9em;color:var(--muted);display:flex;justify-content:space-between;align-items:center}
  .menu-item{padding:10px;border-radius:8px;margin-bottom:8px;cursor:pointer;display:block}
  .menu-item.locked{opacity:0.6}
  .menu-item:hover{background:#f0fff4}
  .menu-title{font-weight:600}
  .menu-sub{font-size:0.85rem;color:#666;margin-top:4px}
  .meta{color:var(--muted);font-size:0.95em;margin-bottom:8px}
  .section{margin-bottom:20px}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
  .card{border:1px solid #eee;padding:12px;border-radius:10px;background:var(--card);box-shadow:0 1px 2px rgba(0,0,0,0.02)}
  table{width:100%;border-collapse:collapse}
  th,td{border:1px solid #eee;padding:8px;text-align:left}
  thead{background:#fafafa}
  .search{display:flex;gap:8px;margin-bottom:12px}
  .search input{flex:1;padding:8px;border:1px solid #ddd;border-radius:6px}
  .lang-toggle{margin-left:auto;display:flex;gap:6px}
  .btn{padding:8px 10px;border-radius:6px;border:1px solid #ddd;background:#fff;cursor:pointer}
  .btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
  .countdown{font-weight:700;color:var(--accent)}
  @media (max-width:900px){
    nav{width:100%;order:2;border-top:1px solid #eee}
    .layout{flex-direction:column}
  }
</style>
</head>
<body>
<header>
  <img id="logo" src="assets/logo.png" alt="logo" onerror="this.style.display='none'">
  <div>
    <div class="title" id="instName">Baitul Quran International Madrasha</div>
    <div class="subtitle" id="instAddress">Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh</div>
  </div>
  <div class="lang-toggle" aria-hidden="false">
    <button id="langEn" class="btn">EN</button>
    <button id="langBn" class="btn">BN</button>
  </div>
</header>

<div class="layout" role="main">
  <nav id="nav" aria-label="Primary navigation">
    <h3 style="margin-top:0">Menu</h3>
    <div id="menuList" aria-live="polite">Loading menu…</div>
    <hr style="margin:12px 0">
    <h4 style="margin:8px 0 6px 0">Quick Links</h4>
    <div id="quickLinks"></div>
  </nav>

  <main id="main" aria-live="polite">
    <div id="content">
      <h2>Overview</h2>
      <div id="overview" class="meta">Loading…</div>

      <div class="search" role="search">
        <input id="globalSearch" placeholder="Search students, staff, departments..." aria-label="Search">
        <select id="filterDept" aria-label="Filter by department"><option value="">All departments</option></select>
        <button id="clearSearch" class="btn">Clear</button>
      </div>

      <div id="pageArea"></div>
    </div>
  </main>
</div>

<footer id="footer" role="contentinfo">
  <div id="footerLeft">© Baitul Quran International Madrasha</div>
  <div id="footerRight">Last updated: <span id="lastUpdated">—</span></div>
</footer>

<script>
/*
index.html viewer
- Loads bq.json and site_config.json
- Renders menu according to site_config
- Supports password-protected items and countdown visibility
- EN | BN toggle
*/

const MASTER_JSON = 'bq.json';
const CONFIG_JSON = 'bq_config.json';

let master = null;
let config = null;
let lang = 'en';

async function fetchJson(path) {
  try {
    const r = await fetch(path, {cache: 'no-store'});
    if (!r.ok) throw new Error('Fetch failed: ' + r.status);
    return await r.json();
  } catch (e) {
    console.error(e);
    return null;
  }
}

function formatHeader() {
  const md = master.institution || {};
  document.getElementById('instName').innerText = md.name || 'Baitul Quran International Madrasha';
  document.getElementById('instAddress').innerText = md.address || '';
  document.getElementById('lastUpdated').innerText = md.last_updated || master.meta?.generated_at || '';
  const logo = document.getElementById('logo');
  if (md.logo) logo.src = md.logo;
}

function buildMenu() {
  const menuList = document.getElementById('menuList');
  menuList.innerHTML = '';
  const items = (config && config.menu) ? config.menu : [];
  items.forEach(item => {
    // countdown visibility
    if (item.countdown_until) {
      const until = new Date(item.countdown_until);
      if (new Date() > until && item.hide_after_countdown) return;
    }
    const el = document.createElement('div');
    el.className = 'menu-item' + (item.password_protected ? ' locked' : '');
    el.dataset.key = item.key;
    const title = document.createElement('div');
    title.className = 'menu-title';
    title.innerText = labelFor(item);
    const sub = document.createElement('div');
    sub.className = 'menu-sub';
    sub.innerText = item.subtitle || '';
    el.appendChild(title);
    el.appendChild(sub);
    el.addEventListener('click', () => onMenuClick(item));
    menuList.appendChild(el);
  });
  // quick links
  const q = document.getElementById('quickLinks');
  q.innerHTML = '';
  const links = [
    {label: lang === 'bn' ? 'হোম' : 'Home', key: 'overview'},
    {label: lang === 'bn' ? 'শিক্ষক' : 'Teachers', key: 'teachers'},
    {label: lang === 'bn' ? 'শিক্ষার্থী' : 'Students', key: 'students'},
    {label: lang === 'bn' ? 'হাজিরা' : 'Attendance', key: 'attendance'}
  ];
  links.forEach(l => {
    const a = document.createElement('a');
    a.href = '#';
    a.innerText = l.label;
    a.style.display = 'inline-block';
    a.style.marginRight = '8px';
    a.addEventListener('click', (e) => { e.preventDefault(); const item = (config.menu||[]).find(m=>m.key===l.key); if(item) onMenuClick(item); });
    q.appendChild(a);
  });
}

function labelFor(item) {
  if (lang === 'bn' && item.label_bn) return item.label_bn;
  return item.label || item.key;
}

function onMenuClick(item) {
  if (item.password_protected) {
    const pw = prompt('Enter password to view this section:');
    if (pw !== item.password) {
      alert('Incorrect password');
      return;
    }
  }
  if (item.countdown_until) {
    const until = new Date(item.countdown_until);
    if (new Date() < until && item.show_countdown) {
      const ms = until - new Date();
      const days = Math.floor(ms / (1000*60*60*24));
      const hours = Math.floor((ms / (1000*60*60)) % 24);
      alert('This item is available until ' + until.toLocaleString() + ' (remaining: ' + days + 'd ' + hours + 'h)');
    }
  }
  renderSection(item);
}

function renderSection(item) {
  const area = document.getElementById('pageArea');
  area.innerHTML = '';
  if (item.key === 'overview') { renderOverview(area); return; }
  if (item.key === 'teachers') { renderTeachers(area); return; }
  if (item.key === 'students') { renderStudents(area); return; }
  if (item.key === 'attendance') { renderAttendance(area); return; }
  if (item.key === 'curriculum') { renderCurriculum(area); return; }
  if (item.key === 'roadmap') { renderRoadmap(area); return; }
  if (item.json_path) {
    const data = getByPath(master, item.json_path);
    area.innerHTML = `<pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>`;
    return;
  }
  area.innerHTML = `<p>Section "${item.key}" not implemented in viewer.</p>`;
}

function renderOverview(area) {
  const md = master.institution || {};
  const html = `
    <div class="section card">
      <h3>${md.name || ''}</h3>
      <p>${md.mission || ''}</p>
      <div class="meta">Curated by: ${md.curated_by || ''} • Established: ${md.established || ''}</div>
    </div>
    <div class="section grid">
      <div class="card"><strong>Pedagogy</strong><p>Spaced repetition, daily micro-practice, teacher-led correction.</p></div>
      <div class="card"><strong>Technology</strong><p>Attendance master, HTML viewer, snapshots, planned web UI.</p></div>
      <div class="card"><strong>Ethics</strong><p>Character formation, community service, accountability.</p></div>
    </div>
  `;
  area.innerHTML = html;
}

function renderTeachers(area) {
  const t = master.staff?.teachers || [];
  let html = '<div class="section"><h3>Teachers</h3><div class="grid">';
  t.forEach(x => {
    html += `<div class="card"><strong>${x.name}</strong><div style="font-size:0.95em;color:#666">${x.role}</div><div style="margin-top:8px;font-size:0.9em">${x.phone || ''}</div></div>`;
  });
  html += '</div></div>';
  area.innerHTML = html;
}

function renderStudents(area) {
  const s = master.students?.serial_master_list || [];
  let html = '<div class="section"><h3>Students — Serial Master List</h3><table><thead><tr><th>Serial</th><th>Roll</th><th>ID</th><th>Name</th><th>Dept</th></tr></thead><tbody>';
  s.forEach(x => {
    html += `<tr><td>${x.serial}</td><td>${x.roll}</td><td>${x.id}</td><td>${x.name}</td><td>${x.department}</td></tr>`;
  });
  html += '</tbody></table></div>';
  area.innerHTML = html;
}


function renderGroups(area) {
  const g = master.groups || [];
  if (!g.length) {
    area.innerHTML = '<div class="empty">No groups available</div>';
    return;
  }

  let html = '<div class="section"><h3>Groups</h3><div class="grid">';
  g.forEach(x => {
    // Count students per department
    const deptCounts = {};
    x.students.forEach(s => {
      const dept = s.department || 'Unknown';
      deptCounts[dept] = (deptCounts[dept] || 0) + 1;
    });
    const deptSummary = Object.entries(deptCounts)
      .map(([dept, count]) => `${count} from ${dept}`)
      .join(' • ');

    // Student rows for expand/collapse
    const studentRows = x.students.map(s =>
      `<tr><td>${s.roll || ''}</td><td>${s.id || ''}</td><td>${s.name}</td><td>${s.department}</td></tr>`
    ).join('');

    html += `
      <div class="card" data-group="${x.group}" data-ustad="${x.ustad}">
        <strong>Group ${x.group}</strong>
        <div style="font-size:0.95em;color:#666">${x.ustad}</div>
        <div style="margin-top:8px;font-size:0.9em">${x.students.length} students</div>
        <div style="margin-top:4px;font-size:0.85em;color:#444">${deptSummary}</div>
        <div class="toggle" style="margin-top:8px">
          <a href="#" onclick="toggleGroup(event, '${x.group}')">Show Students</a>
        </div>
        <div id="group-${x.group}" class="student-list" style="display:none;margin-top:8px">
          <table><thead><tr><th>Roll</th><th>ID</th><th>Name</th><th>Dept</th></tr></thead><tbody>
            ${studentRows}
          </tbody></table>
        </div>
      </div>`;
  });
  html += '</div></div>';
  area.innerHTML = html;
}

function toggleGroup(ev, groupId) {
  ev.preventDefault();
  const el = document.getElementById('group-' + groupId);
  if (!el) return;
  const visible = el.style.display === 'block';
  el.style.display = visible ? 'none' : 'block';
  ev.target.textContent = visible ? 'Show Students' : 'Hide Students';
}


function renderAttendance(area) {
  const att = master.attendance_master || master.attendance || null;
  if (!att) {
    area.innerHTML = '<div class="card"><p>No attendance master embedded. Use attendance system to append records to master/attendance_master.json.</p></div>';
    return;
  }
  const recs = att.records || [];
  let html = '<div class="section"><h3>Attendance Records (latest)</h3>';
  if (recs.length === 0) html += '<p>No records yet.</p>';
  else {
    html += '<div class="grid">';
    recs.slice(-6).reverse().forEach(r => {
      html += `<div class="card"><strong>${r.meta.date} — ${r.meta.department}</strong><div class="meta">${r.meta.mode} • ${r.meta.scheduled_time}</div><div style="margin-top:8px"><a href="#" onclick="showAttendanceRecord(event, \\'${r.meta.id}\\')">View</a></div></div>`;
    });
    html += '</div>';
  }
  html += '</div><div id="attendanceDetail"></div>';
  area.innerHTML = html;
}

function showAttendanceRecord(ev, id) {
  ev.preventDefault();
  const att = master.attendance_master || master.attendance || null;
  if (!att) return;
  const rec = (att.records || []).find(r => r.meta.id === id);
  if (!rec) return alert('Record not found');
  const detail = document.getElementById('attendanceDetail');
  let html = `<h4>Record: ${rec.meta.id}</h4><table><thead><tr><th>Roll</th><th>ID</th><th>Name</th><th>Status</th></tr></thead><tbody>`;
  rec.attendance.forEach(a => {
    html += `<tr><td>${a.roll}</td><td>${a.student_id}</td><td>${a.name}</td><td>${a.status_label}</td></tr>`;
  });
  html += '</tbody></table>';
  detail.innerHTML = html;
}

function renderCurriculum(area) {
  const cur = master.curriculum || {};
  let html = `<div class="section"><h3>Curriculum</h3><div class="meta">${(cur.principles||[]).join(', ')}</div>`;
  if (cur.modules) {
    html += '<div class="grid">';
    cur.modules.forEach(m => {
      html += `<div class="card"><strong>${m.title}</strong><div>Code: ${m.code}</div><div>Hours: ${m.hours}</div></div>`;
    });
    html += '</div>';
  }
  html += '</div>';
  area.innerHTML = html;
}

function renderRoadmap(area) {
  const r = master.roadmap || {};
  let html = '<div class="section"><h3>Roadmap</h3>';
  for (const k of Object.keys(r)) {
    html += `<div class="card"><strong>${k}</strong><div style="margin-top:8px">${r[k].join(', ')}</div></div>`;
  }
  html += '</div>';
  area.innerHTML = html;
}

function getByPath(obj, path) {
  const parts = path.split('.');
  let cur = obj;
  for (const p of parts) {
    if (!cur) return null;
    cur = cur[p];
  }
  return cur;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

async function init() {
  master = await fetchJson(MASTER_JSON);
  config = await fetchJson(CONFIG_JSON) || {menu: []};
  if (!master) {
    document.getElementById('overview').innerText = 'Failed to load master JSON.';
    return;
  }
  formatHeader();
  buildMenu();
  populateDeptFilter();
  renderOverview(document.getElementById('pageArea'));
}

function populateDeptFilter() {
  const sel = document.getElementById('filterDept');
  const depts = (master.departments || []).map(d => d.name);
  depts.forEach(d => {
    const opt = document.createElement('option');
    opt.value = d; opt.innerText = d;
    sel.appendChild(opt);
  });
}

document.getElementById('langEn').addEventListener('click', () => { lang='en'; buildMenu(); renderOverview(document.getElementById('pageArea')); });
document.getElementById('langBn').addEventListener('click', () => { lang='bn'; buildMenu(); renderOverview(document.getElementById('pageArea')); });

document.getElementById('globalSearch').addEventListener('input', (e) => {
  const q = e.target.value.trim().toLowerCase();
  const area = document.getElementById('pageArea');
  if (!q) { renderOverview(area); return; }
  const s = master.students?.serial_master_list || [];
  const found = s.filter(x => (x.name||'').toLowerCase().includes(q) || (x.id||'').toLowerCase().includes(q) || (x.roll||'').toLowerCase().includes(q));
  let html = '<div class="section"><h3>Search results</h3>';
  if (found.length === 0) html += '<p>No results</p>';
  else {
    html += '<table><thead><tr><th>Serial</th><th>Roll</th><th>ID</th><th>Name</th><th>Dept</th></tr></thead><tbody>';
    found.forEach(x => html += `<tr><td>${x.serial}</td><td>${x.roll}</td><td>${x.id}</td><td>${x.name}</td><td>${x.department}</td></tr>`);
    html += '</tbody></table>';
  }
  html += '</div>';
  area.innerHTML = html;
});

document.getElementById('clearSearch').addEventListener('click', () => {
  document.getElementById('globalSearch').value = '';
  renderOverview(document.getElementById('pageArea'));
});

init();
</script>
</body>
</html>


---

bq.json

{
  "institution": {
    "name": "Baitul Quran International Madrasha",
    "short_name": "Bitul Quran",
    "address": "Stadium Road, Nandibari, Muktagacha Upazila, Mymensingh, Bangladesh",
    "phone": "+8801824401812",
    "email": "info@baitulquran.example",
    "website": "https://baitulquran.example",
    "logo": "assets/logo.png",
    "curated_by": "MJ Ahmad — Steward of Ethical Inheritance",
    "established": "2018-09-01",
    "mission": "To combine classical hifz pedagogy with modern learning technology to produce confident, ethical, and proficient memorizers of the Qur'an.",
    "vision": "A globally recognized center of excellence for Quran memorization and ethical leadership.",
    "document_type": "Institutional Record",
    "last_updated": "2026-05-03T02:45:02+06:00"
  },

  "governance": {
    "board": [
      {"name": "Sheikh Rahman", "role": "Chairman"},
      {"name": "Dr. Farida Khan", "role": "Secretary"}
    ],
    "director": {"name": "MJ Ahmad", "title": "Director"},
    "roles_and_responsibilities": {
      "director": "Strategic leadership, external relations, fundraising.",
      "academic_head": "Curriculum, teacher training, quality assurance.",
      "operations_manager": "Facilities, scheduling, logistics.",
      "it_manager": "Systems, backups, security, attendance platform."
    }
  },

  "staff": {
    "teachers": [
      {"id": "T01", "name": "Ustad Arif", "phone": "01824401812", "role": "Senior Ustad", "department": "Khatmi / Recitation"},
      {"id": "T02", "name": "Ustad Arif Robbani", "phone": "01631940605", "role": "Nurani Instructor", "department": "Nurani Maktab"},
      {"id": "T03", "name": "Ustad Jafor", "phone": "01892051303", "role": "Hifz Instructor", "department": "Hifz 1–29"}
    ],
    "administration": [
      {"id": "A01", "name": "Sadia Begum", "role": "Office Manager", "email": "office@baitulquran.example"},
      {"id": "A02", "name": "Rafiq Ahmed", "role": "Facilities Supervisor"}
    ],
    "it": [
      {"id": "IT01", "name": "Imran Hossain", "role": "IT Manager", "email": "it@baitulquran.example"}
    ]
  },

  "students": {
    "serial_master_list": [
      {"serial": 1, "name": "Faysal (1)", "roll": "03", "id": "BQSHK01", "department": "Khatmi / Recitation"},
      {"serial": 2, "name": "Sown", "roll": "04", "id": "BQSHK02", "department": "Khatmi / Recitation"},
      {"serial": 3, "name": "Abu Talha", "roll": "05", "id": "BQSHK03", "department": "Khatmi / Recitation"},
      {"serial": 4, "name": "Abdullah Al Mahi", "roll": "06", "id": "BQSHK04", "department": "Khatmi / Recitation"},
      {"serial": 5, "name": "Faysal (2)", "roll": "07", "id": "BQSHK05", "department": "Khatmi / Recitation"},
      {"serial": 6, "name": "Jarif", "roll": "08", "id": "BQSHK06", "department": "Khatmi / Recitation"},
      {"serial": 7, "name": "Asif", "roll": "09", "id": "BQSHK07", "department": "Khatmi / Recitation"},
      {"serial": 8, "name": "Jihad", "roll": "10", "id": "BQSHK08", "department": "Khatmi / Recitation"},
      {"serial": 9, "name": "Sakib", "roll": "11", "id": "BQSHK09", "department": "Khatmi / Recitation"},
      {"serial": 10, "name": "Tawfiq", "roll": "12", "id": "BQSHK10", "department": "Khatmi / Recitation"},
      {"serial": 11, "name": "Mosaddek", "roll": "31", "id": "BQSHK11", "department": "Khatmi / Recitation"},
      {"serial": 12, "name": "Jubayer", "roll": "01", "id": "BQSHS01", "department": "Hifz 1–10"},
      {"serial": 13, "name": "Sabbir", "roll": "17", "id": "BQSHS02", "department": "Hifz 1–10"},
      {"serial": 14, "name": "Afrad", "roll": "19", "id": "BQSHS03", "department": "Hifz 1–10"},
      {"serial": 15, "name": "Rahat", "roll": "20", "id": "BQSHS04", "department": "Hifz 1–10"},
      {"serial": 16, "name": "Abid", "roll": "21", "id": "BQSHS05", "department": "Hifz 1–10"},
      {"serial": 17, "name": "Arafat (2)", "roll": "22", "id": "BQSHS06", "department": "Hifz 1–10"},
      {"serial": 18, "name": "Akib", "roll": "28", "id": "BQSHS07", "department": "Hifz 1–10"},
      {"serial": 19, "name": "Amir Hamja", "roll": "29", "id": "BQSHS08", "department": "Hifz 1–10"},
      {"serial": 20, "name": "Nabil", "roll": "30", "id": "BQSHS09", "department": "Hifz 1–10"},
      {"serial": 21, "name": "Junayed", "roll": "33", "id": "BQSHS10", "department": "Hifz 1–10"},
      {"serial": 22, "name": "Mafin", "roll": "13", "id": "BQSHS11", "department": "Hifz 1–20"},
      {"serial": 23, "name": "Hasib", "roll": "14", "id": "BQSHS12", "department": "Hifz 1–20"},
      {"serial": 24, "name": "Sahadat", "roll": "15", "id": "BQSHS13", "department": "Hifz 1–20"},
      {"serial": 25, "name": "Hujayfa", "roll": "18", "id": "BQSHS14", "department": "Hifz 1–20"},
      {"serial": 26, "name": "Al‑Amin", "roll": "25", "id": "BQSHS15", "department": "Hifz 1–20"},
      {"serial": 27, "name": "Shoyab", "roll": "34", "id": "BQSHS16", "department": "Hifz 1–20"},
      {"serial": 28, "name": "Junayed", "roll": "35", "id": "BQSHS17", "department": "Hifz 1–20"},
      {"serial": 29, "name": "Anamul Haqe", "roll": "02", "id": "BQSHS18", "department": "Hifz 1–29"},
      {"serial": 30, "name": "Arafat (1)", "roll": "16", "id": "BQSHS19", "department": "Hifz 1–29"},
      {"serial": 31, "name": "Sayem", "roll": "26", "id": "BQSHS20", "department": "Hifz 1–29"},
      {"serial": 32, "name": "Tahmid", "roll": "27", "id": "BQSHS21", "department": "Hifz 1–29"},
      {"serial": 33, "name": "Abu Talha", "roll": "01", "id": "BQSNA01", "department": "Pre-Hifz Nazara"},
      {"serial": 34, "name": "Kawser Ahmad", "roll": "02", "id": "BQSNA02", "department": "Pre-Hifz Nazara"},
      {"serial": 35, "name": "Sifat", "roll": "03", "id": "BQSNA03", "department": "Pre-Hifz Nazara"},
      {"serial": 36, "name": "Shahinur", "roll": "04", "id": "BQSNA04", "department": "Pre-Hifz Nazara"},
      {"serial": 37, "name": "Miraj", "roll": "05", "id": "BQSNA05", "department": "Pre-Hifz Nazara"},
      {"serial": 38, "name": "Minhaz", "roll": "06", "id": "BQSNA06", "department": "Pre-Hifz Nazara"},
      {"serial": 39, "name": "Lijon", "roll": "07", "id": "BQSNA07", "department": "Pre-Hifz Nazara"},
      {"serial": 40, "name": "Rafan", "roll": "08", "id": "BQSNA08", "department": "Pre-Hifz Nazara"},
      {"serial": 41, "name": "Arshad", "roll": "09", "id": "BQSNA09", "department": "Pre-Hifz Nazara"},
      {"serial": 42, "name": "Jidan", "roll": "01", "id": "BQSNU01", "department": "Nurani Maktab"},
      {"serial": 43, "name": "Safan", "roll": "02", "id": "BQSNU02", "department": "Nurani Maktab"},
      {"serial": 44, "name": "Moballig", "roll": "03", "id": "BQSNU03", "department": "Nurani Maktab"},
      {"serial": 45, "name": "Shoyaib", "roll": "04", "id": "BQSNU04", "department": "Nurani Maktab"},
      {"serial": 46, "name": "Sajjad", "roll": "05", "id": "BQSNU05", "department": "Nurani Maktab"},
      {"serial": 47, "name": "Tamim", "roll": "06", "id": "BQSNU06", "department": "Nurani Maktab"},
      {"serial": 48, "name": "Ruman", "roll": "07", "id": "BQSNU07", "department": "Nurani Maktab"},
      {"serial": 49, "name": "Mahdi", "roll": "08", "id": "BQSNU08", "department": "Nurani Maktab"},
      {"serial": 50, "name": "Soyad", "roll": "09", "id": "BQSNU09", "department": "Nurani Maktab"}
    ],
    "by_department": {
      "Khatmi / Recitation": ["BQSHK01","BQSHK02","BQSHK03","BQSHK04","BQSHK05","BQSHK06","BQSHK07","BQSHK08","BQSHK09","BQSHK10","BQSHK11"],
      "Hifz 1–10": ["BQSHS01","BQSHS02","BQSHS03","BQSHS04","BQSHS05","BQSHS06","BQSHS07","BQSHS08","BQSHS09","BQSHS10"],
      "Hifz 1–20": ["BQSHS11","BQSHS12","BQSHS13","BQSHS14","BQSHS15","BQSHS16","BQSHS17"],
      "Hifz 1–29": ["BQSHS18","BQSHS19","BQSHS20","BQSHS21"],
      "Pre-Hifz Nazara": ["BQSNA01","BQSNA02","BQSNA03","BQSNA04","BQSNA05","BQSNA06","BQSNA07","BQSNA08","BQSNA09"],
      "Nurani Maktab": ["BQSNU01","BQSNU02","BQSNU03","BQSNU04","BQSNU05","BQSNU06","BQSNU07","BQSNU08","BQSNU09"]
    },
    "policies": {
      "attendance": "Daily attendance required; excused absences documented; late policy applies.",
      "code_of_conduct": "Respectful behavior, punctuality, and adherence to madrasha rules.",
      "assessment": "Weekly recitation checks; monthly progress reports; quarterly exams."
    }
  },

  "groups": [
    {
      "ustad": "Ustad Jafor Ahmad",
      "group": "A",
      "students": [
        { "name": "Faysal (1)", "roll": "03", "id": "BQSHK01", "department": "Khatmi / Recitation" },
        { "name": "Sown", "roll": "04", "id": "BQSHK02", "department": "Khatmi / Recitation" },
        { "name": "Abu Talha", "roll": "05", "id": "BQSHK03", "department": "Khatmi / Recitation" }
      ]
    },
    {
      "ustad": "Ustad Arif",
      "group": "B",
      "students": [
        { "name": "Sabbir", "roll": "17", "id": "BQSHS02", "department": "Hifz 1–10" },
        { "name": "Rahat", "roll": "20", "id": "BQSHS04", "department": "Hifz 1–10" },
        { "name": "Arafat (2)", "roll": "22", "id": "BQSHS06", "department": "Hifz 1–10" }
      ]
    },
    {
      "ustad": "Ustad Arif Robbani",
      "group": "C",
      "students": [
        { "name": "Jidan", "roll": "01", "id": "BQSNU01", "department": "Nurani Maktab" },
        { "name": "Safan", "roll": "02", "id": "BQSNU02", "department": "Nurani Maktab" },
        { "name": "Moballig", "roll": "", 	"id": "", 		"department":"Nurani Maktab" }
      ]
    }
  ],

  "departments": [
    {"id": "D01", "name": "Nurani Maktab", "description": "Basic Quran reading and tajweed."},
    {"id": "D02", "name": "Pre-Hifz Nazara", "description": "Preparation for memorization."},
    {"id": "D03", "name": "Hifz 1–29", "description": "Full memorization program."},
    {"id": "D04", "name": "Khatmi / Recitation", "description": "Advanced recitation and revision."}
  ],

  "curriculum": {
    "principles": ["Spaced repetition", "Daily micro-practice", "Teacher-led correction", "Peer review"],
    "modules": [
      {"code": "C01", "title": "Nurani Foundations", "hours": 120},
      {"code": "C02", "title": "Nazara Preparation", "hours": 200},
      {"code": "C03", "title": "Hifz Core", "hours": 2000}
    ],
    "assessment_framework": {
      "weekly": "Recitation check by assigned Ustad",
      "monthly": "Progress report and parent update",
      "quarterly": "Formal assessment and placement review"
    }
  },

  "attendance_integration": {
    "master_file": "master/attendance_master.json",
    "snapshots_dir": "outputs/",
    "features": ["JSON master", "HTML viewer", "Markdown export", "teacher recorder", "atomic writes"],
    "policies": {"retention_years": 3, "backup": "daily"}
  },

  "technology": {
    "learning_tools": ["Audio-guided repetition", "Spaced repetition scheduler", "Mobile-friendly revision pages"],
    "infrastructure": {"server": "Static hosting; optional Flask + SQLite for multi-user", "backup": "Daily snapshot to outputs/"}
  },

  "roadmap": {
    "2026-Q2": ["Deploy web UI (Flask)", "Add SQLite history", "Teacher login"],
    "2026-Q3": ["QR check-in pilot", "Automated reports (CSV/PDF)", "Parent portal (read-only)"],
    "2027": ["Mobile app for revision", "AI-assisted tajweed feedback (research)"]
  },

  "goals": {
    "short_term": ["Stabilize master JSON workflow", "Publish attendance viewer", "Train 3 teachers on system"],
    "mid_term": ["Deploy Flask web UI", "Add authentication", "Start QR pilot"],
    "long_term": ["Global recognition for hifz pedagogy", "Research center for memorization methods"]
  },

  "contacts": {
    "director": {"name": "MJ Ahmad", "email": "director@baitulquran.example", "phone": "+8801712345678"},
    "office": {"email": "office@baitulquran.example", "phone": "+8801824401812"}
  },

  "meta": {
    "generated_at": "2026-05-03T02:45:02+06:00",
    "version": "1.0.0",
    "notes": "Master file for Bitul Quran institutional data; serial student list included."
  }
}


---

bq_config.json

{
  "menu": [
    {"key":"overview","label":"Overview","label_bn":"ওভারভিউ","subtitle":"Institution summary","password_protected":false},
    {"key":"people_roles","label":"People & Roles","label_bn":"কর্মকর্তা ও দায়িত্ব","subtitle":"Leadership, staff and responsibilities","password_protected":false},
    {"key":"teachers","label":"Teachers","label_bn":"শিক্ষকবৃন্দ","subtitle":"Staff directory","password_protected":false},
    {"key":"students","label":"Students","label_bn":"শিক্ষার্থী","subtitle":"Master student list","password_protected":false},
    {"key":"groups","label":"Groups","label_bn":"গ্রুপ","subtitle":"Student groups","password_protected":false},
    {"key":"attendance","label":"Attendance","label_bn":"হাজিরা","subtitle":"Attendance master","password_protected":false},
    {"key":"curriculum","label":"Curriculum","label_bn":"পাঠ্যক্রম","subtitle":"Curriculum & modules","password_protected":false},
    {"key":"roadmap","label":"Roadmap","label_bn":"রোডম্যাপ","subtitle":"Strategic roadmap","password_protected":false},
    {"key":"private_reports","label":"Private Reports","label_bn":"প্রাইভেট রিপোর্ট","subtitle":"Confidential","password_protected":true,"password":"change_this_password","countdown_until":"2026-06-01T00:00:00+06:00","hide_after_countdown":false,"show_countdown":true}
  ],
  "footer": {
    "left": "© Baitul Quran International Madrasha",
    "right": "Contact: abn-bq@outlook.com"
  }
}
