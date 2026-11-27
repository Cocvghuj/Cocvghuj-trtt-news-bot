const fs = require('fs');
const path = require('path');

const root = __dirname;
const dist = path.join(root, 'dist');

// Only publish browser-facing assets. Never copy Python source, credentials/config
// files, partner records, tests, histories, or documentation.
const PUBLIC_EXTENSIONS = new Set([
  '.html', '.css', '.js', '.mjs', '.svg',
  '.png', '.jpg', '.jpeg', '.webp', '.gif', '.ico',
  '.woff', '.woff2', '.ttf', '.otf',
  '.xml', '.webmanifest'
]);
const PUBLIC_JSON_FILES = new Set([
  'affiliate-services.json',
  'manifest.json',
  'blog-control.json'
]);
const PUBLIC_TEXT_FILES = new Set([
  'robots.txt',
  'sitemap.txt'
]);
const PRIVATE_FILES = new Set(['build.js', 'roksana-vault.js', 'trtt-auto-sync.js', 'site.css']);
const PRIVATE_PATHS = new Set(['blog/index.html']);
const IGNORED_DIRECTORIES = new Set([
  '.git', '.github', 'api', 'dist', 'node_modules',
  'tests', '__pycache__', '.venv', 'venv',
  'logs', 'private', 'data'
]);

if (fs.existsSync(dist)) {
  fs.rmSync(dist, { recursive: true, force: true });
}
fs.mkdirSync(dist, { recursive: true });

function isPublicAsset(filePath) {
  const filename = path.basename(filePath).toLowerCase();
  const relativePath = path.relative(root, filePath).split(path.sep).join('/').toLowerCase();
  if (PRIVATE_FILES.has(filename) || PRIVATE_PATHS.has(relativePath)) return false;
  if (PUBLIC_JSON_FILES.has(filename) || PUBLIC_TEXT_FILES.has(filename)) return true;
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

const requiredPublicAssets = ['trtt-theme.css', 'trtt-blog-menu.js', 'trtt-voyage-menu.js', 'blog-control.json', 'assets/css/trtt-voyage-site.css', 'blog/trtt-voyage-news-hub.html'];
for (const asset of requiredPublicAssets) {
  if (!fs.existsSync(path.join(dist, asset))) {
    throw new Error('Build failed: required public Blogger asset is missing from dist: ' + asset);
  }
}

const menuConfig = JSON.parse(fs.readFileSync(path.join(dist, 'blog-control.json'), 'utf8'));
const expectedMenu = ['Home', 'News', 'Travel', 'AI', 'Tools', 'About'];
const actualMenu = Array.isArray(menuConfig.menu) ? menuConfig.menu.map(item => item.label) : [];
if (JSON.stringify(actualMenu) !== JSON.stringify(expectedMenu)) {
  throw new Error('Build failed: Blogger menu must contain exactly Home, News, Travel, AI, Tools and About in order.');
}

const builtIndex = path.join(dist, 'index.html');
if (!fs.existsSync(builtIndex)) throw new Error('Build failed: dist/index.html was not created.');
const builtHtml = fs.readFileSync(builtIndex, 'utf8');
if (!builtHtml.includes('TRTT') || !builtHtml.includes('VOYAGEHUB')) throw new Error('Build failed: TRTT VOYAGEHUB branding missing from dist/index.html.');
if (!builtHtml.includes('787950 LOCKED')) throw new Error('Build failed: marker 787950 LOCKED missing from dist/index.html.');
if (!builtHtml.includes('https://cocvghuj-trtt-news-bot.vercel.app')) throw new Error('Build failed: TRTT Live App link missing from dist/index.html.');
if (!builtHtml.includes('trtt-voyage-menu.js')) throw new Error('Build failed: TRTT Voyage navigation menu source missing from dist/index.html.');
if (builtHtml.includes('roksana-vault.js')) throw new Error('Build failed: legacy personal menu script must not be referenced by the public app.');
if (fs.existsSync(path.join(dist, 'roksana-vault.js'))) throw new Error('Build failed: legacy menu script must not be copied into the public build.');
if (fs.existsSync(path.join(dist, 'trtt-auto-sync.js'))) throw new Error('Build failed: retired auto-sync script must not be copied into the public build.');
if (fs.existsSync(path.join(dist, 'assets/css/site.css'))) throw new Error('Build failed: malformed legacy stylesheet must not be copied into the public build.');
if (fs.existsSync(path.join(dist, 'blog/index.html'))) throw new Error('Build failed: legacy blog hub must not be copied into the public build.');
if (!fs.existsSync(path.join(dist, 'blog/trtt-voyage-news-hub.html'))) throw new Error('Build failed: TRTT Voyage news hub is missing from dist.');
if (fs.existsSync(path.join(dist, 'blog.json'))) throw new Error('Build failed: legacy content snapshot must not be copied into the public build.');
const builtManifest = JSON.parse(fs.readFileSync(path.join(dist, 'manifest.json'), 'utf8'));
if (!builtManifest.name.includes('TRTT Voyage') || builtManifest.start_url !== '/' || builtManifest.theme_color !== '#11152D') throw new Error('Build failed: PWA manifest branding or start URL is incorrect.');
if (!builtHtml.includes('https://trttvoyage.com/')) throw new Error('Build failed: official TRTT Voyage website link missing.');
const builtSuperApp = fs.readFileSync(path.join(dist, 'super-app.html'), 'utf8');
if (builtSuperApp.includes('trtt-auto-sync.js') || builtSuperApp.includes('Auto-Synced Articles')) throw new Error('Build failed: retired auto-sync feed is still referenced.');
if (!builtSuperApp.includes('Some partner links may earn TRTT Voyage a commission')) throw new Error('Build failed: partner disclosure missing from Super App.');
if (builtSuperApp.includes('Verified Travel Tools') || builtSuperApp.includes('claim up to €600')) throw new Error('Build failed: unsupported travel claims remain in Super App.');
console.log('Build verified: index, Blogger CSS, menu loader, public config and marker are present in dist.');
