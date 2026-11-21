#!/usr/bin/env python3
"""luavalid.py — syntax-validate chain output that mixes Luau if-expressions
with Lua 5.4 goto labels. Rewrites if-expressions into equivalent function
calls (validation only) and feeds the result to luaparser (Lua 5.3).
Usage: python3 luavalid.py <file.lua>  -> prints PARSE OK / errors."""
import sys
from vmstmt import toks2, skip_exprif
from luaparser import ast


def exprif_spans(toks):
    """All if-expr token spans [(i, j_end)] including nested, j_end exclusive."""
    spans = []
    i = 0
    n = len(toks)
    guard = 0
    while i < n and guard < 200000:
        guard += 1
        t = toks[i]
        if t.w == 'if-expr':
            j = skip_exprif(toks, i)
            if j is None or j <= i:
                i += 1
                continue
            spans.append((i, j))
            i = j
        else:
            i += 1
    return spans


def split3(text, toks, i, j_end):
    """Return (cond_txt, a_txt, b_txt) for the if-expr at toks[i..j_end)."""
    s_tok, e_tok = toks[i], toks[j_end - 1]
    base = text
    # find 'then' at depth 0
    pd = 0
    then_i = None
    for k in range(i, j_end):
        w = toks[k].w
        if w in ('(', '[', '{'):
            pd += 1
        elif w in (')', ']', '}'):
            pd = max(0, pd - 1)
        elif w == 'then' and pd == 0:
            then_i = k
            break
    if then_i is None:
        return None
    pd = 0
    else_i = None
    for k in range(then_i + 1, j_end):
        w = toks[k].w
        if w in ('(', '[', '{'):
            pd += 1
        elif w in (')', ']', '}'):
            pd = max(0, pd - 1)
        elif w == 'else' and pd == 0:
            else_i = k
            break
    if else_i is None:
        return None
    cond = base[toks[i].e:toks[then_i].s]
    a = base[toks[then_i].e:toks[else_i].s]
    b = base[toks[else_i].e:toks[j_end - 1].e]
    return cond.strip(), a.strip(), b.strip()


def rewrite(text):
    toks = toks2(text)
    spans = exprif_spans(toks)
    if not spans:
        return text
    # innermost first: sort by start descending (spans nest, never cross)
    out = text
    for i, j_end in sorted(spans, key=lambda p: -p[0]):
        s_tok, e_tok = toks[i], toks[j_end - 1]
        span_s, span_e = s_tok.s, e_tok.e
        got = split3(out, toks, i, j_end)
        if got is None:
            continue
        cond, a, b = got
        repl = '((function() if (%s) then return (%s) else return (%s) end end)())' % (cond, a, b)
        out = out[:span_s] + repl + out[span_e:]
    return out


import re as _re

def neutralize_goto(text):
    text = _re.sub(r'::\s*L\d+\s*::', 'do end', text)
    text = _re.sub(r'\bgoto\s+L\d+', 'do end', text)
    return text

def check(path):
    src = open(path, encoding='utf-8', errors='replace').read()
    rewritten = neutralize_goto(rewrite(src))
    open('/tmp/luavalid_rewritten.lua', 'w').write(rewritten)
    try:
        tree = ast.parse(rewritten)
        return True, 'OK (%d top-level statements)' % len(tree.body.body)
    except Exception as e:
        return False, str(e)[:600]


if __name__ == '__main__':
    ok, msg = check(sys.argv[1])
    print('PARSE ' + ('OK, ' if ok else 'FAIL: ') + msg)
