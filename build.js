const fs = require('fs');
const path = require('path');

const root = __dirname;
const dist = path.join(root, 'dist');

// Only publish browser-facing assets. Never copy Python source, credentials/config
// files, partner records, tests, package metadata, histories, or documentation.
const PUBLIC_EXTENSIONS = new Set([
  '.html', '.css', '.js', '.mjs', '.svg',
  '.png', '.jpg', '.jpeg', '.webp', '.gif', '.ico',
  '.woff', '.woff2', '.ttf', '.otf',
  '.xml', '.webmanifest'
]);
const PUBLIC_JSON_FILES = new Set([
  'affiliate-services.json',
  'manifest.json'
]);
const PUBLIC_TEXT_FILES = new Set([
  'robots.txt',
  'sitemap.txt'
]);
const IGNORED_DIRECTORIES = new Set([
  '.git', '.github', 'dist', 'node_modules',
  'tests', '__pycache__', '.venv', 'venv',
  'logs', 'private', 'data'
]);

if (fs.existsSync(dist)) {
  fs.rmSync(dist, { recursive: true, force: true });
}
fs.mkdirSync(dist, { recursive: true });

function isPublicAsset(filePath) {
  const filename = path.basename(filePath).toLowerCase();
  if (PUBLIC_JSON_FILES.has(filename) || PUBLIC_TEXT_FILES.has(filename)) {
    return true;
  }
  return PUBLIC_EXTENSIONS.has(path.extname(filename));
}

function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    const directoryName = path.basename(src).toLowerCase();
    if (IGNORED_DIRECTORIES.has(directoryName)) return;
    if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
    fs.readdirSync(src).forEach(child => {
      copyRecursive(path.join(src, child), path.join(dest, child));
    });
    return;
  }

  if (!isPublicAsset(src)) return;
  const parent = path.dirname(dest);
  if (!fs.existsSync(parent)) fs.mkdirSync(parent, { recursive: true });
  fs.copyFileSync(src, dest);
}

fs.readdirSync(root).forEach(file => {
  if (IGNORED_DIRECTORIES.has(file.toLowerCase())) return;
  copyRecursive(path.join(root, file), path.join(dist, file));
});

console.log('Build complete: browser-facing assets copied to dist/ only.');
