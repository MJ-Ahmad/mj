(function () {
  var ICONS = {
    gift: '<path d="M20 12v9H4v-9"/><path d="M2 7h20v5H2z"/><path d="M12 22V7"/><path d="M12 7H7.5A2.5 2.5 0 1 1 10 4.5"/><path d="M12 7h4.5A2.5 2.5 0 1 0 14 4.5"/>',
    sprout: '<path d="M7 20h10"/><path d="M10 20c0-4 2-6 2-10"/><path d="M12 10c-4 0-6-2-6-6 4 0 6 2 6 6z"/><path d="M12 10c4 0 6-3 6-7-4 0-6 3-6 7z"/>',
    handshake: '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
    research: '<path d="M4 6c0-1.1 1.3-2 4-2s4 .9 4 2v13c0-1-1.3-1.5-4-1.5S4 18 4 19V6z"/><path d="M20 6c0-1.1-1.3-2-4-2s-4 .9-4 2v13c0-1 1.3-1.5 4-1.5s4 .5 4 1.5V6z"/>',
    printing: '<path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    distribution: '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="M3.3 7 12 12l8.7-5"/><path d="M12 22V12"/>'
  };

  var lang = localStorage.getItem('qf-lang') || 'bn';
  var DATA = null;

  fetch('data.json')
    .then(function (r) { if (!r.ok) throw new Error('missing data.json'); return r.json(); })
    .then(function (data) { DATA = data; render(); })
    .catch(function (e) {
      console.error(e);
      document.getElementById('hero').innerHTML =
        '<p style="color:#7A2E2E">data.json লোড করা যায়নি। / Could not load data.json.</p>';
    });

  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; }
  function t(field) { return field[lang] || field.bn; }
  function other(field) { return lang === 'bn' ? field.en : field.bn; }

  function render() {
    var data = DATA;
    var h = data.hero;
    document.getElementById('epigraph').textContent = h.epigraph;
    document.getElementById('epigraphRef').textContent = t(h.epigraphRef);
    document.getElementById('heroTitle').textContent = t(h.title);
    document.getElementById('heroLead').textContent = t(h.lead);
    var cta = document.getElementById('heroCta');
    cta.textContent = t(h.cta);
    cta.href = h.cta.link;

    document.getElementById('ledgerStrip').innerHTML = data.ledger.map(function (l) {
      var val = lang === 'en' ? l.valueEn : l.value;
      return '<div class="ledger-item"><div class="val">' + esc(val) + '</div><div class="lbl">' + esc(t(l.label)) + '</div></div>';
    }).join('');

    document.getElementById('chaptersHeadBn').textContent = t(data.chaptersHead);

    document.getElementById('chapters').innerHTML = data.chapters.map(function (c) {
      return '<div class="chapter">' +
        '<div class="medallion"><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">' + ICONS[c.icon] + '</svg></div>' +
        '<div class="chapter-body">' +
        '<h3>' + esc(t(c.title)) + '</h3>' +
        '<span class="en">' + esc(other(c.title)) + '</span>' +
        '<p>' + esc(t(c.text)) + '</p>' +
        '<a href="' + esc(c.link) + '">' + (lang === 'en' ? 'Read more' : 'বিস্তারিত পড়ুন') + '</a>' +
        '</div></div>';
    }).join('');

    document.getElementById('supportHead').textContent = t(data.supportHead);
    document.getElementById('supportLead').textContent = t(data.supportLead);

    document.getElementById('supportGrid').innerHTML = data.ledgerEntries.map(function (e) {
      return '<div class="support-card">' +
        '<div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + ICONS[e.icon] + '</svg></div>' +
        '<h3>' + esc(t(e.title)) + '</h3>' +
        '<span class="en">' + esc(other(e.title)) + '</span>' +
        '<p>' + esc(t(e.note)) + '</p>' +
        '<a href="' + esc(e.link) + '">' + esc(t(e.title)) + ' →</a>' +
        '</div>';
    }).join('');

    var p = data.portal;
    document.getElementById('portalTitle').textContent = t(p.title);
    document.getElementById('portalTitleEn').textContent = other(p.title);
    document.getElementById('portalDesc').textContent = t(p.desc);
    var pcta = document.getElementById('portalCta');
    pcta.textContent = t(p.cta);
    pcta.href = p.cta.link;

    var f = data.footer;
    document.getElementById('footerCols').innerHTML = f.columns.map(function (col) {
      var items = col.links.map(function (l) {
        var soon = l.soon ? '<span class="badge-soon">' + esc(t(f.soonLabel)) + '</span>' : '';
        return '<li><a href="' + esc(l.link) + '">' + esc(t(l.label)) + soon + '</a></li>';
      }).join('');
      return '<div class="footer-col"><h4>' + esc(t(col.heading)) + '</h4><ul>' + items + '</ul></div>';
    }).join('');

    document.getElementById('footerNote').textContent = t(f.note);
    document.getElementById('footerCredit').innerHTML =
      '<a href="' + esc(f.creditLink) + '">' + esc(f.credit) + '</a>';
    document.getElementById('footerLegal').innerHTML = f.legal.map(function (l) {
      return '<a href="' + esc(l.link) + '">' + esc(t(l.label)) + '</a>';
    }).join('');

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var val = lang === 'en' ? el.dataset.i18nEn : el.dataset.i18nBn;
      if (val) el.textContent = val;
    });

    document.documentElement.lang = lang === 'en' ? 'en' : 'bn';
    document.getElementById('langBn').classList.toggle('active', lang === 'bn');
    document.getElementById('langEn').classList.toggle('active', lang === 'en');
    document.getElementById('langBn').setAttribute('aria-pressed', lang === 'bn');
    document.getElementById('langEn').setAttribute('aria-pressed', lang === 'en');
  }

  function applyLang(newLang) {
    lang = newLang;
    localStorage.setItem('qf-lang', lang);
    if (DATA) render();
  }

  document.getElementById('langBn').addEventListener('click', function () { applyLang('bn'); });
  document.getElementById('langEn').addEventListener('click', function () { applyLang('en'); });

  var toggleBtn = document.getElementById('navToggle');
  var navEl = document.getElementById('mainNav');
  toggleBtn.addEventListener('click', function () {
    var open = navEl.classList.toggle('open');
    toggleBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();
