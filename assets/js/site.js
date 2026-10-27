/* MJ Ahmad — shared behaviour: theme, language, Dhaka clock, last-updated */
(function () {
  var root = document.documentElement;
  var listeners = [];
  var LANGS = ['bn', 'en', 'ar'];
  var LOCALES = { bn: 'bn-BD', en: 'en-GB', ar: 'ar' };
  var ZONE = { bn: 'ঢাকা, UTC+06:00', en: 'Dhaka, UTC+06:00', ar: 'دكا، UTC+06:00' };
  var TZ = 'Asia/Dhaka';

  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* ---------- Theme: follows the system until the visitor chooses ---------- */
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return !(window.matchMedia && matchMedia('(prefers-color-scheme: light)').matches);
  }
  function toggleTheme() {
    var next = isDark() ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    set('mj-theme', next);
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', next === 'dark' ? '#0f1216' : '#f6f3ec');
  }

  /* ---------- Dhaka time helpers ---------- */
  var fmtCache = {};
  function fmts(lang) {
    if (fmtCache[lang]) return fmtCache[lang];
    var loc = LOCALES[lang], f;
    try {
      f = {
        date: new Intl.DateTimeFormat(loc, { timeZone: TZ, day: 'numeric', month: 'long', year: 'numeric' }),
        time: new Intl.DateTimeFormat(loc, { timeZone: TZ, hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23' })
      };
    } catch (e) { f = null; }
    return (fmtCache[lang] = f);
  }
  function timeText(d, lang) {
    var f = fmts(lang);
    if (!f) { var p = new Date(d.getTime() + 6 * 3600e3).toISOString(); return p.slice(11, 19); }
    return f.time.format(d);
  }
  function dateTimeText(d, lang) {
    var f = fmts(lang);
    if (!f) return new Date(d.getTime() + 6 * 3600e3).toISOString().replace('T', ' ').slice(0, 19);
    return f.date.format(d) + ' · ' + f.time.format(d);
  }

  /* Last updated: the server's Last-Modified header when available (i.e. the real
     deployment time on the live site); otherwise the value written in the page. */
  var lastMod = null;
  function paintUpdated() {
    var lang = root.lang;
    document.querySelectorAll('[data-updated]').forEach(function (el) {
      var d = lastMod || new Date(el.getAttribute('data-updated'));
      if (isNaN(d)) return;
      el.setAttribute('datetime', d.toISOString());
      el.textContent = dateTimeText(d, lang) + ' (' + ZONE[lang] + ')';
    });
  }
  function fetchLastModified() {
    var el = document.querySelector('[data-lm-url]');
    if (!el || !window.fetch || location.protocol === 'file:') return;
    fetch(el.getAttribute('data-lm-url'), { method: 'HEAD', cache: 'no-store' })
      .then(function (r) {
        var h = r.ok && r.headers.get('last-modified');
        var d = h ? new Date(h) : null;
        if (d && !isNaN(d)) { lastMod = d; paintUpdated(); }
      })
      .catch(function () {});
  }

  function paintClock() {
    var els = document.querySelectorAll('[data-clock]');
    if (!els.length) return;
    var lang = root.lang, now = new Date(), txt = timeText(now, lang) + ' (' + ZONE[lang] + ')';
    els.forEach(function (el) { el.textContent = txt; });
  }

  /* ---------- Language ---------- */
  function setLang(lang) {
    if (LANGS.indexOf(lang) < 0) lang = 'bn';
    root.lang = lang;
    root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-' + lang + ']').forEach(function (el) {
      el.textContent = el.getAttribute('data-' + lang);
    });
    document.querySelectorAll('[data-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang));
    });
    var t = root.getAttribute('data-title-' + lang);
    if (t) document.title = t;
    paintUpdated();
    paintClock();
    set('mj-lang', lang);
    listeners.forEach(function (fn) { fn(lang); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-lang]').forEach(function (b) {
      b.addEventListener('click', function () { setLang(b.getAttribute('data-lang')); });
    });
    document.querySelectorAll('.theme-btn').forEach(function (b) { b.addEventListener('click', toggleTheme); });
    document.querySelectorAll('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });
    var top = document.getElementById('top');
    if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    var saved = get('mj-lang');
    setLang(LANGS.indexOf(saved) >= 0 ? saved : 'bn');

    fetchLastModified();
    setInterval(fetchLastModified, 10 * 60 * 1000);
    (function tick() { paintClock(); setTimeout(tick, 1000 - (Date.now() % 1000) + 5); })();
  });

  window.MJ = {
    onLang: function (fn) { listeners.push(fn); },
    get lang() { return root.lang; }
  };
})();
