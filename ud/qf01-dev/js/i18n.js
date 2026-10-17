/*
 * QuranerFariwala — shared language toggle: BN | EN | AR
 *
 * Works on any page that uses:
 *   - text:         data-bn="..." data-en="..." data-ar="..."
 *   - placeholders: data-bn-placeholder / data-en-placeholder / data-ar-placeholder
 *   - buttons:      <button data-lang-button="bn|en|ar">
 *   - footer year:  <span id="footerYear"></span> (optional)
 *
 * Arabic sets <html dir="rtl">. A missing translation falls back to English.
 * The choice is stored in localStorage under "qf-lang" so every page remembers it.
 */
(function () {
  'use strict';

  // Guard against double initialisation if the script is included twice.
  if (window.qfI18n) return;

  var STORAGE_KEY = 'qf-lang';
  var DEFAULT_LANG = 'bn';
  var SUPPORTED = { bn: true, en: true, ar: true };
  var RTL_LANGS = { ar: true };

  function normalise(lang) {
    return SUPPORTED[lang] ? lang : DEFAULT_LANG;
  }

  function getStoredLang() {
    try {
      return normalise(localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG);
    } catch (e) {
      return DEFAULT_LANG;
    }
  }

  function saveLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* storage unavailable (private mode etc.) — language still applies for this page */
    }
  }

  // Read the translation for a language; fall back to English when it is missing.
  function pick(el, suffix, lang) {
    var value = el.getAttribute('data-' + lang + suffix);
    if (value === null && lang !== 'en') {
      value = el.getAttribute('data-en' + suffix);
    }
    return value;
  }

  // Replace an element's text without destroying child elements (icons, links, spans).
  function setElementText(el, text) {
    if (el.children.length === 0) {
      el.textContent = text;
      return;
    }
    for (var i = 0; i < el.childNodes.length; i++) {
      var node = el.childNodes[i];
      if (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() !== '') {
        node.nodeValue = text;
        return;
      }
    }
  }

  function applyLang(lang) {
    lang = normalise(lang);

    document.querySelectorAll('[data-en]').forEach(function (el) {
      var text = pick(el, '', lang);
      if (text !== null) setElementText(el, text);
    });

    document.querySelectorAll('[data-en-placeholder]').forEach(function (el) {
      var ph = pick(el, '-placeholder', lang);
      if (ph !== null) el.setAttribute('placeholder', ph);
    });

    var root = document.documentElement;
    root.setAttribute('lang', lang);
    root.setAttribute('dir', RTL_LANGS[lang] ? 'rtl' : 'ltr');
    root.setAttribute('data-lang', lang);

    document.querySelectorAll('[data-lang-button]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(btn.getAttribute('data-lang-button') === lang));
    });

    saveLang(lang);

    try {
      document.dispatchEvent(new CustomEvent('qf:langchange', { detail: { lang: lang } }));
    } catch (e) { /* older browsers */ }
  }

  function init() {
    applyLang(getStoredLang());

    document.querySelectorAll('[data-lang-button]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        applyLang(btn.getAttribute('data-lang-button'));
      });
    });

    var year = document.getElementById('footerYear');
    if (year) year.textContent = new Date().getFullYear();
  }

  // Works whether this script loads before or after the DOM is parsed.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.qfI18n = { setLang: applyLang, getLang: getStoredLang };
})();
