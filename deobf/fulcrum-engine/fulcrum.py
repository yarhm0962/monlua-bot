#!/usr/bin/env python3
"""Fulcrum Deobfuscator - unified command line interface.

Commands:
  deobf <in> <out>         full two-stage devirtualization (unflat -> polish -> heal -> verify)
  stage1 <in> <out>        stage 1 only: un-flatten the Fulcrum VM to readable Lua
  polish <in> <out>        stage 2 only: constant-fold + rename + heal a stage-1 output
  decrypt <alg> ...        decrypt one O/Q/U/V string cipher blob
  scan <in> [-o r.json]    static analysis report (never executes the input)
  test                     run the decoder self-tests

Everything is static analysis: no input file is ever executed and no
network access is performed.
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


def cmd_deobf(src, dst):
    tmp = ROOT / '_stage1_out.lua'
    try:
        _stage1(src, tmp)
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
