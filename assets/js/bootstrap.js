/* ==========================================================================
   MJ — bootstrap.js (Data Loader + Renderer)
   index.html-এর সব কনটেন্ট mj-data.json থেকে লোড ও রেন্ডার করে।
   কনটেন্ট বদলাতে শুধু mj-data.json সম্পাদনা করুন — এই ফাইলে হাত দিতে হবে না।
   ========================================================================== */
(function () {
  'use strict';

  var DATA_URL = 'mj-data.json';
  var RTL_LANGS = { ar: true };
  var state = { data: null, lang: 'bn' };

  /* ---------------- helpers ---------------- */
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }
  function node(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) tr(e, text);
    return e;
  }
  /* ত্রিভাষিক টেক্সট: data-bn/en/ar বসায় — পরে setLang() আবার প্রয়োগ করে */
  function tr(e, t) {
    if (!t) return e;
    var bn = t.bn || '';
    e.setAttribute('data-bn', bn);
    e.setAttribute('data-en', t.en || bn);
    e.setAttribute('data-ar', t.ar || bn);
    e.textContent = t[state.lang] || bn;
    return e;
  }
  function pick(t) { return typeof t === 'string' ? t : (t[state.lang] || t.bn || ''); }

  /* ---------------- icons (UI-এর অংশ, ডাটা নয়) ---------------- */
  var ICONS = {
    pin: '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
    github: '<svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor" aria-hidden="true"><path d="M12 .5a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.8.1-.8.1-.8 1.2.1 1.9 1.3 1.9 1.3 1.1 1.9 2.9 1.3 3.6 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.3.5-2.4 1.3-3.2-.1-.3-.6-1.6.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.7 1.6.2 2.9.1 3.2.8.8 1.3 1.9 1.3 3.2 0 4.6-2.8 5.7-5.5 6 .4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .5z"/></svg>',
    linkedin: '<svg viewBox="0 0 24 24" width="36" height="36" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    shield: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 4.5 6v5.5c0 4.6 3.1 8.2 7.5 9.5 4.4-1.3 7.5-4.9 7.5-9.5V6z"/><path d="m9 12 2.2 2.2L15.5 10"/></svg>',
    cap: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m2.5 9.5 9.5-5 9.5 5-9.5 5z"/><path d="M6.5 12v4.5c1.5 1.3 3.5 2 5.5 2s4-.7 5.5-2V12M21.5 9.5V15"/></svg>',
    heart: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20.5s-7.5-4.4-7.5-10a4.3 4.3 0 0 1 7.5-2.8 4.3 4.3 0 0 1 7.5 2.8c0 5.6-7.5 10-7.5 10z"/></svg>',
    arrow: '<svg class="flip" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    sun: '<svg class="sun" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    moon: '<svg class="moon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>'
  };

  /* ---------------- renderers ---------------- */
  function renderHero(h) {
    var sec = node('section', 'hero');
    var c = node('div', 'container');

    if (h.portrait) {
      var pw = node('div', 'portrait-wrap');
      var img = node('img', 'portrait');
      img.src = h.portrait.src; img.alt = h.portrait.alt || '';
      img.width = h.portrait.width || 190; img.height = h.portrait.height || 190;
      pw.appendChild(img); c.appendChild(pw);
    }

    c.appendChild(tr(node('h1'), h.name));

    var loc = node('p', 'location');
    loc.insertAdjacentHTML('beforeend', ICONS.pin);
    loc.appendChild(tr(node('span'), h.location));
    c.appendChild(loc);

    var links = node('div', 'hero-links');
    (h.social || []).forEach(function (s) {
      var a = node('a', s.className || null);
      a.href = s.url; a.target = '_blank'; a.rel = 'noopener noreferrer';
      var label = pick(s.label);
      a.title = label; a.setAttribute('aria-label', label);
      if (s.icon) a.innerHTML = ICONS[s.icon] || '';
      else if (s.image) {
        var im = node('img');
        im.src = s.image; im.alt = '';
        im.width = s.width || 32; im.height = s.height || 32;
        a.appendChild(im);
      }
      links.appendChild(a);
    });
    c.appendChild(links);

    var controls = node('div', 'hero-controls');
    var bar = node('div', 'langbar');
    bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'Language');
    [['en', 'EN'], ['bn', 'বাংলা'], ['ar', 'AR']].forEach(function (pair) {
      var b = node('button'); b.type = 'button';
      b.setAttribute('data-lang', pair[0]);
      b.setAttribute('aria-pressed', pair[0] === state.lang ? 'true' : 'false');
      b.textContent = pair[1];
      bar.appendChild(b);
    });
    controls.appendChild(bar);

    var themeBtn = node('button', 'icon-btn theme-btn');
    themeBtn.type = 'button'; themeBtn.id = 'theme-toggle';
    themeBtn.setAttribute('aria-label', 'Theme'); themeBtn.title = 'Light / Dark';
    themeBtn.innerHTML = ICONS.sun + ICONS.moon;
    controls.appendChild(themeBtn);
    c.appendChild(controls);

    if (h.intro && h.intro.segments) {
      var intro = node('div', 'intro');
      var p = node('p');
      h.intro.segments.forEach(function (seg) {
        if (seg.type === 'link') {
          var a = node('a');
          a.href = seg.url; a.target = '_blank'; a.rel = 'noopener';
          a.appendChild(tr(node('span'), seg.text));
          p.appendChild(a);
        } else {
          p.appendChild(tr(node('span'), seg.text));
        }
      });
      intro.appendChild(p); c.appendChild(intro);
    }

    sec.appendChild(c);
    return sec;
  }

  function renderPillars(pl) {
    var sec = node('section', 'section tint');
    var c = node('div', 'container');
    c.appendChild(tr(node('p', 'lead-in'), pl.lead));
    var wrap = node('div', 'pillars');
    (pl.items || []).forEach(function (it) {
      var d = node('div', 'pillar');
      var ico = node('span', 'ico');
      ico.innerHTML = ICONS[it.icon] || '';
      d.appendChild(ico);
      d.appendChild(tr(node('p'), it.text));
      wrap.appendChild(d);
    });
    c.appendChild(wrap);
    c.appendChild(tr(node('p', 'statement'), pl.statement));
    sec.appendChild(c);
    return sec;
  }

  function renderProjects(pr) {
    var sec = node('section', 'section');
    var c = node('div', 'container');
    c.appendChild(tr(node('p', 'kicker'), pr.kicker));
    (pr.items || []).forEach(function (it, i) {
      var card = node('div', 'project-card');
      if (i > 0) card.style.marginTop = '2.4rem';

      var img = node('img', 'project-logo');
      img.src = it.logo; img.alt = it.logoAlt || '';
      img.width = it.logoWidth || 168; img.height = it.logoHeight || 168;
      card.appendChild(img);

      var txt = node('div', 'project-text');
      txt.appendChild(tr(node('h3'), it.title));
      if (it.status) txt.appendChild(tr(node('p', 'badge'), it.status));
      txt.appendChild(tr(node('p'), it.desc));

      if (it.cta) {
        var cp = node('p'); cp.style.marginTop = '1.3rem';
        var a = node('a', 'btn');
        a.href = it.cta.url;
        if (it.cta.external) { a.target = '_blank'; a.rel = 'noopener'; }
        a.appendChild(tr(node('span'), it.cta.text));
        a.insertAdjacentHTML('beforeend', ICONS.arrow);
        cp.appendChild(a); txt.appendChild(cp);
      }
      card.appendChild(txt);
      c.appendChild(card);
    });
    sec.appendChild(c);
    return sec;
  }

  function renderFooter(f) {
    var foot = node('footer', 'site-footer');
    var wide = node('div', 'wide');

    var nav = node('nav', 'footer-links');
    nav.setAttribute('aria-label', 'Footer');
    (f.links || []).forEach(function (l) {
      var a = node('a'); a.href = l.url; tr(a, l.text);
      nav.appendChild(a);
    });
    wide.appendChild(nav);

    var bottom = node('div', 'footer-bottom');
    var span = node('span');
    span.appendChild(document.createTextNode('© '));
    var yr = node('span');
    yr.setAttribute('data-year', '');
    yr.textContent = String(new Date().getFullYear());
    span.appendChild(yr);
    span.appendChild(document.createTextNode(' MJ Ahmad. '));
    span.appendChild(tr(node('span'), f.rights));
    bottom.appendChild(span);

    var top = tr(node('button', 'back-top'), f.backToTop);
    top.type = 'button'; top.id = 'top';
    bottom.appendChild(top);
    wide.appendChild(bottom);

    var time = node('div', 'footer-time');
    var s1 = node('span');
    s1.appendChild(tr(node('span'), f.lastUpdatedLabel));
    s1.appendChild(document.createTextNode(' '));
    var t1 = node('time');
    if (f.lastUpdated) t1.setAttribute('data-updated', f.lastUpdated);
    s1.appendChild(t1);
    var s2 = node('span');
    s2.appendChild(tr(node('span'), f.clockLabel));
    s2.appendChild(document.createTextNode(' '));
    var t2 = node('time'); t2.setAttribute('data-clock', '');
    s2.appendChild(t2);
    time.appendChild(s1); time.appendChild(s2);
    wide.appendChild(time);

    foot.appendChild(wide);
    return foot;
  }

  /* ---------------- ভাষা ---------------- */
  function setLang(lang) {
    state.lang = lang;
    var root = document.documentElement;
    root.setAttribute('lang', lang);
    root.setAttribute('dir', RTL_LANGS[lang] ? 'rtl' : 'ltr');
    try { localStorage.setItem('mj-lang', lang); } catch (e) {}

    $all('[data-bn]').forEach(function (el) {
      el.textContent = el.getAttribute('data-' + lang) || el.getAttribute('data-bn') || '';
    });
    $all('[data-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-lang') === lang ? 'true' : 'false');
    });

    var d = state.data;
    if (d && d.meta) {
      var t = d.meta.title || {};
      if (t[lang] || t.bn) document.title = t[lang] || t.bn;
      var md = document.querySelector('meta[name="description"]');
      var desc = (d.meta.description || {})[lang] || (d.meta.description || {}).bn;
      if (md && desc) md.setAttribute('content', desc);
    }
    initDates();
  }

  /* ---------------- থিম ---------------- */
  function initTheme() {
    document.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('#theme-toggle');
      if (!b) return;
      var root = document.documentElement;
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('mj-theme', next); } catch (err) {}
    });
  }

  /* ---------------- ভাষা বার ---------------- */
  function initLangbar() {
    document.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('[data-lang]');
      if (b) setLang(b.getAttribute('data-lang'));
    });
  }

  /* ---------------- উপরে ফিরুন ---------------- */
  function initBackTop() {
    document.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('#top')) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  }

  /* ---------------- তারিখ ও ঘড়ি ---------------- */
  function localeFor() {
    return state.lang === 'bn' ? 'bn-BD' : state.lang === 'ar' ? 'ar' : 'en-GB';
  }
  function initDates() {
    var u = $('[data-updated]');
    if (u) {
      var iso = u.getAttribute('data-updated');
      var d = new Date(iso);
      if (!isNaN(d)) {
        try {
          u.textContent = new Intl.DateTimeFormat(localeFor(), {
            dateStyle: 'medium', timeStyle: 'short', timeZone: 'Asia/Dhaka'
          }).format(d);
        } catch (e) { u.textContent = d.toLocaleString(); }
        u.setAttribute('datetime', iso);
      }
    }
  }
  function initClock() {
    var elc = $('[data-clock]');
    if (!elc) return;
    function tick() {
      try {
        elc.textContent = new Intl.DateTimeFormat(localeFor(), {
          timeZone: 'Asia/Dhaka', hour: '2-digit', minute: '2-digit', second: '2-digit'
        }).format(new Date());
      } catch (e) { elc.textContent = new Date().toLocaleTimeString(); }
    }
    tick();
    setInterval(tick, 1000);
  }

  /* ---------------- Splash ---------------- */
  function initSplash() {
    var sp = $('#splash');
    if (!sp) return;
    if (document.documentElement.className.indexOf('no-splash') !== -1) {
      sp.parentNode.removeChild(sp);
      return;
    }
    var progress = $('#progress');
    var skip = $('#skip');
    var done = false;
    function hide() {
      if (done) return; done = true;
      sp.style.transition = 'opacity .5s ease';
      sp.style.opacity = '0';
      setTimeout(function () { if (sp.parentNode) sp.parentNode.removeChild(sp); }, 550);
    }
    if (skip) skip.addEventListener('click', hide);
    var pct = 0;
    var iv = setInterval(function () {
      pct = Math.min(100, pct + 8 + Math.random() * 14);
      if (progress) progress.style.width = pct + '%';
      if (pct >= 100) { clearInterval(iv); setTimeout(hide, 250); }
    }, 160);
    setTimeout(hide, 6000); /* safety */
  }
  function syncSplashText(d) {
    if (!d.splash) return;
    var n = $('.splash-name'), t = $('.splash-tag'), s = $('#skip'), img = $('.splash-logo');
    if (n) tr(n, d.splash.name);
    if (t) tr(t, d.splash.tagline);
    if (s) tr(s, d.splash.skip);
    if (img && d.splash.logo) {
      img.src = d.splash.logo;
      if (d.splash.logoAlt) img.alt = d.splash.logoAlt;
    }
  }

  /* ---------------- ডাটা লোড ---------------- */
  function loadData() {
    function fromInline() {
      if (window.MJ_DATA) return Promise.resolve(window.MJ_DATA);
      return Promise.reject(new Error('no-data'));
    }
    if (!window.fetch) return fromInline();
    return fetch(DATA_URL, { cache: 'no-cache' })
      .then(function (r) {
        if (!r.ok) throw new Error('http-' + r.status);
        return r.json();
      })
      .catch(fromInline);
  }

  function applyMeta(d) {
    var root = document.documentElement;
    var t = (d.meta && d.meta.title) || {};
    ['bn', 'en', 'ar'].forEach(function (l) {
      if (t[l]) root.setAttribute('data-title-' + l, t[l]);
    });
  }

  function showError() {
    var page = $('#page');
    page.removeAttribute('aria-busy');
    page.innerHTML =
      '<main><section class="section"><div class="container">' +
      '<p style="text-align:center;padding:3rem 1rem">' +
      'ডাটা লোড করা যায়নি। <code>mj-data.json</code> ফাইলটি সঠিক জায়গায় আছে কিনা দেখুন।<br>' +
      'লোকালে চালাতে <code>python3 -m http.server</code> ব্যবহার করুন, অথবা <code>./bootstrap.sh</code> চালিয়ে inline fallback তৈরি করুন।<br>' +
      '<span lang="en">Could not load mj-data.json.</span>' +
      '</p></div></section></main>';
  }

  /* ---------------- boot ---------------- */
  function boot() {
    try {
      var l = localStorage.getItem('mj-lang');
      if (l === 'bn' || l === 'en' || l === 'ar') state.lang = l;
    } catch (e) {}

    initTheme(); initLangbar(); initBackTop(); initSplash();

    loadData().then(function (d) {
      state.data = d;
      var page = $('#page');
      page.innerHTML = '';

      var main = node('main');
      if (d.hero) main.appendChild(renderHero(d.hero));
      if (d.pillars) main.appendChild(renderPillars(d.pillars));
      if (d.projects) main.appendChild(renderProjects(d.projects));
      page.appendChild(main);
      if (d.footer) page.appendChild(renderFooter(d.footer));

      page.removeAttribute('aria-busy');
      syncSplashText(d);
      applyMeta(d);
      setLang(state.lang);
      initClock();
    }).catch(showError);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
