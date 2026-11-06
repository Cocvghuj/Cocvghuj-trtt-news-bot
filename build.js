const fs = require('fs');
const path = require('path');
const root = __dirname;
const dist = path.join(root, 'dist');
const PUBLIC_EXTENSIONS = new Set(['.html','.css','.js','.mjs','.svg','.png','.jpg','.jpeg','.webp','.gif','.ico','.woff','.woff2','.ttf','.otf','.xml','.webmanifest']);
const PUBLIC_JSON_FILES = new Set(['affiliate-services.json','manifest.json','blog-control.json']);
const PUBLIC_TEXT_FILES = new Set(['robots.txt','sitemap.txt']);
const PRIVATE_FILES = new Set(['build.js']);
const IGNORED_DIRECTORIES = new Set(['.git','.github','api','dist','node_modules','tests','__pycache__','.venv','venv','logs','private','data']);
if(fs.existsSync(dist))fs.rmSync(dist,{recursive:true,force:true});
fs.mkdirSync(dist,{recursive:true});
function isPublicAsset(filePath){const filename=path.basename(filePath).toLowerCase();if(PRIVATE_FILES.has(filename))return false;if(PUBLIC_JSON_FILES.has(filename)||PUBLIC_TEXT_FILES.has(filename))return true;return PUBLIC_EXTENSIONS.has(path.extname(filename));}
function copyRecursive(src,dest){const stat=fs.statSync(src);if(stat.isDirectory()){if(IGNORED_DIRECTORIES.has(path.basename(src).toLowerCase()))return;if(!fs.existsSync(dest))fs.mkdirSync(dest,{recursive:true});fs.readdirSync(src).forEach(child=>copyRecursive(path.join(src,child),path.join(dest,child)));return;}if(!isPublicAsset(src))return;const parent=path.dirname(dest);if(!fs.existsSync(parent))fs.mkdirSync(parent,{recursive:true});fs.copyFileSync(src,dest);}
fs.readdirSync(root).forEach(file=>{if(IGNORED_DIRECTORIES.has(file.toLowerCase()))return;copyRecursive(path.join(root,file),path.join(dist,file));});
const builtIndex=path.join(dist,'index.html');
if(!fs.existsSync(builtIndex))throw new Error('Build failed: dist/index.html was not created.');
const html=fs.readFileSync(builtIndex,'utf8');
for(const [needle,message] of [['TRTT','brand missing'],['VOYAGE','TRTT Voyage branding missing'],['787950 LOCKED','marker missing'],['https://cocvghuj-trtt-news-bot.vercel.app','Travel Tools link missing'],['roksana-vault.js','marker bottom dock source missing'],['hero-flight.svg','hero plane-and-city artwork missing']])if(!html.includes(needle))throw new Error('Build failed: '+message+'.');
console.log('Build verified: TRTT Voyage homepage, marker and public assets are present.');
