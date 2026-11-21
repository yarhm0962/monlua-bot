#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const detectModule = require('./src/detect');
const driver = require('./src/driver');

const SUPPORTED_EXTENSIONS = ['.lua', '.luau'];

const LURAPH_PLUGINS = ['luraph_v14_7', 'luraph_v14_8', 'luraph_v14_9', 'luraph_v14', 'luraph_v15'];

// Which Luraph family's VM mapper actually finds interpreter dispatch loops in
// this file? Used when the header/shape heuristics found nothing (a stripped or
// mangled header must not turn a real Luraph script into a trace-only job), and
// to pick the other family when the first one produced no lift.
function probeFamilies(source, workdir) {
  const found = [];
  const probe = path.join(workdir, '_probe.luau');
  try {
    fs.writeFileSync(probe, source, 'latin1');
    for (const [name, modPath] of [['luraph_v14_9', './src/vmmap14'], ['luraph_v15', './src/vmmap']]) {
      try {
        const m = require(modPath);
        const root = m.loadAst(probe);
        const n = m.findDispatchers(root).length;
        if (n > 0) found.push({ name, dispatchers: n });
      } catch (e) { /* not parseable / no mapper match: not this family */ }
    }
  } finally {
    try { fs.unlinkSync(probe); } catch (e) {}
  }
  return found.sort((a, b) => b.dispatchers - a.dispatchers);
}

function otherFamily(name) {
  return name === 'luraph_v15' ? 'luraph_v14_9' : 'luraph_v15';
}

function parseArgs(argv) {
  const args = {
    inputs: [],
    output: null,
    detect: false,
    plugin: null,
    noDevirt: false,
    noHooks: false,
    noFold: false,
    debug: false,
    strings: false,
    keepHarness: false,
    keepPreamble: false,
    timeout: 90,
    budget: 30,
    maxRuns: 12,
    devirtRounds: 200,
    executor: 'Wave',
    inputText: null,
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--detect') { args.detect = true; }
    else if (a === '--plugin') { args.plugin = argv[++i]; }
    else if (a === '--no-devirt') { args.noDevirt = true; }
    else if (a === '--no-engine-fallback') { args.noEngineFallback = true; }
    else if (a === '--no-hooks') { args.noHooks = true; }
    else if (a === '--no-fold') { args.noFold = true; }
    else if (a === '--debug') { args.debug = true; }
    else if (a === '--strings') { args.strings = true; }
    else if (a === '--keep-harness') { args.keepHarness = true; }
    else if (a === '--keep-preamble') { args.keepPreamble = true; }
    else if (a === '-o' || a === '--output') { args.output = argv[++i]; }
    else if (a === '--timeout') { args.timeout = parseInt(argv[++i], 10); }
    else if (a === '--prelude-file') { args.preludeFile = argv[++i]; }
    else if (a === '--budget') { args.budget = parseInt(argv[++i], 10); }
    else if (a === '--max-runs') { args.maxRuns = parseInt(argv[++i], 10); }
    else if (a === '--devirt-rounds') { args.devirtRounds = parseInt(argv[++i], 10); }
    else if (a === '--executor') { args.executor = argv[++i]; }
    else if (a === '--input-text') { args.inputText = argv[++i]; }
    else if (a === '--cfg-json') {
      // extra harness CFG as inline JSON or '@file.json' (e.g. readfile_map,
      // http_map, real_json) -- merged into the cfg of every run
      let spec = argv[++i];
      if (spec.startsWith('@')) spec = fs.readFileSync(spec.slice(1), 'utf8');
      args.cfgJson = JSON.parse(spec);
    }
    else if (!a.startsWith('-')) { args.inputs.push(a); }
  }

  return args;
}

class Job {
  constructor(inputPath, source, args, tracePath, debug, obfuscator = '') {
    this.input = inputPath;
    this.source = source;
    this.sourcePath = inputPath;
    this.args = args;
    this.tracePath = tracePath;
    this.debug = debug;
    this.obfuscator = obfuscator;
  }

  creditHeader() {
    return '';
  }

  get base() {
    return this.tracePath.replace(/\.(deobf\.luau|luau)$/, '');
  }

  path(suffix) {
    return this.base + suffix;
  }

  wrote(p) {
    if (this.debug) process.stderr.write(`[+] wrote ${p}\n`);
  }

  write(p, text, encoding = 'utf8') {
    fs.writeFileSync(p, text, { encoding });
    this.wrote(p);
    return p;
  }

  get outdir() {
    return path.dirname(path.resolve(this.tracePath));
  }
}

