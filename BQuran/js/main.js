// js/main.js
// Loads BitulQuran.json, renders nav, groups, departments and provides onclick panel for Group A/B/C.

let currentLang = 'en';
let master = null;

async function fetchJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to fetch ${path} (${res.status})`);
  return res.json();
}

function t(obj) {
  if (!obj) return '';
  return obj[currentLang] || obj.en || Object.values(obj)[0] || '';
}

async function loadMaster() {
  try {
    master = await fetchJson('BitulQuran.json');
  } catch (err) {
    console.error(err);
    document.getElementById('hero-heading').textContent = 'Unable to load data';
    document.getElementById('hero-lead').textContent = err.message;
    return;
  }

  renderHeader();
  renderHero();
  renderFooter();
  renderGroupsList();
  renderDepartments();
  attachLangButtons();
}

function renderHeader() {
  const logo = document.getElementById('logo');
  logo.src = master.institution.logo || 'assets/logo.png';
  document.getElementById('site-title').textContent = master.institution.name;
  const nav = document.getElementById('nav');
  nav.innerHTML = '';

  const navItems = master.homepage && master.homepage.nav ? master.homepage.nav : master.navigation || [];
  navItems.forEach(item => {
    const li = document.createElement('li');
    li.className = 'nav-item';
    const a = document.createElement('a');
    a.href = item.href || '#';
    a.textContent = t(item.label || item);
    a.dataset.navId = item.id || '';
    // Intercept group nav clicks to open panel
    if (item.id && item.id.startsWith('group_')) {
      a.addEventListener('click', ev => {
        ev.preventDefault();
        const groupKey = item.id.replace('group_', '');
        openGroupPanel(groupKey);
      });
    }
    li.appendChild(a);
    nav.appendChild(li);
  });
}

function renderHero() {
  const hero = master.homepage && master.homepage.hero ? master.homepage.hero : (master.content && master.content.home ? master.content.home : null);
  document.getElementById('hero-heading').textContent = t(hero && hero.heading ? hero.heading : { en: 'Welcome' });
  document.getElementById('hero-lead').textContent = t(hero && hero.lead ? hero.lead : (hero && hero.description ? hero.description : { en: '' }));
}

function renderFooter() {
  const footerText = (master.footer && master.footer.text) ? t(master.footer.text) : `© ${new Date().getFullYear()} ${master.institution.name}.`;
  document.getElementById('footer-text').textContent = footerText;
}

function renderDepartments() {
  const container = document.getElementById('department-cards');
  container.innerHTML = '';
  const departments = master.departments || {};
  Object.keys(departments).forEach(key => {
    const dept = departments[key];
    const card = document.createElement('div');
    card.className = 'card dept-card';
    const title = t(dept.title || { en: dept.id || key });
    const desc = t(dept.description || { en: dept.description || '' });
    card.innerHTML = `<h3>${title}</h3><p class="muted">${desc}</p>`;
    container.appendChild(card);
  });
}

function renderGroupsList() {
  const container = document.getElementById('groups-list');
  container.innerHTML = '';

  // Prefer modular files if referenced
  const refs = master.data_files && master.data_files.groups ? master.data_files.groups : null;

  // If inline groups exist, use them for immediate rendering
  if (Array.isArray(master.groups) && master.groups.length) {
    master.groups.forEach(g => container.appendChild(makeGroupCard(g)));
    return;
  }

  // Otherwise fetch each referenced group file
  if (refs) {
    Object.keys(refs).forEach(async key => {
      try {
        const g = await fetchJson(refs[key]);
        container.appendChild(makeGroupCard(g));
      } catch (err) {
        console.warn('Group load failed', key, err);
      }
    });
  }
}

function makeGroupCard(group) {
  const card = document.createElement('div');
  card.className = 'card group-card';
  const studentsCount = Array.isArray(group.students) ? group.students.length : 0;
  card.innerHTML = `
    <h3>Group ${group.group} — ${group.ustad}</h3>
    <p class="muted">Students: <strong>${studentsCount}</strong></p>
    <div class="card-actions">
      <button class="view-group" data-group="${group.group}">View</button>
      <button class="download-json" data-ref="${group.group}">JSON</button>
    </div>
  `;
  card.querySelector('.view-group').addEventListener('click', () => openGroupPanel(group.group));
  card.querySelector('.download-json').addEventListener('click', () => downloadGroupJson(group));
  return card;
}

function downloadGroupJson(group) {
  // If modular file exists, open it; otherwise create a blob from inline data
  const refs = master.data_files && master.data_files.groups ? master.data_files.groups : null;
  const key = group;
  if (refs && refs[key]) {
    window.open(refs[key], '_blank');
    return;
  }
  const inline = Array.isArray(master.groups) ? master.groups.find(g => g.group === key) : null;
  if (!inline) return alert('Group JSON not available');
  const blob = new Blob([JSON.stringify(inline, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `group_${key}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

async function openGroupPanel(groupKey) {
  const panel = document.getElementById('group-panel');
  const content = document.getElementById('group-panel-content');
  content.innerHTML = '<p class="muted">Loading group…</p>';
  panel.classList.remove('hidden');
  panel.setAttribute('aria-hidden', 'false');

  // Try modular file first
  const refs = master.data_files && master.data_files.groups ? master.data_files.groups : null;
  try {
    let groupData = null;
    if (refs && refs[groupKey]) {
      groupData = await fetchJson(refs[groupKey]);
    } else if (Array.isArray(master.groups)) {
      groupData = master.groups.find(g => g.group === groupKey);
    }

    if (!groupData) throw new Error('Group not found');

    // Render table
    const rows = (groupData.students || []).map(s => {
      const roll = s.roll || '—';
      const id = s.id || '—';
      const dept = s.department || '—';
      return `<tr><td>${escapeHtml(roll)}</td><td>${escapeHtml(s.name)}</td><td>${escapeHtml(id)}</td><td>${escapeHtml(dept)}</td></tr>`;
    }).join('');

    content.innerHTML = `
      <h2 id="group-panel-title">Group ${groupData.group} — ${groupData.ustad}</h2>
      <p class="muted">Total students: <strong>${(groupData.students || []).length}</strong></p>
      <div class="table-wrap">
        <table class="students-table" role="table" aria-label="Students table">
          <thead><tr><th>Roll</th><th>Name</th><th>ID</th><th>Department</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;
  } catch (err) {
    content.innerHTML = `<p class="error">Unable to load group ${groupKey}: ${escapeHtml(err.message)}</p>`;
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function attachLangButtons() {
  document.getElementById('lang-en').addEventListener('click', () => { currentLang = 'en'; updateLangUI(); });
  document.getElementById('lang-bn').addEventListener('click', () => { currentLang = 'bn'; updateLangUI(); });
  document.getElementById('lang-ar').addEventListener('click', () => { currentLang = 'ar'; updateLangUI(); });

  document.getElementById('close-panel').addEventListener('click', () => {
    const panel = document.getElementById('group-panel');
    panel.classList.add('hidden');
    panel.setAttribute('aria-hidden', 'true');
  });
}

function updateLangUI() {
  // update nav, hero, footer and department titles
  renderHeader();
  renderHero();
  renderFooter();
  renderDepartments();
}

window.addEventListener('DOMContentLoaded', loadMaster);
