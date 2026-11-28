'use strict';
const fs = require('node:fs');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'dist-pages');
const repo = process.env.GITHUB_REPOSITORY || 'TRTT-VOYAGE/Cocvghuj-trtt-news-bot';
const [owner, repository] = repo.split('/');
if (!owner || !repository) throw new Error('GITHUB_REPOSITORY must be owner/name.');
const BASE_PATH = '/' + repository + '/';
const BASE_URL = 'https://' + owner.toLowerCase() + '.github.io' + BASE_PATH;

// Explicit public allowlist: never publish arbitrary root HTML, admin pages, diaries or vault files.
const ROOT_FILES = [
  'index.html', 'about.html', 'app.html', 'contact.html', 'disclaimer.html',
  'privacy.html', 'terms.html', 'travel-guide.html', 'latest_travel_news.html',
  'flightscoutpro-itinerary.html', 'super-app.html', 'manifest.json', 'sw.js',
  'trtt-hub.css', 'trtt-voyage-menu.js', 'trtt-voyage-logo.svg'
];
const DIRECTORY_RULES = [
  ['assets/css', /^trtt-voyage-site\.css$/i],
  ['news', /\.html$/i],
  ['news/images', /\.(?:svg|png|jpe?g|webp|gif|ico)$/i],
  ['destinations', /\.html$/i],
  ['tools', /\.html$/i],
  ['trtt-shop', /\.html$/i],
  ['blog', /^(?!index\.html$).+\.html$/i]
];
const BLOCKED_OUTPUT = /(?:^|\/)(?:diamond-king|trttmagic|trtt-control|blogger-vault|oshudh-routine|diary|backups|private|credentials?|tokens?)(?:[-./]|$)/i;
const PUBLIC_EXT = new Set(['.html', '.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.ico', '.xml', '.json', '.webmanifest']);

function copyFile(relative) {
  const src = path.join(ROOT, relative);
  const dest = path.join(OUT, relative);
  if (!fs.existsSync(src) || !fs.statSync(src).isFile()) throw new Error('Required public source is missing: ' + relative);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}
