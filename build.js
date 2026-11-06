const fs = require('fs');
const path = require('path');

const root = __dirname;
const dist = path.join(root, 'dist');

// Fail closed on every Vercel Production build unless the owner explicitly
// opts in through a Production-only environment variable. Preview and CI builds
// remain available; this guard does not deploy or change Vercel settings.
if (
  process.env.VERCEL_ENV === 'production' &&
  process.env.TRTT_PRODUCTION_DEPLOY_APPROVED !== 'true'
) {
  console.error(
    'TRTT Production Lock: deployment blocked. Explicit owner approval is required via ' +
    'TRTT_PRODUCTION_DEPLOY_APPROVED=true in the Vercel Production environment.'
  );
  process.exit(1);
}

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
const PRIVATE_FILES = new Set(['build.js']);
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
  if (PRIVATE_FILES.has(filename)) return false;
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

const builtIndex = path.join(dist, 'index.html');
if (!fs.existsSync(builtIndex)) throw new Error('Build failed: dist/index.html was not created.');
const builtHtml = fs.readFileSync(builtIndex, 'utf8');
if (!builtHtml.includes('TRTT') || !builtHtml.includes('VOYAGEHUB')) throw new Error('Build failed: TRTT VOYAGEHUB branding missing from dist/index.html.');
if (!builtHtml.includes('787950 LOCKED')) throw new Error('Build failed: marker 787950 LOCKED missing from dist/index.html.');
if (!builtHtml.includes('https://cocvghuj-trtt-news-bot.vercel.app')) throw new Error('Build failed: TRTT Live App link missing from dist/index.html.');
if (!builtHtml.includes('roksana-vault.js')) throw new Error('Build failed: 787950 bottom menu source missing from dist/index.html.');

const builtVault = fs.readFileSync(path.join(dist, 'roksana-vault.js'), 'utf8');
const requiredMenuIds = ['main-hub', 'flightscoutpro', 'ghost-esim', 'ride-stay', 'experience-vault', 'amazon-gear'];
for (const id of requiredMenuIds) {
  if (!builtVault.includes('id:"' + id + '"')) throw new Error('Build failed: menu item missing: ' + id);
}
if (!builtVault.includes('battery.level<=0.20&&!battery.charging')) throw new Error('Build failed: battery watchdog missing.');
if (fs.readFileSync(path.join(dist, 'roksana-vault.js'), 'utf8') !== fs.readFileSync(path.join(dist, 'roksana-vault-final.js'), 'utf8')) {
  throw new Error('Build failed: vault files are not byte-identical.');
}
const hotelFallback = fs.readFileSync(path.join(dist, 'booking-fallback.html'), 'utf8');
if (!hotelFallback.includes('Not live availability') || !hotelFallback.includes('No corporate cookies') || !hotelFallback.includes('marker=787950')) {
  throw new Error('Build failed: honest hotel fallback disclosure or marker missing.');
}

const catalog = JSON.parse(fs.readFileSync(path.join(root, 'affiliate-services.json'), 'utf8'));
if (catalog.services.length !== 21) throw new Error('Build failed: affiliate catalogue must contain exactly 21 programs.');
if (catalog.marker !== '787950' || catalog.markerHex !== '373837393530') throw new Error('Build failed: affiliate marker or hex mismatch.');
if (catalog.services[20].name !== 'Amazon' || catalog.services[20].program_number !== 21 || catalog.services[20].featured !== true) {
  throw new Error('Build failed: Amazon must be Featured #21.');
}
for (const service of catalog.services) {
  if (!service.url.includes('marker=787950')) throw new Error('Build failed: missing marker on ' + service.name);
  if (!service.category || !service.category_id) throw new Error('Build failed: category missing on ' + service.name);
}
const publicCatalog = JSON.parse(fs.readFileSync(path.join(root, 'public', 'affiliate-services.json'), 'utf8'));
if (JSON.stringify(catalog) !== JSON.stringify(publicCatalog)) throw new Error('Build failed: public catalogue differs from root source.');
if (!builtHtml.includes('data-design-balance="80-20"') || !builtHtml.includes('Featured #21')) {
  throw new Error('Build failed: category directory or 80/20 trust balance missing.');
}
if ((builtHtml.match(/data-affiliate-id=/g) || []).length !== 21) throw new Error('Build failed: homepage must render exactly 21 programs.');
const draftPublisher = fs.readFileSync(path.join(root, 'scripts', 'publish_news.py'), 'utf8');
if (!draftPublisher.includes('isDraft=True') || !draftPublisher.includes('service.posts().get(') || !draftPublisher.includes('DRAFT Verified')) {
  throw new Error('Build failed: real Blogger DRAFT verification is missing.');
}
const apiSource = fs.readFileSync(path.join(root, 'api', 'trtt_787950_master.py'), 'utf8');
if (!apiSource.includes('os.environ.get("TRAVELPAYOUTS_TOKEN")')) throw new Error('Build failed: Travelpayouts token must come from environment.');
const bloggerSource = fs.readFileSync(path.join(root, 'trtt_787950_master.py'), 'utf8');
if (bloggerSource.includes('amzn.to/') || bloggerSource.includes('.tpo.lv/')) throw new Error('Build failed: direct affiliate link found in Blogger draft source.');
if (!builtVault.includes('var BLOGGER_MENU_TOOLS = Object.freeze([') || !builtVault.includes('ACTIVE_MENU_TOOLS.forEach(function(t)')) {
  throw new Error('Build failed: Blogger gadget must render Vercel hub only.');
}
if (!builtVault.includes('Object.freeze(MARKER)') || !builtVault.includes('markerHex: "373837393530"')) {
  throw new Error('Build failed: immutable marker or marker hex missing.');
}

console.log('Build verified: 21 category programs, Amazon Featured #21, Blogger Vercel-only gadget, DRAFT policy and marker 787950 LOCKED.');
