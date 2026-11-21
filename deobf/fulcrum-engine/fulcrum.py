#!/usr/bin/env python3
"""Fulcrum Deobfuscator - unified command line interface.

Commands:
  deobf <in> <out>         full two-stage devirtualization (unflat -> polish -> heal -> verify)
  stage1 <in> <out>        stage 1 only: un-flatten the Fulcrum VM to readable Lua
  polish <in> <out>        stage 2 only: constant-fold + rename + heal a stage-1 output
  decrypt <alg> ...        decrypt one O/Q/U/V string cipher blob
  scan <in> [-o r.json]    static analysis report (never executes the input)
  test                     run the decoder self-tests

Static analysis only: no input file is executed and no network access is
performed, except for Fulcrum/PolSec remote-loader files, which are run in
a locked sandbox (stubbed environment, no network, no file io, no process
exec) to recover their handshake and any dynamically compiled source.
"""
import os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable or 'python3'
LUAU_CC = ROOT / 'bin' / 'luau-compile'
ENV = dict(os.environ, LUAU_CC=str(LUAU_CC))


def _run(args, env=None):
    r = subprocess.run(args, cwd=str(ROOT), env=env or ENV,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace')
    if r.returncode != 0:
        sys.stdout.write(r.stdout)
        raise SystemExit('step failed: %s' % ' '.join(map(str, args[:3])))
    return r.stdout


def _stage1(src, dst):
    print('stage 1: un-flat (VM skeleton -> readable Lua) ...')
    _run([PY, 'unflat.py', 'deobf', str(src), str(dst)])
    print('  -> %s (%d lines)' % (dst, _wc(dst)))


def _stage2(src, dst):
    print('stage 2: polish (fold + rename + heal) ...')
    _run([PY, 'polish.py', str(src), str(dst)])
    print('  -> %s (%d lines)' % (dst, _wc(dst)))


def _verify(path):
    if not LUAU_CC.exists():
        print('verify: skipped (bin/luau-compile missing)')
        return None
    r = subprocess.run([str(LUAU_CC), '--binary', str(path)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='replace')
    ok = r.returncode == 0
    print('verify: luau-compile %s' % ('OK, 0 syntax errors' if ok else 'FAILED:\n' + r.stdout[:800]))
    return ok


def _wc(p):
    n = 0
    with open(p, 'rb') as f:
        for _ in f:
            n += 1
    return n


def _looks_polsec_remote(text):
    head = text[:4000]
    return ('obfuscated by fulcrum' in head.lower() or 'polsec' in head.lower()) and 'bit32.bxor' in text


def _polsec_dump(src, dst):
    """PolSec/Fulcrum remote-loader tier: run the file inside a locked luau
    sandbox (stubs for the Roblox env, no file io, no process exec, no real
    network) and recover what is recoverable: any source chunk the loader
    compiles dynamically, plus its runtime handshake."""
    print('polsec VM tier detected: running the sandbox dump harness ...')
    prelude = ROOT / 'polsec_dump_prelude.lua'
    luau = ROOT / 'bin' / 'luau'
    if not prelude.exists() or not luau.exists():
        raise SystemExit('polsec harness missing (prelude or bin/luau)')
    runf = ROOT / '_polsec_run.lua'
    runf.write_text(prelude.read_text(errors='replace') + '\n' +
                    Path(src).read_text(errors='replace'), encoding='utf-8', errors='replace')
    pre = None
    try:
        import resource
        cap = 2 * 1024 * 1024 * 1024

        def _limit():
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
        pre = _limit
    except Exception:
        pre = None
    out = ''
    try:
        r = subprocess.run([str(luau), str(runf)], cwd=str(ROOT),
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, errors='replace', timeout=240, preexec_fn=pre)
        out = r.stdout or ''
    except subprocess.TimeoutExpired as e:
        so = getattr(e, 'stdout', b'') or b''
        out = so.decode('utf-8', 'replace') if isinstance(so, bytes) else str(so or '')
    finally:
        runf.unlink(missing_ok=True)

    lines = out.splitlines()
    payloads = []
    jsons = []
    reqs = []
    logs = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('WOAJ_PAYLOAD_START\t'):
            i += 1
            body = []
            while i < len(lines) and lines[i] != 'WOAJ_PAYLOAD_END':
                body.append(lines[i])
                i += 1
            payloads.append('\n'.join(body))
        elif ln.startswith('WOAJ_JSON\t'):
            jsons.append(ln.split('\t', 1)[1])
        elif ln.startswith('WOAJ_REQ\t'):
            reqs.append(ln.split('\t', 1)[1])
        elif ln.startswith('WOAJ_LOG\t'):
            logs.append(ln.split('\t', 1)[1])
        i += 1
    logs = logs[:60]

    real = [p2 for p2 in payloads if len(p2.strip()) >= 50]
    if real:
        body = []
        for n, p2 in enumerate(real, 1):
            body.append('-- captured source chunk #%d (recovered at runtime by the sandbox dump)' % n)
            body.append(p2)
            body.append('')
        Path(dst).write_text('\n'.join(body), encoding='utf-8', errors='replace')
        print('dumped %d captured source chunk(s) -> %s' % (len(real), dst))
        return

    rep = []
    rep.append('-- Fulcrum deobfuscator result: PolSec remote loader (no embedded script)')
    rep.append('--')
    rep.append('-- This file is not a normal obfuscated script. It is a Fulcrum/PolSec')
    rep.append("-- remote loader: a VM that boots, then asks polsec.net's servers for")
    rep.append('-- the real script at runtime (HWID + key gated). The script code is')
    rep.append('-- NOT inside this file, so no static deobfuscator can recover it.')
    rep.append('-- The file was run inside a locked sandbox (no network, no file io,')
    rep.append('-- no process exec) to recover everything the loader holds locally:')
    rep.append('')
    if jsons:
        rep.append('-- runtime handshake packets recovered:')
        for j in jsons:
            rep.append('--   %s' % j)
        rep.append('')
    if reqs:
        rep.append('-- outbound requests the loader attempted:')
        for q in reqs:
            rep.append('--   %s' % q)
        rep.append('')
    if logs:
        rep.append('-- loader runtime trace:')
        for l in logs:
            rep.append('--   %s' % l)
        rep.append('')
    rep.append('-- To obtain the script itself, the loader has to complete a live')
    rep.append('-- session with the PolSec servers using a valid key; the deobfuscator')
    rep.append('-- never does that on its own.')
    Path(dst).write_text('\n'.join(rep) + '\n', encoding='utf-8', errors='replace')
    print('[!] PolSec remote loader detected: the script itself is NOT inside this file.')
    print("[!] The VM boots and fetches the real script from polsec.net's servers at runtime (HWID + key gated), so no static deobfuscator can recover it.")
    print('[!] Run the loader in Roblox with a valid key, dump the payload it receives, and send that dump to be deobfuscated instead.')
    print('polsec remote loader: no embedded script; recovery report -> %s' % dst)
    raise SystemExit(2)


def cmd_deobf(src, dst):
    tmp = ROOT / '_stage1_out.lua'
    try:
        try:
            _stage1(src, tmp)
        except SystemExit:
            try:
                text = Path(src).read_text(errors='replace')
            except OSError:
                raise
            if _looks_polsec_remote(text):
                _polsec_dump(src, dst)
                return
            raise
        _stage2(tmp, dst)
        _verify(dst)
    finally:
        tmp.unlink(missing_ok=True)
    print('done: %s' % dst)


def cmd_test():
    r = subprocess.run([PY, '-m', 'unittest', '-v', 'test_fulcrum'], cwd=str(ROOT),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace')
    sys.stdout.write(r.stdout)
    raise SystemExit(r.returncode)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ('-h', '--help', 'help'):
        print(__doc__)
        return
    c, rest = a[0], a[1:]
    if c == 'deobf':
        if len(rest) != 2: raise SystemExit('usage: fulcrum.py deobf <in> <out>')
        cmd_deobf(*rest)
    elif c == 'stage1':
        if len(rest) != 2: raise SystemExit('usage: fulcrum.py stage1 <in> <out>')
        _stage1(*rest); _verify(rest[1])
    elif c == 'polish':
        if len(rest) != 2: raise SystemExit('usage: fulcrum.py polish <in> <out>')
        _stage2(*rest); _verify(rest[1])
    elif c == 'decrypt':
        _run([PY, 'fulcrum_deobf.py', *a])
    elif c == 'scan':
        r = subprocess.run([PY, 'fulcrum_deobf.py', *a], cwd=str(ROOT),
                           env=ENV, text=True, errors='replace', capture_output=True)
        sys.stdout.write(r.stdout + r.stderr)
        raise SystemExit(r.returncode)
    elif c == 'test':
        cmd_test()
    else:
        raise SystemExit('unknown command: %s (try fulcrum.py help)' % c)


if __name__ == '__main__':
    main()
