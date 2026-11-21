#!/usr/bin/env python3
"""vmstmt.py — statement-level plumbing stripper for the PolSec Fulcrum variant.

Channel vars (F,M,q,f,h,s) are dispatcher plumbing: dropped from the body and
returned as ordered events. Register assignments stay in the output but are
value-tracked so channel copies through registers resolve. if-statements are
recursed into; identical branch outcomes fold, differing ones become branch
events the CFG walker turns into real gotos.
"""
import re
from vmwalk2 import tokens
from vmwalk import bxor, decode

CHANNELS = ('F', 'M', 'q', 'f')
PLUMB = set(CHANNELS) | {'h', 's'}

def read_cond(toks, i):
    """toks[i] is the 'if'/'elseif' keyword; return (cond_start, then_start)."""
    sub = []
    j = i + 1
    cs = toks[i].e
    while j < len(toks):
        t = toks[j]; w = t.w
        if w == 'if-expr': sub.append('e')
        elif w == 'if-stmt': sub.append('i')
        elif w in ('function', 'do', 'repeat', 'for', 'while'): sub.append('b')
        elif w == 'else':
            if sub and sub[-1] == 'e': sub.pop()
            elif not sub: return None, None
        elif w in ('end', 'until'):
            if sub: sub.pop()
            else: return None, None
        elif w == 'then':
            if not sub: return cs, t.s
        j += 1
    return None, None

def skip_exprif(toks, i):
    """toks[i] is an 'if-expr' marker; return index of the first token after it."""
    j = i + 1
    pd = 0
    seen_then = False
    seen_else = False
    while j < len(toks):
        t = toks[j]; w = t.w
        if w == 'if-expr':
            j = skip_exprif(toks, j); continue
        if not seen_then:
            if w == 'then' and pd == 0:
                seen_then = True
            elif pd == 0 and w in (';', ',', ')', ']', '}', 'end', 'elseif', 'else', 'do', 'until'):
                return j
        elif not seen_else:
            if w == 'else' and pd == 0:
                seen_else = True
            elif pd == 0 and w in (';', ',', ')', ']', '}', 'end', 'elseif', 'else', 'do', 'until'):
                return j
        else:
            if pd == 0 and w in (';', ',', ')', ']', '}', 'end', 'elseif', 'else', 'do', 'until', 'then'):
                return j
        if w in ('(', '[', '{'):
            pd += 1
        elif w in (')', ']', '}'):
            pd = max(0, pd - 1)
        j += 1
    return j


def toks2(text):
    """tokens() but with punctuation runs split so ';' becomes its own token."""
    out = []
    for t in tokens(text):
        seg = text[t.s:t.e]
        if t.kind != 'str' and ';' in seg and len(seg) > 1:
            pos = t.s
            for m in re.finditer(r'[^;]+|;', seg):
                out.append(TokShim(m.group(0), pos, pos + len(m.group(0)), t.kind))
                pos += len(m.group(0))
        else:
            out.append(t)
    return out


class TokShim:
    __slots__ = ('kind', 's', 'e', 'w')
    def __init__(self, w, s, e, kind):
        self.w = w[:2] if w.strip()[:1].isalpha() and len(w) > 2 and w.strip().isalpha() else w
        self.kind = kind
        self.s = s
        self.e = e

def split_statements(text):
    """Top-level statements cut at ';' (depth 0): [(s, e, stmt)]."""
    out = []
    toks = toks2(text)
    i = 0
    start = 0
    depth = 0
    skip_do = False
    while i < len(toks):
        t = toks[i]; w = t.w
        if w == 'if-expr':
            i = skip_exprif(toks, i); continue
        if w in ('if-stmt', 'for', 'while', 'function', 'repeat', 'do'):
            if w == 'do' and skip_do:
                skip_do = False
            else:
                depth += 1; skip_do = (w in ('for', 'while'))
        elif w in ('end', 'until'):
            if depth > 0:
                depth -= 1
            else:
                out.append((start, t.e, text[start:t.e])); start = t.e
        elif w == ';' and depth == 0:
            out.append((start, t.e, text[start:t.e])); start = t.e
        i += 1
    if start < len(text) and text[start:].strip():
        out.append((start, len(text), text[start:]))
    return out

