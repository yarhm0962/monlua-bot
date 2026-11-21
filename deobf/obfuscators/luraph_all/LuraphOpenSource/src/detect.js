'use strict';

// The header is matched loosely (case, spacing, "v 14.8", a trailing patch
// number) and searched in the first HEADER_SCAN chars instead of the first 500:
// a key line, a BOM or a pasted prefix in front of it used to push it out of
// range, and the script then fell through to the trace-only generic route.
const LURAPH_HEADER = /Luraph\s+Obfuscator\s+v?\s*(\d+)(?:\.(\d+))?/i;
const HEADER_SCAN = 8192;
function findHeader(source) { return LURAPH_HEADER.exec(source.slice(0, HEADER_SCAN)); }
const LURAPH_VM_SHAPE = /\[\d+\]=(bit32|buffer|string|table|math)\.\w+/;
// v15 chunks primed by loader stubs (Luarmor etc.) start with loader lines
// (script_key/_bsdata0/blob tables); the VM chunk starts later with
// `return setmetatable({` — usually at a line start, sometimes directly
// after the stub's closing long-bracket (`]]]]return setmetatable...`).
// Scan the first 64 KB for that boundary (the VM-shape check below is the
// real validator).
const VM_CHUNK_START = /[\s\]]*return setmetatable\(\{/;

// Structural fingerprints for scripts whose header was removed, mangled or
// moved. v14 wraps the VM in `return(function(...)` / `local init=(function(...)`
// (the VM object literal is `return({`); v15 uses `return setmetatable({`.
const V14_WRAPPER = /(?:^|[\s;\]])(?:return\s*\(\s*function\s*\(\s*\.\.\.\s*\)|local\s+init\s*=\s*\(\s*function\s*\(\s*\.\.\.\s*\)|return\s*\(\s*\{)/;
const SHAPE_SCAN = 262144;

function vmShape(source) {
  const head = source.slice(0, SHAPE_SCAN);
  return LURAPH_VM_SHAPE.test(head) || head.includes('LPH') || /\bbit32\.(?:bxor|band|rshift|lshift)\b/.test(head);
}

function detectLuraph14(source) {
  const m = findHeader(source);
  if (m) return m[1] === '14' ? 1.0 : 0.0;
  return V14_WRAPPER.test(source.slice(0, SHAPE_SCAN)) && vmShape(source) &&
    !VM_CHUNK_START.test(source.slice(0, 65536)) ? 0.55 : 0.0;
}

function detectLuraph(source) {
  const m = findHeader(source);
  if (m) {
    if (m[1] === '15') return 1.0;
    return m[1] === '14' ? 0.3 : 0.6;   // newer than 15: the v15 engine is the closest
  }
  const head = source.slice(0, 65536);
  const vm = VM_CHUNK_START.exec(head);
  if (vm) {
    const at = vm.index + vm[0].length - 'return setmetatable({'.length;
    const chunkHead = source.slice(at, at + 200000);
    if (LURAPH_VM_SHAPE.test(chunkHead) || source.slice(at, at + 200000).includes('LPH')) {
      return 0.8;
    }
  }
  return 0.0;
}

const HEADER_LINE_RE = /\s*--[ \t]*This file was protected using Luraph Obfuscator v[\d.]+[ \t]*\[https?:\/\/lura\.ph\/?\]/;

function restoreHeaderNewline(source) {
  const m = HEADER_LINE_RE.exec(source);
  if (m) {
    const end = m.index + m[0].length;
    const next = source[end];
    if (next !== '' && next !== '\n' && next !== '\r') {
      return source.slice(0, end) + '\n' + source.slice(end).replace(/^[ \t]+/, '');
    }
  }
  return source;
}

// Luarmor whitelist client (see docs/LUARMOR_NOTES.md §9 for the rationale).
// These files are auth-gated loaders around a Luraph-VM constant layer; they
// are not devirtualizable, so detection exists to classify and route them.
const LUARMOR_SIGS = [
  /luarmor\.net|Luarmor/i,
  /\bluraph_runtime1\s*\(/,
  /GetTutorialState\(\s*"nil\s+nil\s+/,
  /getfenv\(\)\s*\[\s*tbl\w+\s*\]\s*=/,
  /writefile\(\s*"luarmor-error-log\.txt"/,
  /[a-z]{1,3}\d-roblox-auth\.luarmor\.net/,
  /ce_like_loadstring_fn/,
  /Kick\(\s*"\[Luarmor\]/,
];

function detectLuarmor(source) {
  let hits = 0;
  for (const rx of LUARMOR_SIGS) {
    if (rx.test(source)) hits += 1;
  }
  if (hits >= 4) return 1.0;
  if (hits >= 3) return 0.9;
  if (hits >= 2) return 0.7; // single-sig canaries live below the 0.5 gate
  return 0.0;
}

const PLUGINS = [
  {
    name: 'luraph_v14_7',
    label: 'Luraph v14.7',
    detect: (src) => {
      const m = findHeader(src);
      if (m && m[1] === '14' && m[2] === '7') return 1.0;
      if (m && m[1] === '14') return 0.1;
      // headerless v14 shape: the newest v14 engine is the best guess (the
      // other engines are tried by the retry chain)
      return 0.0;
    },
  },
  {
    name: 'luraph_v14_8',
    label: 'Luraph v14.8',
    detect: (src) => {
      const m = findHeader(src);
      if (m && m[1] === '14' && m[2] === '8') return 1.0;
      if (m && m[1] === '14') return 0.1;
      // headerless v14 shape: the newest v14 engine is the best guess (the
      // other engines are tried by the retry chain)
      return 0.0;
    },
  },
  {
    name: 'luraph_v14_9',
    label: 'Luraph v14.9',
    detect: (src) => {
      const m = findHeader(src);
      if (m && m[1] === '14' && m[2] === '9') return 1.0;
      if (m && m[1] === '14' && m[2] && parseInt(m[2], 10) > 9) return 0.9;   // 14.10+: newest engine
      if (m && m[1] === '14') return 0.1;
      // headerless v14 shape: the newest v14 engine is the best guess (the
      // other engines are tried by the retry chain)
      return (!m && detectLuraph14(src) > 0 ? 0.6 : 0.0);
    },
  },
  {
    name: 'luraph_v14',
    label: 'Luraph v14',
    detect: detectLuraph14,
  },
  {
    name: 'luraph_v15',
    label: 'Luraph v15',
    detect: detectLuraph,
  },
  {
    name: 'luarmor_client',
    label: 'Luarmor whitelist client (loader; payload not devirtualizable)',
    detect: detectLuarmor,
  },
];

function detect(source) {
  let best = { plugin: null, confidence: 0 };
  for (const p of PLUGINS) {
    const c = p.detect(source);
    if (c > best.confidence) best = { plugin: p, confidence: c };
  }
  if (best.confidence < 0.5) {
    return { plugin: { name: 'generic', label: 'unknown obfuscator (behaviour trace only)' }, confidence: 0 };
  }
  return { plugin: best.plugin, confidence: best.confidence };
}

function byName(name) {
  const p = PLUGINS.find(x => x.name === name);
  if (!p) throw new Error(`Unknown obfuscator '${name}' (known: ${PLUGINS.map(x => x.name).join(', ')})`);
  return p;
}

module.exports = { detect, byName, restoreHeaderNewline, PLUGINS };
