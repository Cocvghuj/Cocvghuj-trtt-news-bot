#!/usr/bin/env node
/**
 * TRTT Control Assets & Version Guard Validator
 * Marker: TRTT MAC-787950 LOCKED
 * Production Version: V106
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const rootDir = path.resolve(__dirname, '..');
const REQUIRED_VERSION = '106';

console.log('🔍 [TRTT Validation] Starting syntax and version audit...');

// 1. Validate JS syntax with node --check
const jsFiles = [
  'trtt-loader.js',
  'trtt-control/trtt-app-106.js',
  'trtt-control/trtt-app.js',
  'trtt-control/trtt-loader.js',
  'api/answer.js',
  'trtt-all-in-one.js'
];

for (const relPath of jsFiles) {
  const fullPath = path.join(rootDir, relPath);
  if (fs.existsSync(fullPath)) {
    try {
      execSync(`node --check "${fullPath}"`, { stdio: 'pipe' });
      console.log(`  ✓ JS Syntax OK: ${relPath}`);
    } catch (err) {
      console.error(`  ❌ JS Syntax Error in ${relPath}:`, err.stderr ? err.stderr.toString() : err.message);
      process.exit(1);
    }
  }
}

// 2. Validate CSS brace matching
const cssFiles = [
  'trtt-control/trtt-app-106.css',
  'trtt-control/trtt-app.css'
];

for (const relPath of cssFiles) {
  const fullPath = path.join(rootDir, relPath);
  if (fs.existsSync(fullPath)) {
    const content = fs.readFileSync(fullPath, 'utf8');
    let depth = 0;
    for (let i = 0; i < content.length; i++) {
      if (content[i] === '{') depth++;
      else if (content[i] === '}') {
        depth--;
        if (depth < 0) {
          console.error(`  ❌ CSS Error in ${relPath}: Unmatched closing brace at char ${i}`);
          process.exit(1);
        }
      }
    }
    if (depth !== 0) {
      console.error(`  ❌ CSS Error in ${relPath}: Unclosed brace (unbalanced depth: ${depth})`);
      process.exit(1);
    }
    console.log(`  ✓ CSS Braces Balanced: ${relPath}`);
  }
}

// 3. Version Lock Guard: Verify production loader is locked to V106
const loaderPath = path.join(rootDir, 'trtt-loader.js');
if (fs.existsSync(loaderPath)) {
  const loaderContent = fs.readFileSync(loaderPath, 'utf8');
  if (!loaderContent.includes(`var version = "${REQUIRED_VERSION}";`) && !loaderContent.includes(`VERSION 106`)) {
    console.error(`  ❌ Version Guard Violation: trtt-loader.js must remain on production version ${REQUIRED_VERSION}`);
    process.exit(1);
  }
  console.log(`  ✓ Version Guard: trtt-loader.js locked to V${REQUIRED_VERSION}`);
}

console.log('✅ [TRTT Validation] All syntax, CSS, and version guard checks passed successfully!');
