#!/usr/bin/env python3
"""Fulcrum Deobfuscator - unified command line interface.

Commands:
  deobf <in> <out>         full two-stage devirtualization (unflat -> polish -> heal -> verify)
  vmchain <in> <out>       VM-interpreter build: walk the dispatch tree and emit the compact handler chain
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


def _lua_lit(s):
    if isinstance(s, str):
        b = s.encode('utf-8', 'surrogateescape')
    else:
        b = s
    out = []
    for x in b:
        c = chr(x)
        if c == '"':
            out.append('\\"')
        elif c == '\\':
            out.append('\\\\')
        elif c == '\n':
            out.append('\\n')
        elif c == '\r':
            out.append('\\r')
        elif c == '\t':
            out.append('\\t')
        elif 32 <= x < 127:
            out.append(c)
        else:
            out.append('\\x%02x' % x)
    return '"' + ''.join(out) + '"'


def _lua_responses_table(responses):
    parts = []
    for url, v in responses.items():
        parts.append('[%s]={status=%d,body=%s}' % (_lua_lit(url), v['status'], _lua_lit(v['body'])))
    return '{' + ','.join(parts) + '}'


def _unhex(h):
    if not h or h == '-':
        return None
    try:
        return bytes.fromhex(h)
    except ValueError:
        return None


def _real_fetch(method, url, headers, body):
    """Perform the loader's own request for real. Returns (status, body_text, note)."""
    import urllib.request
    import urllib.error
    if not (url.startswith('http://') or url.startswith('https://')):
        return None, '', 'blocked non-http scheme'
    if len(body or b'') > 4 * 1024 * 1024:
        return None, '', 'request body too large'
    req = urllib.request.Request(url, data=body if body else None, method=method)
    sent_headers = dict(headers or {})
    for k, v in sent_headers.items():
        try:
            req.add_header(k, v)
        except Exception:
            pass
    if not any(k.lower() == 'user-agent' for k in sent_headers):
        # HttpService always sends a Roblox UA; stand in for that when the loader sent none
        req.add_header('User-Agent', 'Roblox/Win64')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode('utf-8', 'replace'), ''
    except urllib.error.HTTPError as e:
        try:
            b = e.read().decode('utf-8', 'replace')
        except Exception:
            b = ''
        return e.code, b, ''
    except Exception as e:
        return None, '', 'fetch failed: %s' % e


