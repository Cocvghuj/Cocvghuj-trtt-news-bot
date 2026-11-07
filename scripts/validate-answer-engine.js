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
const vault = read('roksana-vault.js');
const finalVault = read('roksana-vault-final.js');
const build = read('build.js');
const vercel = JSON.parse(read('vercel.json'));

assert.equal(browser, publicBrowser, 'Root and public Answer Engine scripts must be byte-identical.');
assert.equal(vault, finalVault, 'Roksana Vault source and published source must be byte-identical.');
assert.ok(vault.includes('rv-ai-question') && vault.includes('rv-ai-ask'), 'The published Vault must include the dual-AI question interface.');
assert.ok(vault.includes('https://cocvghuj-trtt-news-bot.vercel.app/api/answer'), 'The Vault must call the production Answer Engine API.');
assert.ok(vault.includes('trttnews24bd.blogspot.com') && vault.includes('trttnews24bd.com') && vault.includes('www.trttnews24bd.com'), 'Strict three-domain lock is missing.');
assert.ok(vault.includes("name:'Signature',g:'#ff2e63',k:'#FFC300',p:'#AF7AC5'"), 'Signature colors must remain exact.');
assert.ok(!/AIza[0-9A-Za-z_-]{20,}|sk-or-v1-[0-9a-f]{20,}/.test(vault), 'A provider secret appears in the published Vault.');
assert.ok(api.includes('process.env.GEMINI_API_KEY'), 'Gemini key must be server-side.');
assert.ok(api.includes('process.env.OPENROUTER_API_KEY'), 'OpenRouter key must be server-side.');
assert.ok(!/AIza[0-9A-Za-z_-]{20,}|sk-or-v1-[0-9a-f]{20,}/.test(api + browser), 'A provider secret appears hard-coded.');
assert.ok(api.includes('max_tool_calls: 3'), 'OpenRouter web-search tool-call limit is missing.');
assert.ok(api.includes('max_results: 5') && api.includes('max_uses: 3'), 'OpenRouter web-search result and use limits are missing.');
assert.ok(!api.includes('temperature: 0.2') && !api.includes('max_tokens: 900'), 'Provider request includes unsupported legacy generation parameters.');
assert.ok(browser.includes('/api/answer'), 'Browser client must call the Answer Engine API.');
assert.ok(browser.includes('https://cocvghuj-trtt-news-bot.vercel.app/api/answer'), 'Browser API endpoint changed; review before changing it.');
assert.ok(build.includes("'api'"), 'Static build must exclude server-only API source.');
assert.ok(build.includes("'scripts'"), 'Static build must exclude private validation and automation scripts.');
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

for (const [file, source] of [['api/answer.js', api], ['trtt-all-in-one.js', browser], ['roksana-vault.js', vault]]) {
  new vm.Script(source, { filename: file });
}

console.log('PASS: Answer Engine source, Vault sync, dual-AI UI, syntax, strict origins, secrets and Vercel config checks.');