function collectInputFiles(rawPaths) {
  const files = [];
  const seen = new Set();

  for (const raw of rawPaths) {
    const abs = path.resolve(raw);
    if (!fs.existsSync(abs)) {
      process.stderr.write(`[!] path not found, skipping: ${raw}\n`);
      continue;
    }
    const stat = fs.statSync(abs);
    if (stat.isDirectory()) {
      const entries = fs.readdirSync(abs, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isFile() && SUPPORTED_EXTENSIONS.includes(path.extname(entry.name).toLowerCase())) {
          const filePath = path.join(abs, entry.name);
          if (!seen.has(filePath)) {
            seen.add(filePath);
            files.push(filePath);
          }
        }
      }
    } else if (stat.isFile()) {
      const ext = path.extname(abs).toLowerCase();
      if (!SUPPORTED_EXTENSIONS.includes(ext)) {
        process.stderr.write(`[!] unsupported extension for ${raw} (expected ${SUPPORTED_EXTENSIONS.join(', ')})\n`);
        continue;
      }
      if (!seen.has(abs)) {
        seen.add(abs);
        files.push(abs);
      }
    }
  }

  return files;
}

async function processFile(absInput, args) {
  const source = fs.readFileSync(absInput, 'latin1');
  let plugin, confidence;
  if (args.plugin) {
    plugin = detectModule.byName(args.plugin); // force a plugin (e.g. v14.x headers score 0.3)
    confidence = 1.0;
  } else {
    ({ plugin, confidence } = detectModule.detect(source.replace(/^\xEF\xBB\xBF/, '')));
  }

  if (args.detect) {
    console.log(`${path.basename(absInput)}\t${plugin.name}\t${confidence.toFixed(2)}\t${plugin.label}`);
    return;
  }

  if (plugin.name === 'generic' && !args.plugin) {
    // detection found no header or fingerprint: ask the mappers before settling for a trace
    const os0 = require('os');
    const tmp0 = fs.mkdtempSync(path.join(os0.tmpdir(), 'deobf_probe_'));
    try {
      const fam = probeFamilies(source, tmp0);
      if (fam.length) {
        plugin = detectModule.byName(fam[0].name);
        confidence = 0.5;
        process.stderr.write(`[*] no Luraph header found, but the VM structure matches ${plugin.label} ` +
          `(${fam[0].dispatchers} dispatch loop(s)); using it\n`);
      }
    } finally {
      try { fs.rmSync(tmp0, { recursive: true, force: true }); } catch (e) {}
    }
  }

  process.stderr.write(`[*] obfuscator: ${plugin.label} (detected, ${confidence.toFixed(2)})\n`);

  const outdir = path.join(path.dirname(absInput), 'output');
  fs.mkdirSync(outdir, { recursive: true });

  const tracename = path.basename(absInput).replace(/(\.luau?|\.txt)?$/, '.deobf.luau');
  const os = require('os');
  const workdir = args.debug ? null : fs.mkdtempSync(path.join(os.tmpdir(), 'deobf_node_'));

  const tracePath = args.debug
    ? (args.output || path.join(outdir, tracename))
    : path.join(workdir, tracename);
  const final = (args.output && args.inputs.length === 1)
    ? args.output
    : path.join(outdir, path.basename(absInput));

  fs.mkdirSync(path.dirname(path.resolve(final)), { recursive: true });

  try {
    // a UTF-8 BOM in front of the code is not valid Luau; drop it (and split a header that ran into the code)
    const fixed = detectModule.restoreHeaderNewline(source.replace(/^\xEF\xBB\xBF/, ''));
    let jobSource = source;
    let sourcePath = absInput;

    if (fixed !== source) {
      process.stderr.write('[*] normalized the input (BOM removed / header comment ran into the code)\n');
      jobSource = fixed;
      sourcePath = path.join(workdir || outdir, path.basename(absInput) + '.src.lua');
      fs.writeFileSync(sourcePath, fixed, 'latin1');
    }

    const job = new Job(absInput, jobSource, args, tracePath, args.debug, plugin.label);
    job.sourcePath = sourcePath;

    let result;
    if (plugin.name === 'luarmor_client') {
      // Auth-gated loader: control flow is not virtualized, but tracing deadlocks
      // on wall-clock anti-tamper (docs/LUARMOR_NOTES.md §4, §8). Route instead.
      throw new Error(
        'Luarmor whitelist client detected — devirtualization/tracing not applicable. ' +
        'Use tools/luarmor_probe.py to classify and split loader vs payload.'
      );
    } else if (
      plugin.name === 'luraph_v15' ||
      plugin.name === 'luraph_v14' ||
      plugin.name === 'luraph_v14_7' ||
      plugin.name === 'luraph_v14_8' ||
      plugin.name === 'luraph_v14_9'
    ) {
      result = await driver.run(job);
    } else {
      result = await driver.runGeneric(job);
    }

    // The first engine family only produced a trace: if the header was not an
    // exact match (or the file was routed by structure), the other family's
    // mapper may be the right one. Costs one more trace run, only on failure.
    const isLuraph = LURAPH_PLUGINS.includes(plugin.name);
    const gotTrace = result && !/\.devirt\.luau$|\.loadstring_recovered\.lua$/.test(result);
    // an exact header (confidence 1.0) already fixes the family; only a guessed one is retried
    if (isLuraph && gotTrace && confidence < 1.0 && !args.noDevirt && !args.plugin && !args.noEngineFallback) {
      const alt = detectModule.byName(otherFamily(plugin.name));
      process.stderr.write(`[*] ${plugin.label} gave no devirtualized output; trying ${alt.label}\n`);
      try {
        const job2 = new Job(absInput, jobSource, args, tracePath, args.debug, alt.label);
        job2.sourcePath = sourcePath;
        const result2 = await driver.run(job2);
        if (result2 && fs.existsSync(result2) && /\.(devirt\.luau|loadstring_recovered\.lua)$/.test(result2)) result = result2;
      } catch (e) {
        process.stderr.write(`[!] ${alt.label} attempt failed: ${e.message || e}\n`);
      }
    }

    if (final && result && fs.existsSync(result)) {
      let content = fs.readFileSync(result, 'utf8');
      content = content.replace(/^(\s*--(?:[ \t]*(?:Deobfuscated(?:\s+(?:by|in|with))?|Detected obfuscation|Local names are inferred|source:|NOTE: reconstructed|during the trace|yeah this ran at runtime|not gonna be full|Luraph v\d|Devirtualized with)[^\n]*\n?|\s*\n))+/, '');
      fs.writeFileSync(final, content, 'utf8');

      // v4: run sl_post.py for trace-only outputs (devirt outputs are post-processed
      // directly in the Python pipeline; this covers --no-devirt and fallback traces)
      if (args.noDevirt || !result.endsWith('.devirt.luau')) {
        try {
          const { execFileSync } = require('child_process');
          const { getPythonBin } = require('./src/pyenv');
          const pythonBin = getPythonBin();
          const slPostPy = path.join(__dirname, 'core', 'sl_post.py');
          if (fs.existsSync(slPostPy)) {
            const runner = `
import sys
sys.path.insert(0, r'${path.join(__dirname, 'core').replace(/\\/g, '\\\\')}')
import sl_post
sl_post.process_file(sys.argv[1])
`;
            execFileSync(pythonBin, ['-c', runner, final], { stdio: 'inherit' });
          }
        } catch (e) {
          process.stderr.write(`[!] sl_post pass failed (continuing): ${e.message}\n`);
        }
      }

      process.stderr.write(`[+] result: ${final}\n`);
      return final;
    }
    process.stderr.write(`[!] no result for ${path.basename(absInput)}\n`);
    return null;
  } finally {
    if (workdir && fs.existsSync(workdir)) {
      try { fs.rmSync(workdir, { recursive: true, force: true }); } catch {}
    }
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.inputs.length === 0) {
    console.error('Usage: node deob.js <input.lua | folder> [more_files_or_folders...] [-o <output.lua>] [--plugin <name>] [--no-devirt] [--debug] [--detect]');
    process.exit(2);
  }

  const files = collectInputFiles(args.inputs);
  if (files.length === 0) {
    console.error('[!] no valid .lua / .luau input files found');
    process.exit(1);
  }

  if (args.detect) {
    for (const file of files) {
      const source = fs.readFileSync(file, 'latin1');
      let plugin, confidence;
      if (args.plugin) { plugin = detectModule.byName(args.plugin); confidence = 1.0; }
      else ({ plugin, confidence } = detectModule.detect(source));
      console.log(`${path.basename(file)}\t${plugin.name}\t${confidence.toFixed(2)}\t${plugin.label}`);
    }
    return;
  }

  if (files.length > 1 && args.output) {
    process.stderr.write('[!] --output is ignored for multiple inputs (each file goes into its own output/ folder)\n');
  }

  let succeeded = 0;
  let failed = 0;

  for (const file of files) {
    process.stderr.write(`\n[*] processing ${file}\n`);
    try {
      const res = await processFile(file, args);
      if (res) succeeded++;
      else failed++;
    } catch (err) {
      process.stderr.write(`[!] failed on ${path.basename(file)}: ${err.message || err}\n`);
      failed++;
    }
  }

  process.stderr.write(`\n[*] done: ${succeeded} succeeded, ${failed} failed out of ${files.length}\n`);
  if (failed > 0 && succeeded === 0) process.exit(1);
}

main().catch(err => {
  process.stderr.write('[!] Fatal error: ' + (err.message || err) + '\n');
  process.exit(1);
});