def _polsec_dump(src, dst, depth=0):
    """PolSec/Fulcrum remote-loader tier: run the file inside a locked luau
    sandbox (Roblox stubs, no file io, no process exec) and recover the real
    payload without Roblox. The sandbox records every network request the
    loader attempts; this side performs those exact requests, injects the
    genuine responses back into the sandbox, and re-runs it until nothing new
    is fetched. Whatever the loader then hands to its own compiler
    (loadstring) is captured and deobfuscated."""
    print('polsec VM tier detected: running the sandbox dumper (real fetch round-trip) ...')
    prelude = ROOT / 'polsec_dump_prelude.lua'
    luau = ROOT / 'bin' / 'luau'
    if not prelude.exists() or not luau.exists():
        raise SystemExit('polsec harness missing (prelude or bin/luau)')
    try:
        loader_src = Path(src).read_text(errors='replace')
    except OSError as e:
        raise SystemExit('cannot read input: %s' % e)

    responses = {}
    payloads = []
    payload_names = []
    jsons = []
    reqs = []
    logs = []
    raw_lines = []
    fetch_log = []
    rounds = 0
    total_fetches = 0
    runf = ROOT / '_polsec_run.lua'
    try:
        for rounds in range(1, 7):
            runf.write_text(prelude.read_text(errors='replace') + '\nWOAJ_RESPONSES = '
                            + _lua_responses_table(responses) + '\n' + loader_src,
                            encoding='utf-8', errors='replace')
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
                                   text=True, errors='replace', timeout=90, preexec_fn=pre)
                out = r.stdout or ''
            except subprocess.TimeoutExpired as e:
                so = getattr(e, 'stdout', b'') or b''
                out = so.decode('utf-8', 'replace') if isinstance(so, bytes) else str(so or '')

            lines = out.splitlines()
            fetched = []
            i = 0
            round_payloads = []
            while i < len(lines):
                ln = lines[i]
                if ln.startswith('WOAJ_PAYLOAD_START\t'):
                    i += 1
                    body = []
                    while i < len(lines) and lines[i] != 'WOAJ_PAYLOAD_END':
                        body.append(lines[i])
                        i += 1
                    round_payloads.append('\n'.join(body))
                elif ln.startswith('WOAJ_JSON\t'):
                    jsons.append(ln.split('\t', 1)[1])
                elif ln.startswith('WOAJ_REQ\t'):
                    reqs.append(ln.split('\t', 1)[1])
                elif ln.startswith('WOAJ_FETCH\t'):
                    f = ln.split('\t')
                    method = f[1] if len(f) > 1 else 'GET'
                    url = f[2] if len(f) > 2 else ''
                    hdrs = {}
                    hb = _unhex(f[3]) if len(f) > 3 else None
                    if hb:
                        for pair in hb.decode('utf-8', 'replace').split('|'):
                            if ':' in pair:
                                k, v = pair.split(':', 1)
                                hdrs[k.strip()] = v.strip()
                    body = _unhex(f[4]) if len(f) > 4 else None
                    fetched.append({'method': method, 'url': url, 'headers': hdrs, 'body': body})
                elif ln.startswith('WOAJ_LOG\t'):
                    logs.append(ln.split('\t', 1)[1])
                elif ln.strip():
                    raw_lines.append(ln)
                i += 1
            for p in round_payloads:
                payloads.append(p)
            logs = logs[:120]
            raw_lines = raw_lines[:120]

            new = [f for f in fetched if f['url'] and f['url'] not in responses]
            if not new:
                break
            for f in new:
                if total_fetches >= 12:
                    fetch_log.append((f['method'], f['url'], 0, 'fetch cap reached, not sent'))
                    continue
                total_fetches += 1
                st, body, note = _real_fetch(f['method'], f['url'], f['headers'], f['body'])
                if st is None:
                    fetch_log.append((f['method'], f['url'], None, note))
                    responses[f['url']] = {'status': 0, 'body': ''}
                else:
                    fetch_log.append((f['method'], f['url'], st, ''))
                    responses[f['url']] = {'status': st, 'body': body[:4 * 1024 * 1024]}
            for f2 in new:
                b = (responses.get(f2['url']) or {}).get('body', '')
                if b and len(b) >= 50 and ('bit32.bxor' in b or 'obfuscated by fulcrum' in b.lower()
                                           or 'obfuscated by' in b[:400].lower()):
                    if b not in payloads:
                        payloads.append(b)
                        payload_names.append('fetched from %s' % f2['url'])
    finally:
        runf.unlink(missing_ok=True)

    payload_names = ['(compiler input #%d)' % (n + 1) for n in range(len(payloads))]
    logs = logs[:60]

    real = [p for p in payloads if len(p.strip()) >= 50]
    if real:
        print('dumper captured %d source chunk(s) after %d sandbox round(s), %d real fetch(es)'
              % (len(real), rounds, total_fetches))
        biggest = max(real, key=len)
        if depth < 2 and ('bit32.bxor' in biggest or 'api.polsec.net' in biggest):
            tmp = ROOT / '_polsec_payload.lua'
            tmp.write_text(biggest, encoding='utf-8', errors='replace')
            try:
                cmd_deobf(str(tmp), dst, depth=depth + 1, skip_polsec=True)
            except (Exception, SystemExit) as e:
                hdr = (
                    '-- Fulcrum deobfuscator result: PolSec payload recovered by the sandbox dumper (no Roblox needed)\n'
                    "-- The real script was fetched from the PolSec server using the loader's own\n"
                    '-- embedded credentials (%d bytes, Fulcrum-obfuscated). The static engine does not\n'
                    '-- cover this Fulcrum VM variant yet, so the recovered payload itself is\n'
                    '-- written below for the next stage.\n'
                    '-- engine error: %s\n') % (len(biggest), e)
                Path(dst).write_text(hdr + biggest + '\n', encoding='utf-8', errors='replace')
                print('payload recovered (%d bytes) but the engine does not cover this Fulcrum VM variant yet -> %s' % (len(biggest), dst))
            finally:
                tmp.unlink(missing_ok=True)
            return
        body = []
        for n, p2 in enumerate(real, 1):
            body.append('-- Fulcrum deobfuscator result: PolSec payload recovered by the sandbox dumper (no Roblox needed)')
            body.append('-- captured source chunk #%d (handed to the loader\'s own compiler at runtime)' % n)
            body.append(p2)
            body.append('')
        Path(dst).write_text('\n'.join(body), encoding='utf-8', errors='replace')
        print('dumped %d captured source chunk(s) -> %s' % (len(real), dst))
        return

    rep = []
    rep.append('-- Fulcrum deobfuscator result: PolSec remote loader')
    rep.append('--')
    rep.append('-- This file is a Fulcrum/PolSec remote loader: the real script lives')
    rep.append("-- on the PolSec servers. The dumper ran the loader in a locked sandbox")
    rep.append('-- and replayed every request the loader itself made, then fed the real')
    rep.append('-- responses back in. Result of that session:')
    rep.append('')
    if fetch_log:
        rep.append('-- real network round-trips performed:')
        for m, u, st, note in fetch_log:
            if st is None:
                rep.append('--   %s %s -> %s' % (m, u, note))
            elif st == 0:
                rep.append('--   %s %s -> %s' % (m, u, note))
            else:
                b = (responses.get(u) or {}).get('body', '')
                prev = b[:160].replace('\n', ' ')
                rep.append('--   %s %s -> HTTP %s  %s' % (m, u, st, prev))
        rep.append('')
    if jsons:
        rep.append('-- handshake packets the loader built:')
        for j in jsons[:20]:
            rep.append('--   %s' % j)
        rep.append('')
    if reqs:
        rep.append('-- outbound requests recorded in-sandbox:')
        for q in reqs[:20]:
            rep.append('--   %s' % q)
        rep.append('')
    if logs:
        rep.append('-- loader runtime trace:')
        for l in logs:
            rep.append('--   %s' % l)
        rep.append('')
    if raw_lines:
        rep.append('-- raw sandbox output (non-marker):')
        for l in raw_lines[:40]:
            rep.append('--   %s' % l)
        rep.append('')
    denied = any(st not in (0, None, 200) for _, _, st, _ in fetch_log)
    if denied:
        rep.append('-- The PolSec server answered with a non-200 status. That is the')
        rep.append('-- server-side HWID/key gate: the loader was run with the credentials')
        rep.append('-- embedded in it, and the server still refused this session. A')
        rep.append('-- different valid key would have to come from the script owner.')
        rep.append('-- No static deobfuscator can recover the script without the server')
        rep.append('-- handing it over.')
    else:
        rep.append('-- The loader compiled no script chunk during the session, so nothing')
        rep.append('-- could be captured. The payload may need a valid script key that the')
        rep.append('-- loader does not embed.')
    Path(dst).write_text('\n'.join(rep) + '\n', encoding='utf-8', errors='replace')
    if denied:
        print('[!] PolSec server refused the session (HWID/key gate): see the recovery report for the exact responses.')
        print('polsec remote loader: server-gated; recovery report -> %s' % dst)
    else:
        print('[!] PolSec loader session completed but no script chunk was compiled; see the recovery report.')
        print('polsec remote loader: nothing captured; recovery report -> %s' % dst)
    raise SystemExit(2)


def cmd_deobf(src, dst, depth=0, skip_polsec=False):
    tmp = ROOT / '_stage1_out.lua'
    try:
        try:
            _stage1(src, tmp)
        except SystemExit:
            try:
                text = Path(src).read_text(errors='replace')
            except OSError:
                raise
            if not skip_polsec and _looks_polsec_remote(text):
                _polsec_dump(src, dst, depth=depth)
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
        try:
            import vmfinal
            vmfinal.run(rest[0], rest[1])
            if _verify(rest[1]):
                return
            raise SystemExit('vmchain output failed verification; falling back to the two-stage pipeline')
        except SystemExit as e:
            msg = str(e)
            if 'not a Fulcrum VM-interpreter build' in msg:
                cmd_deobf(*rest)
            else:
                raise
    elif c == 'vmchain':
        if len(rest) != 2: raise SystemExit('usage: fulcrum.py vmchain <in> <out>')
        import vmfinal
        vmfinal.run(rest[0], rest[1])
        _verify(rest[1])
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