def split_if_branches(stmt):
    """Return [(cond_text_or_None, body_start, body_end, mark_start, mark_end)]."""
    toks = toks2(stmt)
    if not toks or toks[0].w != 'if-stmt':
        return None
    cs, ce = read_cond(toks, 0)
    if ce is None:
        return None
    branches = []
    body_start = ce + 4
    i = 0
    while i < len(toks) and toks[i].s < body_start:
        i += 1
    depth = 0
    skip_do = False
    cur_start = body_start
    cur_cond = stmt[cs:ce]
    mark = (toks[0].s, toks[0].e)
    while i < len(toks):
        t = toks[i]; w = t.w
        if w == 'if-expr':
            i = skip_exprif(toks, i); continue
        if depth == 0 and w in ('elseif', 'else', 'end'):
            branches.append((cur_cond, cur_start, t.s, mark[0], mark[1]))
            if w == 'end':
                break
            mark = (t.s, t.e)
            if w == 'elseif':
                cs, ce = read_cond(toks, i)
                cur_cond = stmt[cs:ce]
                cur_start = ce + 4
                i += 1
                while i < len(toks) and toks[i].s < cur_start:
                    i += 1
                continue
            else:
                cur_cond = None
                cur_start = t.e
                i += 1
                continue
        if w in ('if-stmt', 'for', 'while', 'function', 'repeat', 'do'):
            if w == 'do' and skip_do:
                skip_do = False
            else:
                depth += 1; skip_do = (w in ('for', 'while'))
        elif w in ('end', 'until'):
            depth -= 1
        i += 1
    return branches

def _sep(a, b):
    if a and b and a[-1] and (a[-1].isalnum() or a[-1] == '_') and (b[0].isalnum() or b[0] == '_'):
        return ' '
    return ''

def rebuild_if(stmt, outs):
    segs = []
    pos = 0
    for cond, b0, b1, m0, m1, cleaned in outs:
        segs.append(stmt[pos:b0]); segs.append(cleaned)
        pos = b1
    segs.append(stmt[pos:])
    out = []
    prev = ''
    for seg in segs:
        if out:
            out.append(_sep(prev, seg))
        out.append(seg)
        prev = seg
    return ''.join(out)

RE_PAIR   = re.compile(r'^\s*([FfqM])\s*,\s*([FfqM])\s*=\s*I\s*\(\s*(\d+)\s*,\s*h\s*\)\s*,\s*I\s*\(\s*(\d+)\s*,\s*h\s*\)\s*$')
RE_FIF    = re.compile(r'^\s*([FfqM])\s*=\s*\(\s*if\s+([A-Za-z_]\w*)\s+then\s+I\s*\(\s*(?:h\s*,\s*(\d+)|(\d+)\s*,\s*h)\s*\)\s*else\s+I\s*\(\s*(?:h\s*,\s*(\d+)|(\d+)\s*,\s*h)\s*\)\s*\)\s*$')
RE_SETKEY = re.compile(r'^\s*([FfqM])\s*=\s*I\s*\(\s*(\d+)\s*,\s*h\s*\)\s*$|^\s*([FfqM])\s*=\s*I\s*\(\s*h\s*,\s*(\d+)\s*\)\s*$')
RE_H      = re.compile(r'^\s*h\s*=\s*(?:\((\d+)\+h\)|\(h\+(\d+)\)|h\+(\d+)|(\d+)\+h|\(\(v\+(\d+)\)-\(v\+(\d+)\)\)\s*)\s*$')
RE_H_ABS  = re.compile(r'^\s*h\s*=\s*(\d+)\s*$')
RE_S      = re.compile(r'^\s*s\s*=\s*(true|false)\s*$')
RE_GATE   = re.compile(r'^\s*if\s+not\s+U\[119\]\s*then\s+continue\s+end\s*$')
RE_COPYC  = re.compile(r'^\s*([FfqM])\s*=\s*([FfqM])\s*$')
RE_COPYV  = re.compile(r'^\s*([FfqM])\s*=\s*([A-Za-z_]\w*)\s*$')
RE_IXK    = re.compile(r'^\s*([A-Za-z_]\w*)\s*=\s*I\s*\(\s*(\d+)\s*,\s*h\s*\)\s*$|^\s*([A-Za-z_]\w*)\s*=\s*I\s*\(\s*h\s*,\s*(\d+)\s*\)\s*$')
RE_IVV    = re.compile(r'^\s*([A-Za-z_]\w*)\s*=\s*I\s*\(\s*([A-Za-z_]\w*)\s*,\s*(\d+)\s*\)\s*$|^\s*([A-Za-z_]\w*)\s*=\s*I\s*\(\s*(\d+)\s*,\s*([A-Za-z_]\w*)\s*\)\s*$')
RE_ICC    = re.compile(r'^\s*([A-Za-z_]\w*)\s*=\s*I\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*$')
RE_ARITHE = re.compile(r'^\s*([A-Za-z_]\w*)\s*=\s*(?:\(?\s*(\d+)\s*\+\s*([A-Za-z_]\w*)\s*\)?|\(?\s*([A-Za-z_]\w*)\s*\+\s*(\d+)\s*\)?)\s*$')
RE_CONST  = re.compile(r'^\s*([A-Za-z_]\w*)\s*=\s*(\d+)\s*$')
RE_SWAP   = re.compile(r'^\s*do\s+local\s+(\w+)\s*;(.+?)end\s*$', re.S)

