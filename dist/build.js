const fs = require('fs');
const path = require('path');

const root = __dirname;
const dist = path.join(root, 'dist');

if (fs.existsSync(dist)) {
  fs.rmSync(dist, { recursive: true, force: true });
}
fs.mkdirSync(dist, { recursive: true });

function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
    fs.readdirSync(src).forEach(child => {
      copyRecursive(path.join(src, child), path.join(dest, child));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

const ignored = new Set(['.git', '.github', 'dist', 'node_modules', '.gitignore']);

fs.readdirSync(root).forEach(file => {
  if (ignored.has(file)) return;
  copyRecursive(path.join(root, file), path.join(dist, file));
});

console.log('Build complete: All static files copied to dist/');
