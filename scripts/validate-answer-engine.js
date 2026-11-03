'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');

const api = read('api/answer.js');
const browser = read('trtt-all-in-one.js');
const publicBrowser = read('public/trtt-all-in-one.js');
const build = read('build.js');
const vercel = JSON.parse(read('vercel.json'));

assert.equal(browser, publicBrowser, 'Root and public Answer Engine scripts must be byte-identical.');
assert.ok(api.includes('process.env.GEMINI_API_KEY'), 'Gemini key must be server-side.');
assert.ok(api.includes('process.env.OPENROUTER_API_KEY'), 'OpenRouter key must be server-side.');
assert.ok(!/AIza[0-9A-Za-z_-]{20,}|sk-or-v1-[0-9a-f]{20,}/.test(api + browser), 'A provider secret appears hard-coded.');
assert.ok(api.includes('max_tool_calls: 3'), 'OpenRouter web-search tool-call limit is missing.');
assert.ok(api.includes('max_total_results: 10'), 'OpenRouter result limit is missing.');
assert.ok(browser.includes('/api/answer'), 'Browser client must call the Answer Engine API.');
assert.ok(browser.includes('https://cocvghuj-trtt-news-bot.vercel.app/api/answer'), 'Browser API endpoint changed; review before changing it.');
assert.ok(build.includes("'api'"), 'Static build must exclude server-only API source.');
assert.equal(vercel.outputDirectory, 'dist', 'Vercel output directory must remain dist.');
assert.equal(vercel.functions?.['api/answer.js']?.maxDuration, 30, 'Answer API maxDuration must remain 30 seconds.');

const allowedOrigins = [
  'https://trttnews24bd.blogspot.com',
  'https://trttnews24bd.com',
  'https://www.trttnews24bd.com'
];
for (const origin of allowedOrigins) assert.ok(api.includes(origin), 'Missing allowed origin: ' + origin);
const configuredOrigins = [...api.matchAll(/"https:\/\/(?:www\.)?trttnews24bd(?:\.blogspot)?\.com"/g)].map((m) => m[0]);
assert.equal(configuredOrigins.length, 3, 'The API must retain exactly the approved three-origin allowlist.');

for (const [file, source] of [['api/answer.js', api], ['trtt-all-in-one.js', browser]]) {
  new vm.Script(source, { filename: file });
}

console.log('PASS: Answer Engine source, syntax, origins, secrets, frontend sync and Vercel config checks.');