def classify(stq, events, vals):
    """Classify one statement; True if it is plumbing (consumed)."""
    m = RE_PAIR.match(stq)
    if m:
        events.append(('set2', m.group(1), int(m.group(3)), m.group(2), int(m.group(4)))); return True
    m = RE_FIF.match(stq)
    if m:
        var, cond = m.group(1), m.group(2)
        a = int(m.group(3) or m.group(4))
        b = int(m.group(5) or m.group(6))
        events.append(('branch', [(cond, [('set', var, a)]), ('not ' + cond, [('set', var, b)])]))
        return True
    m = RE_SETKEY.match(stq)
    if m:
        events.append(('set', m.group(1) or m.group(3), int(m.group(2) or m.group(4)))); return True
    m = RE_H.match(stq)
    if m:
        if m.group(5) is not None:
            events.append(('h_set', int(m.group(5)) - int(m.group(6))))
        else:
            events.append(('h_add', int(m.group(1) or m.group(2) or m.group(3) or m.group(4))))
        return True
    m = RE_H_ABS.match(stq)
    if m:
        events.append(('h_set', int(m.group(1)))); return True
    m = RE_S.match(stq)
    if m:
        events.append(('s', m.group(1) == 'true')); return True
    if RE_GATE.match(stq):
        return True
    m = RE_COPYC.match(stq)
    if m:
        events.append(('copy', m.group(1), m.group(2))); return True
    m = RE_COPYV.match(stq)
    if m:
        src = m.group(2)
        if src in vals:
            events.append(('copyv', m.group(1), src))
        else:
            events.append(('copy_unknown', m.group(1), src))
        return True
    m = RE_ICC.match(stq)
    if m:
        v = bxor(int(m.group(2)), int(m.group(3)))
        if m.group(1) in CHANNELS:
            events.append(('set_chan_num', m.group(1), v))
        else:
            events.append(('setv', m.group(1), ('num', v)))
        return True
    m = RE_IXK.match(stq)
    if m:
        var = m.group(1) or m.group(3)
        k = int(m.group(2) or m.group(4))
        if var in CHANNELS:
            events.append(('set', var, k))
        else:
            events.append(('setv', var, ('xorh', k)))
        return True
    m = RE_IVV.match(stq)
    if m:
        var = m.group(1) or m.group(4)
        src = m.group(2) or m.group(5)
        k = int(m.group(3) or m.group(4))
        if var in CHANNELS:
            events.append(('set_from', var, src, k))
        else:
            events.append(('setv', var, ('xor', src, k)))
        return True
    m = RE_ARITHE.match(stq)
    if m:
        var = m.group(1)
        d = int(m.group(2) or m.group(5))
        if var in CHANNELS:
            events.append(('add', var, d))
        else:
            events.append(('setv', var, ('add', d, m.group(3) or m.group(4))))
        return True
    m = RE_CONST.match(stq)
    if m:
        if m.group(1) in CHANNELS:
            events.append(('set_chan_num', m.group(1), int(m.group(2))))
            return True
        vals[m.group(1)] = int(m.group(2))
        events.append(('setv', m.group(1), ('num', int(m.group(2)))))
        return False
    m = RE_SWAP.match(stq)
    if m:
        body = m.group(2)
        used = set(re.findall(r'\b([A-Za-z_]\w*)\b', body)) - {m.group(1)}
        if used <= PLUMB:
            for a, b, c, d, e2, f2 in re.findall(r'(\w+)=(\w+);(\w+)=(\w+);(\w+)=(\w+)', body):
                events.append(('copy', a, b)); events.append(('copy', c, d)); events.append(('copy', e2, f2))
            return True
    return False

