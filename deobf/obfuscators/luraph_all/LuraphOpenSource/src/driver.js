'use strict';

const fs = require('fs');
const path = require('path');
let vmmap = require('./vmmap');
const harness = require('./harness');
const trace = require('./traceout');
const tidy = require('./tidy');

const SPIN_CHECKS = 24;

// Lift engines tried in order for one trace. The v14.7/14.8/14.9 engines are
// strict (they refuse a partial lift); the plain v14 engine is the lenient one
// (v15 walker + v14 mapper) and often still lifts what the strict one gives up on.
function liftEngines(label) {
  const l = label || '';
  if (/v14\.\d/i.test(l)) return [l, 'Luraph v14'];
  return [l];
}

// A lifted file is a result only if it holds code; unresolved markers and
// calls of nil are how a misread VM shows up.
function liftQuality(text) {
  let code = 0, marks = 0;
  for (const raw of text.split('\n')) {
    const t = raw.trim();
    if (!t) continue;
    if (t.startsWith('--')) {
      if (/unresolved native\/runtime closure|unresolved Luraph runtime helper|^-- VM .* not lifted|could not recover this block|devirt: /.test(t)) marks++;
      continue;
    }
    code++;
  }
  const nilCalls = (text.match(/\(nil\)\(/g) || []).length;
  const lines = text.split('\n').length;
  const broken = code === 0 || (nilCalls >= 50 && nilCalls * 100 >= lines);
  // higher is better; a lift full of unresolved markers loses to a cleaner one
  return { code, marks, nilCalls, broken, score: code - 25 * marks - 10 * nilCalls };
}

function looksObfuscated(src) {
  try { return require('./detect').detect(src).confidence >= 0.5; } catch (e) { return false; }
}

const TRACE_NOTE =
  '-- NOTE: this is NOT the original source. Devirtualization did not complete, so what follows is a\n' +
  '-- runtime behaviour trace: the calls the script made while it ran in a fake environment.\n';

function patchChunk(src, tmpdir, chunkTag) {
  const p = path.join(tmpdir, `_chunk_${harness.chunkKey(src)}.luau`);
  fs.writeFileSync(p, src, 'latin1');
  try {
    return vmmap.patchEntries(src, p, chunkTag);
  } catch (e) {
    process.stderr.write(`[!] could not instrument chunk (${e.message})\n`);
    return src;
  } finally {
    try { fs.unlinkSync(p); } catch {}
  }
}

async function run(job) {
  const { args } = job;
  const devirtOn = !args.noDevirt;
  let source = job.source;
  vmmap = /v14/i.test(job.obfuscator || '') ? require('./vmmap14') : require('./vmmap');

  let patched;
  let hooksFailed = null;
  try {
    patched = args.noHooks ? source : vmmap.patchEntries(source, job.sourcePath, harness.chunkKey(source));
  } catch (e) {
    // No instrumentation means no captured protos (so nothing to lift), but the
    // script can still be traced: do that instead of failing the whole file.
    process.stderr.write(`[!] could not instrument the VM (${e.message}); tracing without lifting\n`);
    hooksFailed = e.message;
    patched = source;
  }

  let spin = true;
  if (spin) patched = vmmap.patchSpin(patched);

  const cachePath = harness.loadP2dCache(job.input);
  const runner = new harness.Runner(job);

  const skip = [];
  const chunks = {};
  const rawChunks = {};
  let body = null;
  let trapped = null;
  let cfg = null;
  let degraded = 0;

  for (let attempt = 1; attempt <= args.maxRuns; attempt++) {
    cfg = {
      time_budget: args.budget,
      dump_strings: args.strings,
      executor: args.executor,
      skip_protos: skip,
      devirt: devirtOn,
    };
    if (args.inputText) cfg.input_text = args.inputText;
    if (args.preludeFile) cfg.prelude = require('fs').readFileSync(args.preludeFile, 'latin1');
    if (args.noFold) cfg.fold = false;
    if (spin) cfg.spin = degraded ? Math.max(4, SPIN_CHECKS >> (degraded + 1)) : SPIN_CHECKS;
    if (args.cfgJson) Object.assign(cfg, args.cfgJson);

    process.stderr.write(`[*] tracing ${job.input} (run ${attempt})...\n`);
    const res = await runner.run(patched, cfg, chunks);
    body = res.body;

    if (!body) {
      // A run that timed out (or died) leaves nothing to lift. Retry with a
      // shorter script-time budget and a tighter spin watchdog so the runtime
      // ends the script itself and still reports what it captured.
      const why = (res.err || '').trim().split('\n').pop() || 'no output';
      if (degraded < 1) {     // one retry only: each failed attempt costs a full timeout
        degraded++;
        args.budget = Math.max(5, Math.min(Math.floor(args.budget / 2), Math.floor(args.timeout / 3)));
        process.stderr.write(`[!] trace run failed (${why.slice(0, 160)}); ` +
          `retrying once with a ${args.budget}s script budget\n`);
        attempt--;      // a failed run is not one of the anti-tamper reruns
        continue;
      }
      runner.finish();
      throw new Error(res.err || 'Trace failed without output');
    }

    body = harness.takeP2d(body);

    const { chunks: found, body: cleanBody } = harness.takeChunks(body);
    body = cleanBody;
    let added = 0;
    for (const [key, src] of found) {
      if (!chunks[key]) {
        rawChunks[key] = src;
        chunks[key] = patchChunk(src, job.outdir, key);
        if (spin) chunks[key] = vmmap.patchSpin(chunks[key]);
        added++;
      }
    }
    if (added > 0) {
      process.stderr.write(`[*] script loadstring'd ${added} new VM chunk(s); instrumenting and re-running\n`);
      continue;
    }

    const trig = new RegExp(harness.mark('TRIGGER ') + '(\\d+)').exec(body);
    if (trapped !== null && trace.stmtCount(body) < trace.stmtCount(trapped[0])) {
      process.stderr.write(`[*] disabling function #${skip[skip.length - 1]} made script stop earlier: keeping run ${attempt - 1}\n`);
      body = trapped[0];
      skip.pop();
      break;
    }
    if (!trig) break;

    trapped = [body, harness.getLastRaw()];
    const pid = parseInt(trig[1], 10);
    if (skip.includes(pid)) {
      process.stderr.write(`[!] anti-tamper trigger ${pid} fired again; giving up on reruns\n`);
      break;
    }
    process.stderr.write(`[*] anti-tamper trap reached through function #${pid}; disabling it and re-running\n`);
    skip.push(pid);
  }

  const runText = harness.traceText(body);
  body = harness.p2dMiss(body, cachePath);
  body = body.replace(new RegExp(harness.mark('TRIGGER ') + '\\d+\\n?', 'g'), '');

  const [protosJson, b1] = trace.takeLine(body, 'PROTOS');
  body = b1;
  const [force, b2] = trace.takeLine(body, 'FORCE');
  body = b2;
  if (force && devirtOn) process.stderr.write(`[*] constants decoded on request: ${force}\n`);

  const [unscrambled, b3] = trace.takeLine(body, 'UNSCRAMBLED');
  body = b3;
  if (unscrambled && devirtOn)
    process.stderr.write(`[*] ${unscrambled} function(s) scrambled by LPH_CRASH(): dumped as created\n`);

  const [b4, strings] = trace.takeStrings(body);
  body = b4;

  const notes = skip.length ? [`anti-tamper trap functions disabled: ${skip.map(p => '#' + p).join(', ')}`] : [];
  const text = trace.header(job.input, notes) + body;

  function writeTrace(reason) {
    let out = tidy.tidy(text, { preamble: !args.keepPreamble });
    if (reason) out = TRACE_NOTE + '-- reason: ' + String(reason).replace(/\s+/g, ' ').slice(0, 300) + '\n\n' + out;
    job.write(job.tracePath, out);
  }

  if (!devirtOn && !job.debug) {
    writeTrace();
  }

  if (strings) job.write(job.path('.strings.txt'), strings);

  const dpath = job.path('.devirt.luau');
  let liftBest = null;
  if (protosJson) {
    const ppath = job.path('.protos.json');
    if (protosJson.startsWith('error:')) {
      process.stderr.write(`[!] proto capture failed: ${protosJson}\n`);
    } else {
      job.write(ppath, protosJson);
      if (devirtOn) {
        const chunkPaths = Object.entries(rawChunks).map(([k, src]) =>
          job.write(job.path(`.chunk_${k}.luau`), src, 'latin1')
        );

        const cfgData = {
          input: job.input,
          source: job.source,
          source_path: job.sourcePath,
          trace_path: job.tracePath,
          debug: job.debug,
          obfuscator: job.obfuscator,
          luau_exe: runner.luau,
          patched: patched,
          cfg: cfg,
          chunks: chunks,
          run_text: runText,
          ppath: ppath,
          dpath: dpath,
          chunk_paths: chunkPaths,
          args: {
            budget: args.budget,
            timeout: args.timeout,
            devirt_rounds: args.devirtRounds || 200,
            studio: false,
            no_fold: args.noFold || false,
            strings: args.strings || false,
            executor: args.executor || 'Wave',
          },
        };
        const cfgPath = job.path('.cfg.json');
        fs.writeFileSync(cfgPath, JSON.stringify(cfgData), 'utf8');

        const { execFileSync } = require('child_process');
        const { getPythonBin } = require('./pyenv');
        const pythonBin = getPythonBin();
        const bridgePy = path.join(__dirname, 'devirt_bridge.py');
        const coreDir = path.join(__dirname, '..', 'core');
        // Try each lift engine on the same trace; keep the best result. A clean
        // lift stops the chain, a broken or partial one moves on to the next.
        const engines = liftEngines(job.obfuscator);
        try {
          for (let i = 0; i < engines.length; i++) {
            cfgData.obfuscator = engines[i];
            fs.writeFileSync(cfgPath, JSON.stringify(cfgData), 'utf8');
            try {
              execFileSync(pythonBin, [bridgePy, 'pipeline', cfgPath], {
                env: Object.assign({}, process.env, { PYTHONPATH: coreDir }),
                stdio: 'inherit',
              });
            } catch (e) {
              process.stderr.write(`[!] ${engines[i]} lift process failed: ${String(e.message).split('\n')[0]}\n`);
            }
            if (!fs.existsSync(dpath)) {
              if (i + 1 < engines.length) process.stderr.write(`[*] ${engines[i]} produced nothing; trying ${engines[i + 1]}\n`);
              continue;
            }
            const text = fs.readFileSync(dpath, 'utf8');
            const q = liftQuality(text);
            if (!liftBest || (!q.broken && (liftBest.q.broken || q.score > liftBest.q.score))) {
              liftBest = { label: engines[i], text, q };
            }
            if (!q.broken && q.marks === 0) break;
            if (i + 1 < engines.length) {
              process.stderr.write(`[*] ${engines[i]} lift is ${q.broken ? 'broken' : 'partial (' + q.marks + ' unresolved)'}; ` +
                `trying ${engines[i + 1]}\n`);
              try { fs.unlinkSync(dpath); } catch (e) {}
            }
          }
        } finally {
          try { fs.unlinkSync(cfgPath); } catch (e) {}
        }
        if (liftBest) fs.writeFileSync(dpath, liftBest.text, 'utf8');
      }
    }
  }

  runner.finish();
  trace.statusLine(body);

  let failReason = hooksFailed ? `could not instrument the VM (${hooksFailed})` : 'devirtualization produced no output';

  if (devirtOn && fs.existsSync(dpath)) {
    const lifted = fs.readFileSync(dpath, 'utf8');
    const q = liftQuality(lifted);
    if (!q.broken) {
      if (q.marks > 0) {
        process.stderr.write(`[!] partial devirtualization: ${q.marks} function(s) could not be recovered ` +
          `(marked "unresolved" in the output)\n`);
        fs.writeFileSync(dpath,
          `-- NOTE: partially devirtualized: ${q.marks} function(s) could not be recovered and are marked "unresolved".\n` +
          lifted, 'utf8');
      }
      process.stderr.write('[result] kind=devirt' + (q.marks ? ' partial=' + q.marks : '') + '\n');
      return dpath;
    }
    failReason = `the devirtualized output is broken (${q.nilCalls} calls of nil, ${q.code} code lines)`;
    process.stderr.write(`[!] ${failReason}\n`);
    if (!job.debug) { try { fs.unlinkSync(dpath); } catch (e) {} }
  } else if (devirtOn) {
    process.stderr.write(`[!] ${failReason}\n`);
  }

  if (devirtOn) {
    // A plain-source loadstring() the script made is the real next layer: better than a trace.
    const plain = Object.entries(rawChunks).reverse().find(([, src]) => src && src.trim() && !looksObfuscated(src));
    if (plain) {
      const rpath = job.path('.loadstring_recovered.lua');
      job.write(rpath, '-- Recovered from a runtime-intercepted loadstring() (devirtualization did not complete)\n' +
        `-- chunk: ${plain[0]}, ${Buffer.byteLength(plain[1], 'latin1')} bytes\n\n` + plain[1], 'latin1');
      process.stderr.write('[result] kind=loadstring-payload\n');
      return rpath;
    }
    writeTrace(failReason);
    process.stderr.write('[result] kind=trace reason=' + failReason.replace(/\s+/g, '_') + '\n');
    return job.tracePath;
  }
  return job.tracePath;
}

async function runGeneric(job) {
  const { args } = job;
  const cachePath = harness.loadP2dCache(job.input);
  const runner = new harness.Runner(job);
  const cfg = {
    time_budget: args.budget,
    executor: args.executor,
    dump_strings: args.strings,
  };
  if (args.inputText) cfg.input_text = args.inputText;
  if (args.noFold) cfg.fold = false;
  if (args.cfgJson) Object.assign(cfg, args.cfgJson);

  process.stderr.write(`[*] tracing ${job.input}...\n`);
  const res = await runner.run(job.source, cfg);
  if (!res.body) {
    runner.finish();
    throw new Error(res.err || 'Trace failed without output');
  }
  runner.finish();
  let body = harness.takeP2d(res.body);
  body = harness.p2dMiss(body, cachePath);
  const { body: cleanBody } = harness.takeChunks(body);
  body = cleanBody;
  const [b2, strings] = trace.takeStrings(body);
  body = b2;

  const text = trace.header(job.input) + body;
  job.write(job.tracePath, tidy.tidy(text, { preamble: false }));
  if (strings) job.write(job.path('.strings.txt'), strings);
  trace.statusLine(body);
  return job.tracePath;
}

module.exports = { run, runGeneric };