function copyDirectory(relative, matcher) {
  const src = path.join(ROOT, relative);
  if (!fs.existsSync(src)) throw new Error('Required public directory is missing: ' + relative);
  function walk(current, prefix) {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const rel = prefix + '/' + entry.name;
      if (BLOCKED_OUTPUT.test(rel)) continue;
      if (entry.isDirectory()) {
        walk(path.join(current, entry.name), rel);
      } else if (entry.isFile() && matcher.test(entry.name)) {
        copyFile(rel);
      }
    }
  }
  walk(src, relative);
}
function rewriteHtml(text) {
  text = text.replace(/\b(href|src|action|poster)=("|')\/(?!\/)/gi,
    (_, attr, quote) => attr + '=' + quote + BASE_PATH);
  text = text.replace(/https:\/\/cocvghuj-trtt-news-bot\.vercel\.app\//gi, BASE_URL);
  text = text.replace(/https:\/\/cocvghuj\.github\.io\/Cocvghuj-trtt-news-bot\//gi, BASE_URL);
  text = text.replace(/\/trtt-original-logo\.jpeg/gi, BASE_PATH + 'trtt-voyage-logo.svg');
  return text;
}
function rewriteCss(text) {
  return text.replace(/url\((\s*["']?)\/(?!\/)/gi, (_, prefix) => 'url(' + prefix + BASE_PATH);
}
function rewriteJs(text) {
  return text.replace(/(["'`])\/(?!\/)([^"'`\r\n]*)\1/g,
    (_, quote, rest) => quote + BASE_PATH + rest + quote);
}
function writePublicText(relative) {
  const file = path.join(OUT, relative);
  const ext = path.extname(file).toLowerCase();
  let text = fs.readFileSync(file, 'utf8');
  if (ext === '.html') text = rewriteHtml(text);
  else if (ext === '.css') text = rewriteCss(text);
  else if (ext === '.js') text = rewriteJs(text);
  else if (path.basename(file) === 'manifest.json') {
    const manifest = JSON.parse(text);
    manifest.start_url = BASE_PATH;
    manifest.scope = BASE_PATH;
    manifest.icons = (manifest.icons || []).map(icon => ({
      ...icon, src: icon.src && icon.src.startsWith('/') ? BASE_PATH + icon.src.slice(1) : icon.src
    }));
    text = JSON.stringify(manifest, null, 2) + '\n';
  }
  fs.writeFileSync(file, text, 'utf8');
}
function listFiles(dir, prefix = '') {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    const full = path.join(dir, entry.name);
    const rel = path.posix.join(prefix, entry.name);
    return entry.isDirectory() ? listFiles(full, rel) : [rel];
  });
}
function validateLocalLinks(files) {
  const attr = /\b(?:href|src|action|poster)=["']([^"']+)["']/gi;
  const errors = [];
  for (const rel of files.filter(x => x.endsWith('.html'))) {
    const html = fs.readFileSync(path.join(OUT, rel), 'utf8');
    let match;
    while ((match = attr.exec(html))) {
      const value = match[1];
      if (!value.startsWith(BASE_PATH)) continue;
      const clean = decodeURIComponent(value.slice(BASE_PATH.length).split(/[?#]/)[0]);
      let target = path.join(OUT, clean);
      if (value.endsWith('/') || !path.extname(clean)) target = path.join(target, 'index.html');
      if (!fs.existsSync(target)) errors.push(rel + ' -> ' + value);
    }
  }
  if (errors.length) throw new Error('Broken local links:\n' + errors.slice(0, 30).join('\n'));
}
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
for (const file of ROOT_FILES) copyFile(file);
for (const [dir, matcher] of DIRECTORY_RULES) copyDirectory(dir, matcher);
for (const rel of listFiles(OUT)) {
  if (BLOCKED_OUTPUT.test(rel)) throw new Error('Blocked private path in output: ' + rel);
  if (!PUBLIC_EXT.has(path.extname(rel).toLowerCase())) throw new Error('Unexpected public file type: ' + rel);
  if (/\.(?:html|css|js|json|webmanifest)$/i.test(rel)) writePublicText(rel);
}
const htmlFiles = listFiles(OUT).filter(file => file.endsWith('.html')).sort();
const urls = [BASE_URL, ...htmlFiles.map(file => BASE_URL + file)];
const today = new Date().toISOString().slice(0, 10);
const xml = '<?xml version="1.0" encoding="UTF-8"?>\n' +
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  urls.map(url => '  <url><loc>' + url.replace(/&/g, '&amp;') + '</loc><lastmod>' + today + '</lastmod></url>').join('\n') +
  '\n</urlset>\n';
fs.writeFileSync(path.join(OUT, 'sitemap.xml'), xml, 'utf8');
fs.writeFileSync(path.join(OUT, 'robots.txt'), 'User-agent: *\nAllow: /\nSitemap: ' + BASE_URL + 'sitemap.xml\n', 'utf8');
const files = listFiles(OUT);
for (const required of ['index.html', 'manifest.json', 'sw.js', 'robots.txt', 'sitemap.xml', 'trtt-hub.css', 'trtt-voyage-logo.svg']) {
  if (!files.includes(required)) throw new Error('Required output missing: ' + required);
}
const index = fs.readFileSync(path.join(OUT, 'index.html'), 'utf8');
if (!index.includes('TRTT Voyage') || !index.includes('787950 LOCKED')) throw new Error('Brand or marker validation failed.');
if (files.some(file => BLOCKED_OUTPUT.test(file))) throw new Error('Private/admin path detected in public output.');
validateLocalLinks(files);
console.log('PASS: GitHub Pages static artifact built.');
console.log('Base URL: ' + BASE_URL);
console.log('Files: ' + files.length);
console.log('Private/admin/vault/diary files: excluded by explicit allowlist.');
console.log('Local HTML links: validated.');
