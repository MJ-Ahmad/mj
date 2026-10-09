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
  return s.replace(/<\/??WebsiteContent_[^>]*>/g, '')
          .replace(/\s+/g, ' ')
          .trim();
}

function sanitizeUrl(rawUrl) {
  if (!rawUrl || typeof rawUrl !== 'string') return null;
  let u = stripWebsiteContentTags(rawUrl);
  u = u.trim();
  if (!/^https?:\/\//i.test(u)) return null;
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