def _is_if_stmt(stmt):
    toks = list(tokens(stmt))
    return bool(toks) and toks[0].w == 'if-stmt'


def split_repeat(stmt):
    """For a top-level repeat statement: return (body_start, body_end, until_cond_text)."""
    toks = toks2(stmt)
    depth = 0
    skip_do = False
    i = 0
    while i < len(toks):
        t = toks[i]; w = t.w
        if w == 'if-expr':
            i = skip_exprif(toks, i); continue
        if w == 'repeat':
            body_start = t.e
            # scan for matching 'until' at this repeat's level
            j = i + 1
            d = 0
            sk = False
            while j < len(toks):
                t2 = toks[j]; w2 = t2.w
                if w2 == 'if-expr':
                    j = skip_exprif(toks, j); continue
                if w2 in ('repeat', 'if-stmt', 'for', 'while', 'function', 'do'):
                    if w2 == 'do' and sk:
                        sk = False
                    else:
                        d += 1; sk = (w2 in ('for', 'while'))
                elif w2 in ('end', 'until'):
                    if d == 0 and w2 == 'until':
                        body_end = t2.s
                        ucond = stmt[t2.e:].strip().rstrip(';').strip()
                        return body_start, body_end, ucond
                    d -= 1
                j += 1
            return None
        i += 1
    return None

def process_body(text, st, vals):
    kept = []
    events = []
    for s, e, stmt in split_statements(text):
        stq = stmt.strip().rstrip(';').strip()
        if not stq:
            continue
        if classify(stq, events, vals):
            continue
        if stmt.lstrip().startswith('repeat'):
            rep = split_repeat(stmt)
            if rep:
                bstart, bend, ucond = rep
                btext, bev = process_body(stmt[bstart:bend], st, dict(vals))
                kept.append('repeat %s until %s -- single-pass exit assumed (flag init true)' % (btext, ucond))
                events.extend(bev)
                continue
        if _is_if_stmt(stmt):
            branches = split_if_branches(stmt)
            if branches:
                outs = []
                for cond, b0, b1, m0, m1 in branches:
                    btext, bev = process_body(stmt[b0:b1], st, dict(vals))
                    outs.append((cond, b0, b1, m0, m1, btext, bev))
                succ = []
                for cond, b0, b1, m0, m1, btext, bev in outs:
                    ss = expand_states(bev, dict(st), dict(vals))
                    succ.append(tuple(sorted((str(c), decode(s2)) for c, s2, v2 in ss)))
                kept.append(rebuild_if(stmt, [(c, b0, b1, m0, m1, bt) for c, b0, b1, m0, m1, bt, _ in outs]))
                if len(set(succ)) == 1 and succ[0] is not None and len(succ[0]) == 1:
                    events.extend(outs[0][6])
                else:
                    events.append(('branch', [(c, bev) for c, _, _, _, _, _, bev in outs]))
            else:
                kept.append(stmt)
        else:
            kept.append(stmt)
    kept = [k.strip().rstrip(';').strip() for k in kept if k.strip()]
    return '; '.join(kept), events

# expand_states imported late to avoid a circular import (vmwalk imports vmstmt lazily)
from vmwalk import expand_states
