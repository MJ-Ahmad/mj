/* MJ Ahmad — Splash controller (robust)
   - rAF-এর উপর নির্ভর করে না (ব্যাকগ্রাউন্ড ট্যাব/ইন-অ্যাপ ব্রাউজারে rAF থেমে যায়)
   - পেজ লোড শেষ + ন্যূনতম সময় পার হলেই শেষ হয়; সর্বোচ্চ সময়েও জোর করে শেষ হয়
   - JS ব্যর্থ হলেও CSS failsafe (site.css) ৭ সেকেন্ডে splash সরিয়ে দেয় */
(function () {
  'use strict';
  var root = document.documentElement;
  var splash = document.getElementById('splash');
  var page = document.getElementById('page');
  if (!splash || !page) return;

  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var MIN = reduce ? 400 : 1800;   /* ন্যূনতম দেখানোর সময় (ms) */
  var MAX = 4500;                  /* সর্বোচ্চ অপেক্ষা (ms) — ধীর নেটওয়ার্কেও আটকে থাকবে না */
  var t0 = Date.now();
  var finished = false;

  function setInert(on) {
    try { if (on) page.setAttribute('inert', ''); else page.removeAttribute('inert'); } catch (e) {}
  }

  function reveal() {
    page.classList.add('is-ready');
    setInert(false);
  }

  function finish() {
    if (finished) return;
    finished = true;
    splash.classList.add('is-done');
    reveal();
    setTimeout(function () { root.className += ' splash-gone'; }, 750);
  }

  function tryFinish() {
    if (finished) return;
    var elapsed = Date.now() - t0;
    if (elapsed >= MAX) return finish();
    if (document.readyState === 'complete' && elapsed >= MIN) return finish();
    /* এখনো প্রস্তুত নয় — একটু পরে আবার দেখি */
    setTimeout(tryFinish, Math.max(60, Math.min(250, MIN - elapsed)));
  }

  /* সাইটের ভেতর থেকে ফিরলে (head স্ক্রিপ্ট no-splash দিয়েছে) */
  if (/\bno-splash\b/.test(root.className)) {
    finished = true;
    reveal();
    return;
  }

  /* স্প্ল্যাশ চলাকালীন পেজের কনটেন্টে ফোকাস/স্ক্রিন-রিডার ঢুকবে না */
  setInert(true);

  /* প্রগ্রেস বার: CSS অ্যানিমেশন, সময় এখান থেকে নির্ধারিত */
  var bar = document.getElementById('progress');
  if (bar) bar.style.animationDuration = MIN + 'ms';

  /* Skip: বাটন, Escape, অথবা স্ক্রিনে ট্যাপ/ক্লিক */
  var skip = document.getElementById('skip');
  if (skip) skip.addEventListener('click', function (e) { e.stopPropagation(); finish(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') finish(); });
  splash.addEventListener('click', finish);

  window.addEventListener('load', tryFinish);
  setTimeout(tryFinish, MIN);
  setTimeout(finish, MAX + 300);   /* চূড়ান্ত নিরাপত্তা */

  /* ব্যাক-ফরওয়ার্ড ক্যাশ (bfcache) থেকে ফিরলে আটকে থাকা splash পরিষ্কার করি */
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { finished = true; splash.classList.add('is-done'); root.className += ' splash-gone'; reveal(); }
  });
})();
