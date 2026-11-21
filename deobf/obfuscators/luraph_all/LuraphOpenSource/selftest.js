#!/usr/bin/env node
'use strict';
// Quick regression check: `node selftest.js` (exit code 0 = all good).
// Covers the failure modes that used to turn real Luraph scripts into
// behaviour traces: header detection, and every engine finding luau-ast.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const detect = require('./src/detect');
const { getPythonBin } = require('./src/pyenv');

let bad = 0;
function check(name, ok, extra) {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
  if (!ok) bad++;
}

const H = '-- This file was protected using Luraph Obfuscator v14.8 [https://lura.ph/]\n';
const body = 'return(function(...) local a={[1]=bit32.band} while true do local op=a[1]; end end)(...)';
const cases = [
  ['exact header', H + body, 'luraph_v14_8'],
  ['header pushed past 500 chars', 'x=1\n--' + ' '.repeat(900) + '\n' + H + body, 'luraph_v14_8'],
  ['header with odd case/spacing', '-- this file was protected using luraph obfuscator V 14.9\n' + body, 'luraph_v14_9'],
  ['header removed (v14 shape)', body, 'luraph_v14_9'],
  ['v15 header', '-- This file was protected using Luraph Obfuscator v15.1 [https://lura.ph/]\nreturn setmetatable({},{})', 'luraph_v15'],
];
for (const [n, src, want] of cases) {
  const r = detect.detect(src);
  check('detect: ' + n, r.plugin.name === want, `${r.plugin.name} ${r.confidence.toFixed(2)}`);
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'selftest_'));
const f = path.join(tmp, 't.luau');
fs.writeFileSync(f, 'local x = 1\nreturn x\n');
const py = `
import sys
sys.path.insert(0, sys.argv[1])
import importlib, harness
for m in ("luraph_v14_7", "luraph_v14_8", "luraph_v14_9", "luraph_v14", "luraph_v15"):
    mod = importlib.import_module("obfuscators.%s.vmmap" % m)
    mod.load_ast(sys.argv[2])
    print(m)
`;
try {
  const out = execFileSync(getPythonBin(), ['-I', '-c', py, path.join(__dirname, 'core'), f], { encoding: 'utf8' });
  check('every engine locates luau-ast', out.trim().split('\n').length === 5, out.trim().replace(/\n/g, ' '));
} catch (e) {
  check('every engine locates luau-ast', false, String(e.stderr || e.message).trim().split('\n').pop());
}
fs.rmSync(tmp, { recursive: true, force: true });

// lowering back end: random CFGs + readability-pass failure containment
try {
  const out = execFileSync(getPythonBin(), ['-I', path.join(__dirname, 'tests', 'lowering_selftest.py')],
    { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  out.trim().split('\n').forEach(l => { if (/^(PASS|FAIL)/.test(l)) { console.log(l); if (l.startsWith('FAIL')) bad++; } });
} catch (e) {
  check('lowering back end', false, String(e.stdout || e.stderr || e.message).trim().split('\n').slice(-3).join(' | '));
}
process.exit(bad ? 1 : 0);
