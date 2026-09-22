const DASHBOARD_PASSWORD = '23542';
const loginShell = document.getElementById('loginShell');
const dashboardShell = document.getElementById('dashboardShell');
const loginForm = document.getElementById('loginForm');
const passwordInput = document.getElementById('password');
const loginError = document.getElementById('loginError');
const logoutBtn = document.getElementById('logoutBtn');
const liveClock = document.getElementById('liveClock');

const taskBoard = [
  { title: 'Governance audit', detail: 'Completed — oversight baseline signed off', state: 'done' },
  { title: 'Public launch preparation', detail: 'In progress — partnerships, messaging, and URL readiness', state: 'active' },
  { title: 'Partner pipeline', detail: 'Pending — outreach and institutional alignment', state: 'pending' },
  { title: 'Executive reporting cadence', detail: 'Next brief due in 3 days', state: 'active' }
];

const contacts = [
  { name: 'MJ Ahmad', role: 'Principal / Controller', email: 'mj@mjsovereign.org', phone: '+88 01700-000000' },
  { name: 'Executive Office', role: 'Leadership Coordination', email: 'office@mjsovereign.org', phone: '+88 01600-000000' },
  { name: 'Operations Desk', role: 'Delivery & Oversight', email: 'ops@mjsovereign.org', phone: '+88 01800-000000' },
  { name: 'Partner Network', role: 'Institutional Links', email: 'partners@mjsovereign.org', phone: '+88 01900-000000' },
  { name: 'Communications', role: 'Messaging & Public Trust', email: 'media@mjsovereign.org', phone: '+88 01500-000000' },
  { name: 'Finance & Compliance', role: 'Budget & Governance', email: 'finance@mjsovereign.org', phone: '+88 01750-000000' }
];

function renderTaskBoard() {
  const taskContainer = document.getElementById('taskBoard');
  if (!taskContainer) return;

  taskContainer.innerHTML = taskBoard
    .map(
      (task) => `
        <div class="task-item">
          <span class="status-dot ${task.state}"></span>
          <div>
            <strong>${task.title}</strong>
            <small>${task.detail}</small>
          </div>
        </div>
      `
    )
    .join('');
}

function renderContacts() {
  const contactContainer = document.getElementById('contactDirectory');
  if (!contactContainer) return;

  contactContainer.innerHTML = contacts
    .map(
      (contact) => `
        <article class="contact-card">
          <span>${contact.role}</span>
          <strong>${contact.name}</strong>
          <a href="mailto:${contact.email}">${contact.email}</a>
          <small>${contact.phone}</small>
        </article>
      `
    )
    .join('');
}

function updateClock() {
  if (!liveClock) return;

  const now = new Date();
  liveClock.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function unlockDashboard() {
  loginShell.classList.add('hidden');
  dashboardShell.classList.remove('hidden');
  passwordInput.value = '';
  loginError.textContent = '';
  updateClock();
}

function lockDashboard() {
  dashboardShell.classList.add('hidden');
  loginShell.classList.remove('hidden');
  passwordInput.value = '';
  loginError.textContent = '';
  passwordInput.focus();
}

loginForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const enteredPassword = passwordInput.value.trim();

  if (enteredPassword === DASHBOARD_PASSWORD) {
    unlockDashboard();
    return;
  }

  loginError.textContent = 'Incorrect password. Please try again.';
  passwordInput.focus();
});

logoutBtn.addEventListener('click', lockDashboard);
passwordInput.focus();
renderTaskBoard();
renderContacts();
updateClock();
setInterval(updateClock, 60000);
