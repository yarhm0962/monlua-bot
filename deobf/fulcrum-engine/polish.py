#!/usr/bin/env python3
"""polish.py — mechanical quality pass for the unflat.py output.

Stages (all deterministic):
  1. strip tool traces and plumbing (flags, base/shadow/dispatch regs, shuffle temps)
  2. local constant-propagation: substitute alias values, fold expressions,
     evaluate remaining O/Q/U/V decrypt calls to string literals
  3. drop dead assignments (lhs never referenced again in its scope)
  4. rename identifiers by inferred type with counters (s*/n*/t*/f*/v*)
  5. format: tabs, blank lines between blocks; flatten the aY wrapper

Usage: python3 polish.py in.lua out.lua
"""
import json
import re
import warnings
warnings.simplefilter("ignore", SyntaxWarning)
import sys

sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import unflat
from unflat import Sym, sym_const, fold_expr, fulcrum_decrypt, lua_quote, canon_name

DEC = {'bZ': 'U', 'cb': 'Q', 'cc': 'O', 'ce': 'V'}

PLUMB_EXACT = {'cB = true', 'local dN', 'cB=true'}
PLUMB_NAMES = {'cA', 'cB', 'cC', 'dC', 'dE', 'dG', 'dJ', 'dL', 'dN', 'fD', 'fF', 'fG', 'fJ', 'fs', 'fI', 'fr'}


def is_plumbing(line):
    st = line.strip()
    if st in PLUMB_EXACT:
        return True
    m = re.match(r'^local\s+(dN)\s*$', st)
    if m:
        return True
    m = re.match(r'^([A-Za-z_]\w*(?:\[\d+\])*)\s*=\s*(.+)$', st)
    if m:
        lhs = m.group(1)
        base = lhs.split('[')[0]
        if base in PLUMB_NAMES and not re.match(r'^[A-Za-z_]', m.group(2).strip()[:1] or 'x'):
            return True
        if base in PLUMB_NAMES:
            return True
    return False


def strip_traces(lines):
    out = []
    for l in lines:
        st = l.strip()
        if st.startswith('-- warn:') or st.startswith('-- region end') or st.startswith('-- REGION'):
            continue
        if st.startswith('-- nested function body'):
            continue
        if st.startswith('-- deobfuscated by') or st.startswith('-- O/Q/U/V') or st.startswith('-- Fulcrum'):
            continue
        if st == '' and out and out[-1] == '':
            continue
        out.append(l)
    return out


ASSIGN_RE = re.compile(r'^(\t*)([A-Za-z_]\w*(?:\[\d+\])*)\s*=\s*(.+)$')


def propagate(lines):
    """Fold simple assignments left-to-right; substitute known aliases; decrypt calls."""
    store = {}
    out = []
    for l in lines:
        st = l.strip()
        m = ASSIGN_RE.match(l)
        if m and not st.startswith('local '):
            indent, lhs, rhs = m.group(1), m.group(2), m.group(3).strip()
            # decrypt call?  NAME(arg1,arg2,arg3) with store-resolvable args
            dm = re.match(r'^([A-Za-z_]\w*)\s*\((.+)\)\s*$', rhs, re.S)
            if dm and dm.group(1) in DEC:
                new_rhs = try_decrypt(dm.group(1), dm.group(2), store)
                if new_rhs is not None:
                    rhs = new_rhs
            v = None
            try:
                v = fold_expr(rhs, store)
            except Exception:
                pass
            if v is not None and v.kind == 'str':
                rhs = lua_quote(v.val)
                v = Sym('str', v.val)
            elif v is not None and v.kind == 'int':
                rhs = str(v.val)
            if v is not None and v.kind in ('str', 'int', 'bool', 'list', 'fn'):
                key = canon_name(lhs) or lhs
                store[key] = v
            else:
                key = canon_name(lhs) or lhs
                if key in store:
                    del store[key]
            # substitute aliases in the rhs text for display
            rhs2 = rhs
            for name, val in sorted(store.items(), key=lambda kv: -len(kv[0])):
                if val.kind == 'str' and re.search(r'\b' + re.escape(name) + r'\b', rhs2):
                    rhs2 = re.sub(r'\b' + re.escape(name) + r'\b', lambda m, q=lua_quote(val.val): q, rhs2)
                elif val.kind == 'int' and re.search(r'\b' + re.escape(name) + r'\b', rhs2):
                    rhs2 = re.sub(r'\b' + re.escape(name) + r'\b', lambda m, q=str(val.val): q, rhs2)
            out.append(indent + lhs + ' = ' + rhs2)
            continue
        out.append(l)
    return out


def try_decrypt(fn, argstext, store):
    """Resolve (data, key, seed) from store and run the cipher; return quoted str or None."""
    try:
        args = split_args(argstext)
        if len(args) != 3:
            return None
        vals = []
        for a in args:
            a = a.strip()
            v = fold_expr(a, store)
            vals.append(v)
        data, key, seed = vals
        if data.kind == 'list' and key.kind == 'list' and seed.kind == 'int':
            d = [x.val if isinstance(x, Sym) else None for x in data.val]
            k = [x.val if isinstance(x, Sym) else None for x in key.val]
            if all(isinstance(x, int) for x in d + k) and len(k) == 5:
                pt = fulcrum_decrypt(DEC[fn], d, k, seed.val)
                try:
                    s = pt.decode('utf-8')
                except UnicodeDecodeError:
                    s = pt.decode('latin-1')
                    try:
                        s = s.encode('latin-1').decode('utf-8')
                    except Exception:
                        pass
                return lua_quote(s)
    except Exception:
        return None
    return None


def split_args(text):
    out = []
    depth = 0
    cur = ''
    instr = None
    for ch in text:
        if instr:
            cur += ch
            if ch == instr:
                instr = None
            continue
        if ch in '"\'':
            instr = ch
            cur += ch
            continue
        if ch in '({[':
            depth += 1
        elif ch in ')}]':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(cur)
            cur = ''
            continue
        cur += ch
    if cur.strip():
        out.append(cur)
    return out


def inline_decrypt(lines):
    """Replace cipher calls appearing inside larger expressions with literals."""
    call_re = re.compile(r'\b(bZ|cb|cc|ce)\s*\(')
    out = []
    for l in lines:
        if not call_re.search(l):
            out.append(l)
            continue
        changed = True
        guard = 0
        while changed and guard < 20:
            changed = False
            guard += 1
            m = call_re.search(l)
            while m:
                fn = m.group(1)
                # find the matching close paren
                depth = 0
                j = m.end() - 1
                instr = None
                while j < len(l):
                    ch = l[j]
                    if instr:
                        if ch == instr:
                            instr = None
                    elif ch == chr(34) or ch == chr(39):
                        instr = ch
                    elif ch == '(':
                        depth += 1
                    elif ch == ')':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                if j >= len(l):
                    break
                args = l[m.end():j]
                repl = try_decrypt(fn, args, {})
                if repl is None:
                    # try with a minimal store built from sibling assignments is not
                    # available here; leave the call
                    break
                l = l[:m.start()] + repl + l[j + 1:]
                changed = True
                m = call_re.search(l)
        out.append(l)
    return out



# ---------------- deep readability engine ----------------

MARKER_RE = re.compile(r'^\s*--\s*(PARSE ERROR|for-dispatch|sub-region|region end|UNPARSED|walk error|giant|nested decompile|Traceback|File "|NameError|Traceback|  )')


def strip_markers(lines):
    out = []
    for l in lines:
        if MARKER_RE.match(l):
            continue
        out.append(l)
    return out


_STRMASK = re.compile("\"(?:[^\"\\\\]|\\\\.)*\"|'(?:[^'\\\\]|\\\\.)*'")


def _mask_strings(text):
    parts = []
    def sub(m):
        parts.append(m.group(0))
        return '\x00S%d\x00' % (len(parts) - 1)
    return _STRMASK.sub(sub, text), parts


def _unmask_strings(text, parts):
    for i, p in enumerate(parts):
        text = text.replace('\x00S%d\x00' % i, p)
    return text


_SUBARITH = re.compile(r'\[([\d\s+\-*/()]+)\]')


def _fold_subs_text(text):
    def rep(m):
        try:
            return '[%d]' % int(eval(m.group(1), {'__builtins__': {}}))
        except Exception:
            return m.group(0)
    return _SUBARITH.sub(rep, text)


def _parse_path(expr):
    m = re.match(r'^([A-Za-z_]\w*)((?:\[\d+\])*)$', expr.strip())
    if not m:
        return None
    path = [m.group(1)]
    for n in re.findall(r'\[(\d+)\]', m.group(2)):
        path.append(int(n))
    return tuple(path)


def _looks_simple(expr):
    e = expr.strip()
    if re.match(r'^-?\d+(\.\d+)?$', e):
        return True
    if re.match(r'^(true|false|nil)$', e):
        return True
    if _STRMASK.fullmatch(e):
        return True
    if re.match(r'^[A-Za-z_]\w*$', e):
        return True
    return False


def _fold_condexpr(text, env):
    """Fold (if COND then A else B) when COND is a literal. PAREN-AWARE:
    branches may contain balanced parens and jammed 'else(' forms."""
    def kw_at(buf, k, kw):
        if not buf.startswith(kw, k):
            return False
        after = buf[k + len(kw):k + len(kw) + 1]
        return not (after.isalnum() or after == '_')
    changed = True
    guard = 0
    while changed and guard < 16:
        changed = False
        guard += 1
        i = 0
        n = len(text)
        while i < n - 3:
            if text[i] == '(' and kw_at(text, i + 1, 'if') and (text[i + 3] in ' \t\n'):
                depth = 0
                j = i
                while j < n:
                    ch = text[j]
                    if ch == '(':
                        depth += 1
                    elif ch == ')':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                if j >= n:
                    i += 1
                    continue
                inner = text[i + 1:j]
                depth2 = 0
                k = 0
                then_at = else_at = -1
                while k < len(inner):
                    ch = inner[k]
                    if ch == '(':
                        depth2 += 1
                    elif ch == ')':
                        depth2 -= 1
                    elif depth2 == 0:
                        if then_at < 0 and kw_at(inner, k, 'then'):
                            then_at = k
                            k += 4
                            continue
                        if then_at >= 0 and else_at < 0 and kw_at(inner, k, 'else'):
                            else_at = k
                            k += 4
                            continue
                    k += 1
                if then_at < 0 or else_at < 0:
                    i += 1
                    continue
                cond = inner[2:then_at]
                b_then = inner[then_at + 4:else_at]
                b_else = inner[else_at + 4:]
                c = _fold_simple_masked(cond, env)
                cs = c.strip()
                if cs == 'true' or cs == 'false':
                    repl = b_then if cs == 'true' else b_else
                    text = text[:i] + ' ' + repl + ' ' + text[j + 1:]
                    changed = True
                    break
                i = j + 1
                continue
            i += 1
    return text


def _fold_simple_masked(masked, env):
    """Substitute known cells/vars and fold arithmetic on MASKED text -> MASKED text."""
    masked = _fold_condexpr(masked, env)
    def sub_path(m):
        raw = m.group(0)
        path = _parse_path(raw)
        if path and path in env:
            return env[path]
        return raw
    def sub_path2(m):
        raw = m.group(0)
        nxt = masked[m.end():m.end() + 1]
        path = _parse_path(raw)
        if path and path in env:
            val = env[path]
            # never splice a table literal or non-name into base/arg positions
            if val.startswith('{'):
                return raw
            if nxt in ('[', '(') and (val in ('nil', 'true', 'false') or not re.match(r'^[A-Za-z_]\w*$', val)):
                return raw
            return val
        return raw
    def _fold_sub(m):
        try:
            return '[%d]' % int(eval(m.group(1), {'__builtins__': {}}))
        except Exception:
            return m.group(0)
    masked = re.sub(r'\[(-?\d+\s*[+\-*/]\s*[\d\s+\-*/()]+)\]', _fold_sub, masked)
    masked2 = re.sub(r'[A-Za-z_]\w*(?:\[\d+\])*', sub_path2, masked)
    masked2 = re.sub(r'(?<![\w\]])(?:nil|true|false|\d+|\x00S\d+\x00)\s*[=!]=\s*nil',
                     lambda m: 'false' if '==' in m.group(0) else 'true', masked2)
    masked2 = re.sub(r'(?<![\w\]])(?:nil|true|false|\d+|\x00S\d+\x00)\s*[=!]=\s*nil',
                     lambda m: 'false' if '==' in m.group(0) else 'true', masked2)
    try:
        import unflat
        v = unflat.fold_expr(masked2, {})
        if v.kind == 'int':
            out = str(v.val)
        elif v.kind == 'bool':
            out = 'true' if v.val else 'false'
        elif v.kind == 'nil':
            out = 'nil'
        else:
            out = masked2.strip()
    except Exception:
        out = masked2.strip()
    return out


_KEYWORD_LINE = re.compile(r'^(end|else|elseif|until|then|do|break|and|or|not)\s*$')


def _split_top_assign(text):
    """Split 'lhs = rhs' at a top-level single '='; returns (lhs, rhs) or None."""
    depth = 0
    instr = None
    i = 0
    while i < len(text):
        ch = text[i]
        if instr:
            if ch == '\\':
                i += 2
                continue
            if ch == instr:
                instr = None
        elif ch == '"' or ch == "'":
            instr = ch
        elif ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        elif ch == '=' and depth == 0:
            prev = text[i - 1] if i else ''
            nxt = text[i + 1] if i + 1 < len(text) else ''
            if prev not in '=<>~!' and nxt != '=':
                return text[:i], text[i + 1:]
        i += 1
    return None


def fold_simple(text, env):
    """Public: raw text in, raw text out (or None if unchanged)."""
    if _KEYWORD_LINE.match(text.strip()):
        return None
    masked, parts = _mask_strings(text)
    out = _fold_simple_masked(masked, env)
    out = _unmask_strings(out, parts)
    if out != text.strip():
        return out
    return None


def deep_propagate(lines):
    """Cell/alias-level constant propagation with folding and write removal."""
    env = {}
    out = []
    # count writes per lhs path; propagate only single-write cells (branch-safe)
    wcount = {}
    wvals = {}
    _are = re.compile(r'^(local\s+)?([A-Za-z_]\w*)((?:\[\d+\])*)\s*=\s*(.+)$', re.S)
    for l in lines:
        st = l.strip()
        m = _are.match(st)
        if m and not re.match(r'^(function|if|for|while|repeat|return)\b', st):
            p = _parse_path(m.group(2) + m.group(3))
            if p:
                wcount[p] = wcount.get(p, 0) + 1
                rhs0 = m.group(4).strip()
                if re.match(r'^-?\d+(\.\d+)?$', rhs0) or re.match(r'^(true|false|nil)$', rhs0) or _STRMASK.fullmatch(rhs0):
                    wvals.setdefault(p, set()).add(rhs0)

    # branch-aware env: snapshot on block entry, invalidate changed keys on exit
    import copy
    snapshots = []
    changed_in = [set()]
    depth = 0
    _open_re = re.compile(r'\b(function|if|for|while|repeat)\b')
    _do_re = re.compile(r'\bdo\b')

    def _depth_delta(st):
        masked, _ = _mask_strings(st)
        d = len(_open_re.findall(masked))
        if not re.match(r'^(for|while)\b', st.strip()):
            d += len(_do_re.findall(masked))
        d -= len(re.findall(r'\bend\b', masked))
        if re.match(r'^repeat\b', st.strip()) or re.search(r'\buntil\b', masked):
            pass
        return d
    assign_re = re.compile(r'^(local\s+)?([A-Za-z_]\w*)((?:\[\d+\])*)\s*=\s*(.+)$', re.S)
    for l in lines:
        stripped = l.strip()
        if not stripped or stripped.startswith('--'):
            out.append(l)
            continue
        indent = l[:len(l) - len(l.lstrip())]
        dd = _depth_delta(stripped)
        if dd > 0:
            for _ in range(dd):
                snapshots.append(dict(env))
                changed_in.append(set())
            depth += dd
        m = assign_re.match(stripped)
        if m and not re.match(r'^(function|if|for|while|repeat|return)\b', stripped):
            islocal, name, subs, rhs = m.groups()
            lhs_path = _parse_path(name + subs)
            if lhs_path:
                newrhs = rhs.strip()
                for _ in range(8):
                    r = fold_simple(newrhs, env)
                    if r is None:
                        break
                    newrhs = r
                tbl = re.match(r'^\{(.*)\}$', newrhs, re.S)
                if tbl and ',' not in name:
                    body = tbl.group(1)
                    elems = [x.strip() for x in body.split(',')] if body.strip() else []
                    allsimple = all(_looks_simple(el) for el in elems)
                    if allsimple:
                        env[lhs_path] = '{}'
                        for i, el in enumerate(elems, 1):
                            env[lhs_path + (i,)] = el
                        # keep the table write (its elements may be read as a whole)
                        out.append(indent + _fold_subs_text(('local ' if islocal else '') + name + subs + ' = ' + newrhs))
                        continue
                lit = re.match(r'^-?\d+(\.\d+)?$', newrhs) or re.match(r'^(true|false|nil)$', newrhs) or _STRMASK.fullmatch(newrhs)
                if lit:
                    env[lhs_path] = newrhs
                    if depth > 0:
                        changed_in[-1].add(lhs_path)
                    continue  # drop the literal write; reads are substituted
                if _looks_simple(newrhs):
                    env[lhs_path] = newrhs
                    if depth > 0:
                        changed_in[-1].add(lhs_path)
                out.append(indent + _fold_subs_text(('local ' if islocal else '') + name + subs + ' = ' + newrhs))
                continue
        if dd < 0:
            for _ in range(-dd):
                if snapshots:
                    snap = snapshots.pop()
                    chg = changed_in.pop()
                    for k in chg:
                        if k in snap:
                            env[k] = snap[k]
                        else:
                            env.pop(k, None)
                    depth = max(0, depth - 1)
        parts_as = _split_top_assign(stripped)
        if parts_as:
            lhs, rhs = parts_as
            new = rhs
            for _ in range(8):
                r = fold_simple(new, env)
                if r is None:
                    break
                new = r
            out.append(indent + _fold_subs_text(lhs.strip()) + ' = ' + new.strip())
        else:
            new = stripped
            for _ in range(8):
                r = fold_simple(new, env)
                if r is None:
                    break
                new = r
            out.append(indent + new)
    return out


def drop_dead(lines):
    """Backward liveness: drop assignments whose lhs is never read later."""
    used = set()
    keep = [False] * len(lines)
    for i in range(len(lines) - 1, -1, -1):
        l = lines[i]
        st = l.strip()
        m = ASSIGN_RE.match(l)
        is_assign = bool(m) and not st.startswith('local ')
        decl = st.startswith('local ')
        if is_assign:
            lhs = m.group(2)
            base = lhs.split('[')[0]
            rhs = m.group(3)
            if base in used or lhs in used:
                keep[i] = True
                for mm in re.finditer(r'[A-Za-z_]\w*', rhs):
                    used.add(mm.group(0))
            else:
                keep[i] = False
            continue
        if decl:
            names = re.findall(r'[A-Za-z_]\w*', st[6:])
            rhs_part = st.split('=', 1)[1] if '=' in st else ''
            live = any(n in used for n in names if n != 'local')
            if live:
                keep[i] = True
                for mm in re.finditer(r'[A-Za-z_]\w*', rhs_part):
                    used.add(mm.group(0))
            else:
                keep[i] = False
            continue
        keep[i] = True
        for mm in re.finditer(r'[A-Za-z_]\w*', l):
            used.add(mm.group(0))
    return [l for i, l in enumerate(lines) if keep[i]]


def drop_shuffles(lines):
    """Remove register-shuffle preludes: 'local a,b,c=X,Y,Z' followed by permutes."""
    out = []
    i = 0
    while i < len(lines):
        st = lines[i].strip()
        m = re.match(r'^local\s+([A-Za-z_]\w*(?:\[\d+\])*\s*,\s*)+[A-Za-z_]\w*(?:\[\d+\])*\s*=', st)
        if m and i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            # shuffle body: x[y]=z  or  x=y  permutations
            if re.match(r'^[A-Za-z_]\w*(?:\[\d+\])*\[[A-Za-z_]\w*(?:\[\d+\])*\]\s*=', nxt) or re.match(r'^[A-Za-z_]\w*(?:\[\d+\])*\s*=\s*[A-Za-z_]', nxt):
                # drop the prelude and consecutive permute statements
                i += 1
                while i < len(lines):
                    st2 = lines[i].strip()
                    if re.match(r'^[A-Za-z_]\w*(?:\[\d+\])*(\[[A-Za-z_]\w*(?:\[\d+\])*\])?\s*=', st2):
                        i += 1
                        continue
                    break
                continue
        out.append(lines[i])
        i += 1
    return out


def expand_giants(lines):
    """Splice nested function bodies on giant lines."""
    out = []
    for l in lines:
        if len(l) > 4000 and 'function' in l:
            try:
                out.extend(unflat.splice_fns(l.strip(), {}, 0))
                continue
            except Exception:
                pass
        out.append(l)
    return out


def rename(lines):
    """Type-counter renaming per reference style: s*/n*/t*/f*/v*."""
    kind_of = {}
    for l in lines:
        m = ASSIGN_RE.match(l)
        if not m:
            continue
        lhs, rhs = m.group(2), m.group(3).strip()
        base = lhs.split('[')[0]
        if base in kind_of:
            continue
        if re.match(r'^"[^"]*"$', rhs):
            kind_of[base] = 's'
        elif re.match(r'^-?\d+$', rhs):
            kind_of[base] = 'n'
        elif rhs.startswith('{'):
            kind_of[base] = 't'
        elif 'function' in rhs[:30]:
            kind_of[base] = 'f'
        else:
            kind_of[base] = 'v'
    counters = {}
    mapping = {}
    for base, kind in sorted(kind_of.items()):
        counters[kind] = counters.get(kind, 0) + 1
        mapping[base] = '%s%d' % (kind, counters[kind])
    out = []
    for l in lines:
        def sub(m):
            tok = m.group(0)
            base = tok.split('[')[0]
            if base in ('data', 'key', 'seed', 'length', 'out', 'state'):
                return tok
            return mapping.get(base, base) + tok[len(base):]
        l = re.sub(r'[A-Za-z_]\w*(?:\[\d+\])*', sub, l)
        out.append(l)
    return out


def format_lines(lines):
    out = []
    for l in lines:
        st = l.strip()
        if st.startswith('if ') or st.startswith('for ') or st.startswith('while ') or st.startswith('function') or st.startswith('repeat'):
            if out and out[-1] != '':
                out.append('')
        out.append(l)
    return out


def flatten_wrapper(lines):
    """Unwrap 'local function aY(...) <body> end local aX = aY return aX(...)'."""
    start = None
    endidx = None
    tailidx = None
    for i, l in enumerate(lines):
        st = l.strip()
        if start is None and re.match(r'^local function aY\(', st):
            start = i
        if st == 'local aX = aY':
            tailidx = i
            break
        if st == 'return aX(...)':
            tailidx = i
            break
    if start is not None and tailidx is not None:
        j = tailidx - 1
        while j > start and lines[j].strip() == '':
            j -= 1
        if j > start and lines[j].strip() == 'end':
            endidx = j
    if start is None or endidx is None:
        return [l for l in lines if l.strip() not in ('local aX = aY', 'return aX(...)')]
    out = []
    for i, l in enumerate(lines):
        if i == start or i == endidx:
            continue
        if l.strip() in ('local aX = aY', 'return aX(...)'):
            continue
        if start < i < endidx and l.startswith('\t'):
            l = l[1:]
        out.append(l)
    return out



# ---------------- cipher recognition (O/Q/U/V) ----------------

CIPHER_SIGS = [
    # (regex in body, op name, seed-update b-expr, per-byte value expr)
    (r'\(\(dP\[aT\]-dU\)\*ec\)%256', 'O', 'b', '(data[i] - f) * c'),
    (r'\(dP\[aT\]\*ec-dU\)%256', 'Q', 'b * a', 'data[i] * c - f'),
    (r'\(\(dP\[aT\]\+dU\)\*ec\)%256', 'U', '-b', '(data[i] + f) * c'),
    (r'\(dP\[aT\]\*ec\+dU\)%256', 'V', '-b * a', 'data[i] * c + f'),
]


def _cipher_template(name, bexpr, vexpr):
    return [
        '%s = function(data, key, seed)' % name,
        '\tlocal length = #data',
        '\tif length == 0 then',
        '\t\treturn ""',
        '\tend',
        '\tlocal a, b, c, d, e = key[1], key[2], key[3], key[4], key[5]',
        '\tlocal out = {}',
        '\tfor i = 1, length do',
        '\t\tseed = (seed * a + %s) %% 16777216' % bexpr,
        '\t\tlocal f = seed + (seed // 256) * d + (seed // 65536) * e',
        '\t\tout[i] = string.char((%s) %% 256)' % vexpr,
        '\tend',
        '\treturn table.concat(out)',
        'end',
    ]


def recognize_ciphers(lines):
    """Replace the four flattened cipher state machines with clean sequential code
    when their byte-op signature matches the package's O/Q/U/V ciphers."""
    out = []
    i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r'^(\s*)(\w+) = function\(dP,dQ,dR\)(.*)end\s*$', l.strip())
        if m and 'while true do' in m.group(3):
            body = m.group(3)
            for sig, op, bexpr, vexpr in CIPHER_SIGS:
                if re.search(sig, body):
                    out.extend(_cipher_template(m.group(2), bexpr, vexpr))
                    break
            else:
                out.append(l)
            i += 1
            continue
        out.append(l)
        i += 1
    return out


# ---------------- junk-loop / dead-cell cleanup ----------------

def drop_junk_loops(lines):
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = re.match(r'\s*(?:if\s+)?\(#(\w+)\) < 500000 then\s*$', line)
        if m:
            # gather full block, verify EVERY line is mechanical junk before dropping
            j = i + 1
            body = []
            ok = True
            depth = 1
            while j < n:
                cur = lines[j]
                if cur.strip() in ('while True do', 'for _ = 1, 0 do'):
                    depth += 1
                    body.append(cur)
                elif cur.strip() in ('end', 'until true'):
                    depth -= 1
                    body.append(cur)
                    if depth == 0:
                        break
                else:
                    body.append(cur)
                j += 1
            if depth != 0 or j >= n:
                out.append(line)
                i += 1
                continue
            inner = [b for b in body[:-1]]
            junk = 0
            for bl in inner:
                if re.match(r'\s*local\s+\w+\s*=', bl) or re.match(r'\s*\w+ = ', bl):
                    if 'function' in bl or '(' in bl:
                        ok = False
                        break
                    junk += 1
                elif bl.strip() in ('while True do', 'for _ = 1, 0 do', 'end', 'until true', ''):
                    pass
                else:
                    ok = False
                    break
            if ok and junk > 0:
                i = j + 1
                continue
            out.append(line)
            i += 1
            continue
        out.append(line)
        i += 1
    return out


def drop_dead(lines):
    """Backward liveness: drop assignments whose lhs is never read later."""
    used = set()
    keep = [False] * len(lines)
    for i in range(len(lines) - 1, -1, -1):
        l = lines[i]
        st = l.strip()
        m = ASSIGN_RE.match(l)
        is_assign = bool(m) and not st.startswith('local ')
        decl = st.startswith('local ')
        if is_assign:
            lhs = m.group(2)
            base = lhs.split('[')[0]
            rhs = m.group(3)
            if base in used or lhs in used:
                keep[i] = True
                for mm in re.finditer(r'[A-Za-z_]\w*', rhs):
                    used.add(mm.group(0))
            else:
                keep[i] = False
            continue
        if decl:
            names = re.findall(r'[A-Za-z_]\w*', st[6:])
            rhs_part = st.split('=', 1)[1] if '=' in st else ''
            live = any(n in used for n in names if n != 'local')
            if live:
                keep[i] = True
                for mm in re.finditer(r'[A-Za-z_]\w*', rhs_part):
                    used.add(mm.group(0))
            else:
                keep[i] = False
            continue
        keep[i] = True
        for mm in re.finditer(r'[A-Za-z_]\w*', l):
            used.add(mm.group(0))
    return [l for i, l in enumerate(lines) if keep[i]]


def drop_shuffles(lines):
    """Remove register-shuffle preludes: 'local a,b,c=X,Y,Z' followed by permutes."""
    out = []
    i = 0
    while i < len(lines):
        st = lines[i].strip()
        m = re.match(r'^local\s+([A-Za-z_]\w*(?:\[\d+\])*\s*,\s*)+[A-Za-z_]\w*(?:\[\d+\])*\s*=', st)
        if m and i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            # shuffle body: x[y]=z  or  x=y  permutations
            if re.match(r'^[A-Za-z_]\w*(?:\[\d+\])*\[[A-Za-z_]\w*(?:\[\d+\])*\]\s*=', nxt) or re.match(r'^[A-Za-z_]\w*(?:\[\d+\])*\s*=\s*[A-Za-z_]', nxt):
                # drop the prelude and consecutive permute statements
                i += 1
                while i < len(lines):
                    st2 = lines[i].strip()
                    if re.match(r'^[A-Za-z_]\w*(?:\[\d+\])*(\[[A-Za-z_]\w*(?:\[\d+\])*\])?\s*=', st2):
                        i += 1
                        continue
                    break
                continue
        out.append(lines[i])
        i += 1
    return out


def expand_giants(lines):
    """Splice nested function bodies on giant lines."""
    out = []
    for l in lines:
        if len(l) > 4000 and 'function' in l:
            try:
                out.extend(unflat.splice_fns(l.strip(), {}, 0))
                continue
            except Exception:
                pass
        out.append(l)
    return out


def rename(lines):
    """Type-counter renaming per reference style: s*/n*/t*/f*/v*."""
    kind_of = {}
    for l in lines:
        m = ASSIGN_RE.match(l)
        if not m:
            continue
        lhs, rhs = m.group(2), m.group(3).strip()
        base = lhs.split('[')[0]
        if base in kind_of:
            continue
        if re.match(r'^"[^"]*"$', rhs):
            kind_of[base] = 's'
        elif re.match(r'^-?\d+$', rhs):
            kind_of[base] = 'n'
        elif rhs.startswith('{'):
            kind_of[base] = 't'
        elif 'function' in rhs[:30]:
            kind_of[base] = 'f'
        else:
            kind_of[base] = 'v'
    counters = {}
    mapping = {}
    for base, kind in sorted(kind_of.items()):
        counters[kind] = counters.get(kind, 0) + 1
        mapping[base] = '%s%d' % (kind, counters[kind])
    out = []
    for l in lines:
        def sub(m):
            tok = m.group(0)
            base = tok.split('[')[0]
            if base in ('data', 'key', 'seed', 'length', 'out', 'state'):
                return tok
            return mapping.get(base, base) + tok[len(base):]
        l = re.sub(r'[A-Za-z_]\w*(?:\[\d+\])*', sub, l)
        out.append(l)
    return out


def format_lines(lines):
    out = []
    for l in lines:
        st = l.strip()
        if st.startswith('if ') or st.startswith('for ') or st.startswith('while ') or st.startswith('function') or st.startswith('repeat'):
            if out and out[-1] != '':
                out.append('')
        out.append(l)
    return out


def flatten_wrapper(lines):
    """Unwrap 'local function aY(...) <body> end local aX = aY return aX(...)'."""
    start = None
    endidx = None
    tailidx = None
    for i, l in enumerate(lines):
        st = l.strip()
        if start is None and re.match(r'^local function aY\(', st):
            start = i
        if st == 'local aX = aY':
            tailidx = i
            break
        if st == 'return aX(...)':
            tailidx = i
            break
    if start is not None and tailidx is not None:
        j = tailidx - 1
        while j > start and lines[j].strip() == '':
            j -= 1
        if j > start and lines[j].strip() == 'end':
            endidx = j
    if start is None or endidx is None:
        return [l for l in lines if l.strip() not in ('local aX = aY', 'return aX(...)')]
    out = []
    for i, l in enumerate(lines):
        if i == start or i == endidx:
            continue
        if l.strip() in ('local aX = aY', 'return aX(...)'):
            continue
        if start < i < endidx and l.startswith('\t'):
            l = l[1:]
        out.append(l)
    return out



# ---------------- cipher recognition (O/Q/U/V) ----------------

CIPHER_SIGS = [
    # (regex in body, op name, seed-update b-expr, per-byte value expr)
    (r'\(\(dP\[aT\]-dU\)\*ec\)%256', 'O', 'b', '(data[i] - f) * c'),
    (r'\(dP\[aT\]\*ec-dU\)%256', 'Q', 'b * a', 'data[i] * c - f'),
    (r'\(\(dP\[aT\]\+dU\)\*ec\)%256', 'U', '-b', '(data[i] + f) * c'),
    (r'\(dP\[aT\]\*ec\+dU\)%256', 'V', '-b * a', 'data[i] * c + f'),
]


def _cipher_template(name, bexpr, vexpr):
    return [
        '%s = function(data, key, seed)' % name,
        '\tlocal length = #data',
        '\tif length == 0 then',
        '\t\treturn ""',
        '\tend',
        '\tlocal a, b, c, d, e = key[1], key[2], key[3], key[4], key[5]',
        '\tlocal out = {}',
        '\tfor i = 1, length do',
        '\t\tseed = (seed * a + %s) %% 16777216' % bexpr,
        '\t\tlocal f = seed + (seed // 256) * d + (seed // 65536) * e',
        '\t\tout[i] = string.char((%s) %% 256)' % vexpr,
        '\tend',
        '\treturn table.concat(out)',
        'end',
    ]


def recognize_ciphers(lines):
    """Replace the four flattened cipher state machines with clean sequential code
    when their byte-op signature matches the package's O/Q/U/V ciphers."""
    out = []
    i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r'^(\s*)(\w+) = function\(dP,dQ,dR\)(.*)end\s*$', l.strip())
        if m and 'while true do' in m.group(3):
            body = m.group(3)
            for sig, op, bexpr, vexpr in CIPHER_SIGS:
                if re.search(sig, body):
                    out.extend(_cipher_template(m.group(2), bexpr, vexpr))
                    break
            else:
                out.append(l)
            i += 1
            continue
        out.append(l)
        i += 1
    return out


# ---------------- junk-loop / dead-cell cleanup ----------------

def drop_junk_loops(lines):
    """Drop `while cond do <pure assignments> end` anti-emulation loops."""
    out = []
    i = 0
    while i < len(lines):
        l = lines[i]
        st = l.strip()
        m = re.match(r'^while\s+(.+?)\s*do\s*(.*)\s*end\s*$', st)
        if m:
            body = m.group(2)
            if not re.search(r'\b(return|break|goto|function|\w+\s*\()', body):
                i += 1
                continue
        out.append(l)
        i += 1
    return out


def drop_dead_cells(lines):
    """Backward liveness on full cell tokens (X[1][2]) and bare names."""
    tok_re = re.compile(r'[A-Za-z_]\w*(?:\[\d+\])*')
    live = set()
    out = []
    for l in reversed(lines):
        st = l.strip()
        if not st or st.startswith('--'):
            out.append(l)
            continue
        m = re.match(r'^(local\s+)?([A-Za-z_]\w*(?:\[\d+\])*)\s*=\s*(.+)$', st, re.S)
        keep = True
        if m and not re.match(r'^(function|if|for|while|repeat|return)\b', st):
            lhs = m.group(2)
            rhs = m.group(3)
            if lhs not in live and not re.match(r'^function\b', rhs) and lhs + '(' not in ''.join(lines):
                # drop if lhs never read later (live set from later lines)
                if lhs not in live:
                    keep = False
        if keep:
            out.append(l)
            for t in tok_re.findall(st):
                live.add(t)
        # tokens on dropped lines still bind lhs? lhs not added -> dead
    out.reverse()
    return out


def split_semis(lines):
    """Split ';'-joined statements into separate lines (depth-aware, block-safe)."""
    out = []
    for l in lines:
        st = l
        if l.lstrip().startswith('--'):
            out.append(l)
            continue
        if ';' not in l:
            out.append(l)
            continue
        parts = []
        cur = ''
        depth = 0
        instr = None
        i = 0
        while i < len(st):
            ch = st[i]
            if instr:
                cur += ch
                if ch == '\\':
                    if i + 1 < len(st):
                        cur += st[i + 1]
                    i += 2
                    continue
                if ch == instr:
                    instr = None
            elif ch == '"' or ch == "'":
                instr = ch
                cur += ch
            elif ch in '([{':
                depth += 1
                cur += ch
            elif ch in ')]}':
                depth -= 1
                cur += ch
            elif ch == ';' and depth == 0:
                parts.append(cur)
                cur = ''
            else:
                cur += ch
            i += 1
        parts.append(cur)
        for p in parts:
            if p.strip():
                out.append(p if p.startswith('\t') or l.startswith('\t') else p)
    return out


def strip_machinery(lines):
    """Drop register/pstate machinery statements (pair writes, dispatcher updates)."""
    out = []
    names = "fD|fE|fF|fG|fH|fI|fJ|fK|cA|cB|dJ|dE|dG|fs|fr|dL"
    mach_re = re.compile(r"^(" + names + r")\s*(,\s*(" + names + r")\s*)*=")
    for l in lines:
        st = l.strip()
        m = mach_re.match(st)
        if m:
            rhs = st.split("=", 1)[1] if "=" in st else ""
            if "function" not in rhs and not re.search(r"[A-Za-z_]\w*\s*\(", rhs) and '"' not in rhs and "'" not in rhs:
                continue
        out.append(l)
    return out


def unwrap_repeats(lines):
    """One-shot repeat ... until wrappers: emit the body, drop the machine loop."""
    out = []
    i = 0
    while i < len(lines):
        l = lines[i]
        st = l.strip()
        if re.match(r'^repeat\b', st):
            rest = re.sub(r'^repeat\s*', '', st)
            body = []
            done = False
            if re.search(r'\suntil\s+', rest):
                body.append(re.sub(r'\suntil\s+.*$', '', rest))
                i += 1
                done = True
            else:
                if rest.strip():
                    body.append(rest)
                j = i + 1
                while j < len(lines):
                    stj = lines[j].strip()
                    if re.match(r'^until\b', stj):
                        j += 1
                        done = True
                        break
                    m2 = re.search(r'^(.*)\suntil\s+.*$', stj)
                    if m2 and m2.group(1).strip():
                        body.append(m2.group(1))
                        j += 1
                        done = True
                        break
                    body.append(lines[j])
                    j += 1
                i = j
            if done:
                out.extend(body)
                continue
            out.append(l)
            i += 1
            continue
        if re.match(r'^until\b', st):
            i += 1
            continue
        out.append(l)
        i += 1
    return out




def _mask_strings_cmts(line):
    out = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch in '"\'':
            q = ch
            j = i + 1
            while j < n:
                if line[j] == '\\':
                    j += 2
                    continue
                if line[j] == q:
                    j += 1
                    break
                j += 1
            out.append(' ' * (j - i))
            i = j
        elif ch == '-' and line[i:i+2] == '--':
            out.append(' ' * (n - i))
            i = n
        else:
            out.append(ch)
            i += 1
    return ''.join(out)


def split_blocks(lines):
    """Split giant `if..then if..then..end end else if` chains into
    one-construct-per-line. Never cuts inside parens (if-expressions, IIFE
    args) or strings/comments; never cuts IIFE tail lines."""
    cut_after = ('then', 'do', 'repeat')
    cut_before = ('else', 'elseif', 'until', 'end', 'local', 'return', 'break')
    out = []
    for ln in lines:
        if ln.lstrip().startswith('--'):
            out.append(ln)
            continue
        if 'end end)' in ln or 'end end)(' in ln or re.search(r'\)\s*\(', ln):
            out.append(ln)
            continue
        m = _mask_strings_cmts(ln)
        if len(m) != len(ln):
            out.append(ln)
            continue
        cuts = []
        depth = 0
        i = 0
        n = len(m)
        while i < n:
            ch = m[i]
            if ch in '([{':
                depth += 1
            elif ch in ')]}':
                depth -= 1
            elif depth == 0 and (ch.isalpha() or ch == '_'):
                j = i
                while j < n and (m[j].isalnum() or m[j] == '_'):
                    j += 1
                w = m[i:j]
                if w in cut_after:
                    cuts.append(j)
                elif w in cut_before:
                    cuts.append(i)
                i = j
                continue
            i += 1
        if not cuts:
            out.append(ln)
            continue
        indent = ln[:len(ln) - len(ln.lstrip())]
        prev = 0
        for c in sorted(set(cuts)):
            piece = ln[prev:c].strip()
            if piece:
                out.append(indent + piece if not piece.startswith(indent) or indent == '' else piece)
            prev = c
        piece = ln[prev:].strip()
        if piece:
            out.append(indent + piece if indent else piece)
    return out



def _depth_counts(m2):
    """Count block tokens with paren awareness: `function`/`end`/`repeat` at
    any depth (they balance), but `then`/`do` ONLY at depth 0 (inside parens
    they belong to if-expressions / function bodies)."""
    fn = th = d0 = rep = endc = 0
    depth = 0
    i = 0
    n = len(m2)
    while i < n:
        ch = m2[i]
        if ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        elif ch.isalpha() or ch == '_':
            j = i
            while j < n and (m2[j].isalnum() or m2[j] == '_'):
                j += 1
            w = m2[i:j]
            if w == 'function':
                fn += 1
            elif w == 'end':
                endc += 1
            elif w == 'repeat':
                rep += 1
            elif w == 'then' and depth == 0:
                th += 1
            elif w == 'do' and depth == 0:
                d0 += 1
            i = j
            continue
        i += 1
    return fn, th, d0, rep, endc



def repair_structure(lines):
    """Balance `end`-counters by deleting truly extra closers and appending
    missing ones. Counts inline `do ... end` pairs on one line correctly."""
    def net(line):
        st = _mask_strings_cmts(line)
        # inline one-line do-blocks are self-balanced
        st2 = re.sub(r'\bdo\b[^\n]*?\bend\b', '', st)
        n = 0
        n += len(re.findall(r'(?<![\w.:])function(?![\w.:])', st2))
        n += len(re.findall(r'(?<![\w.:(])if(?![\w.:])', st2))
        n += len(re.findall(r'(?<![\w.:])for(?![\w.:])', st2))
        n += len(re.findall(r'(?<![\w.:])while(?![\w.:])', st2))
        n += len(re.findall(r'(?<![\w.:])repeat(?![\w.:])', st2))
        if not re.search(r'\b(?:for|while)\b[^\n]*\bdo\b', st2):
            n += len(re.findall(r'(?<![\w.:])do(?![\w.:])', st2))
        n -= len(re.findall(r'(?<![\w.:])end(?![\w.:])', st2))
        n -= len(re.findall(r'(?<![\w.:])until(?![\w.:])', st2))
        return n

    depth = 0
    for i in range(len(lines) - 1, -1, -1):
        depth -= net(lines[i])
        while depth < 0:
            st = lines[i].strip()
            m = re.match(r'^(.*?)(\s*)(end|until)(\s*)$', st)
            if m and m.group(1).strip():
                # closer glued to a statement: drop just the closer
                lines[i] = lines[i][:lines[i].rindex(m.group(3))].rstrip()
            elif st in ('end', 'until'):
                del lines[i]
            else:
                break
            depth += 1
    depth = 0
    for i in range(len(lines)):
        depth += net(lines[i])
    if depth > 0:
        lines += ['end'] * depth
    return lines


def wrap_returns(lines):
    """`return` must be the last statement of its block. Split trailing
    closers off return lines; wrap non-final returns in `do ... end`;
    unwrap wrapped returns that are final."""
    out = []
    for ln in lines:
        st = ln.strip()
        ind = ln[:len(ln) - len(ln.lstrip())]
        # 1) split trailing block closers: `return X end end` -> `return X` / `end` / `end`
        m = re.match(r'^(.*\S)\s+((?:end|until)(?:\s+(?:end|until))*)\s*$', st)
        if m and not re.match(r'^(end|until|else|elseif)\b', st):
            out.append(ind + m.group(1))
            for kw in re.findall(r'end|until', m.group(2)):
                out.append(kw)
            continue
        out.append(ln)
    # 2) wrap/unwrap
    res = []
    for i, ln in enumerate(out):
        st = ln.strip()
        ind = ln[:len(ln) - len(ln.lstrip())]
        nxt = None
        j = i + 1
        while j < len(out):
            probe = out[j].strip()
            if not probe or probe.startswith('--'):
                j += 1
                continue
            nxt = probe
            break
        final = nxt is None or re.match(r'^(end|else|elseif|until)\b', nxt)
        if st.startswith('return'):
            if not final:
                res.append(ind + 'do ' + st + ' end')
            else:
                res.append(ln)
        elif re.match(r'^do return .* end$', st):
            if final:
                res.append(ind + st[3:-4].strip())
            else:
                res.append(ln)
        else:
            res.append(ln)
    return res



def fix_spacing(lines):
    out = []
    for l in lines:
        l = re.sub(r'\)(?=then\b|else\b|elseif\b|do\b|end\b|until\b)', ') ', l)
        l = re.sub(r'\b(if|elseif|while|until|not|and|or)\(', r'\1 (', l)
        l = re.sub(r'(\d|nil|true|false)(else|then|end|do|until|repeat|or|and|not|in)\b', r'\1 \2', l)
        l = re.sub(r'\b(do|then|else|end|until|repeat|or|and)(\d|nil|true|false)\b', r'\1 \2', l)
        l = re.sub(r'("(?:[^"\\]|\\.)*")\s*(else|then|end|do|until|repeat|or|and|not)\b', r'\1 \2', l)
        l = re.sub(r'\b(else|then|do|or|and|not)("(?:[^"\\]|\\.)*")', r'\1 \2', l)
        # parenthesize bare literals used as index bases: "x"[1] -> ("x")[1]
        l = re.sub(r'("(?:[^"\\]|\\.)*"|(?<![\w.])\d+(?:\.\d+)?|(?<![\w])nil|(?<![\w])true|(?<![\w])false)(\s*\[|\s*\()', r'(\1)\2', l)
        l = re.sub(r'(\d)(\.\.)', r'\1 \2', l)
        l = re.sub(r'=\s+=(?!=)', '==', l)
        if l.lstrip().startswith('('):
            ind = l[:len(l) - len(l.lstrip())]
            l = ind + ';' + l.lstrip()
        m2 = _mask_strings_cmts(l)
        depth = m2.count('(') - m2.count(')')
        if depth > 0 and l.rstrip().endswith('('):
            l = l.rstrip()[:-1].rstrip()
        if re.match(r'^\s*\([^)]*\)\s*(\[[^]]*\])+\s*=', l):
            l = l[:len(l) - len(l.lstrip())] + '-- dropped: assignment to literal base'
        out.append(l)
    return out


def fold_diffs(lines):
    """Fold ((fD+X)-(fD+Y)) constant diffs inside statements."""
    pat = re.compile(r'\(\((\w+)\+(-?\d+)\)-\((\w+)\+(-?\d+)\)\)')
    out = []
    for l in lines:
        def rep(m):
            if m.group(1) == m.group(3):
                return str(int(m.group(2)) - int(m.group(4)))
            return m.group(0)
        out.append(pat.sub(rep, l))
    return out


import re

CIPHER_NAME = {'bZ': 'O', 'cb': 'Q', 'cc': 'U', 'ce': 'V'}
CIPHER_F = {'f1': 'O', 'f2': 'Q', 'f3': 'U', 'f4': 'V'}


def _try_decrypt_val(algo, data, key, seed):
    try:
        import unflat
        if not isinstance(data, list) or not isinstance(key, list) or len(key) != 5:
            return None
        if not isinstance(seed, int):
            return None
        if not all(isinstance(x, int) and 0 <= x <= 255 for x in data):
            return None
        out = unflat.fulcrum_decrypt(algo, data, key, seed)
        if isinstance(out, bytes):
            out = out.decode('latin-1')
        if isinstance(out, list):
            out = ''.join(chr(x) for x in out)
        if not out or len(out) > 500:
            return None
        bad = sum(1 for c in out if ord(c) < 32 and c not in '\r\n\t') + sum(1 for c in out if ord(c) > 126)
        pr = sum(1 for c in out if 32 <= ord(c) <= 126 or c in '\r\n\t')
        if bad == 0 and pr >= 0.7 * len(out):
            return out
    except Exception:
        return None
    return None


def resolve_calls(lines):
    """Brute-force unresolved cipher calls: collect candidate data/key/seed
    literals from the surrounding window, try every combination, keep the one
    that decrypts to printable text."""
    list_re = re.compile(r'\{([0-9,\s]+)\}')
    int_re = re.compile(r'(?<![\w.\[])(-?\d{1,8})(?![\w.\]])')
    call_re = re.compile(r'\b(bZ|cb|cc|ce|f1|f2|f3|f4)\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)')
    out = list(lines)
    resolved = 0
    for i, l in enumerate(out):
        if not call_re.search(l):
            continue
        m = call_re.search(l)
        algo = CIPHER_NAME.get(m.group(1)) or CIPHER_F.get(m.group(1)) or DEC.get(m.group(1))
        if not algo:
            continue
        args = m.group(2)
        # already resolvable?
        # gather candidates from the window
        lo = max(0, i - 30)
        hi = min(len(out), i + 10)
        window = '\n'.join(out[lo:hi])
        datas, keys, seeds = [], [], []
        for mm in list_re.finditer(window):
            nums = [int(x) for x in mm.group(1).split(',') if x.strip()]
            if not nums:
                continue
            if len(nums) == 5:
                keys.append(nums)
            if all(0 <= x <= 255 for x in nums):
                datas.append(nums)
            if len(nums) > 5 and all(0 <= x <= 255 for x in nums):
                pass
        for mm in int_re.finditer(window):
            v = int(mm.group(1))
            if v != 0:
                seeds.append(v)
        seeds = list(dict.fromkeys(seeds))[:48]
        keys = keys[:16]
        datas = datas[:16]
        found = None
        algos = [algo] + [a for a in 'OQUV' if a != algo]
        for d in datas:
            for k in keys:
                for sd in seeds:
                    for alg in algos:
                        r = _try_decrypt_val(alg, d, k, sd)
                        if r:
                            found = (d, k, sd, r)
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                break
        if found:
            repl = lua_quote(found[3])
            l2 = out[i][:m.start()] + repl + out[i][m.end():]
            out[i] = l2
            resolved += 1
    return out


IIFE_HEAD = re.compile(r'^(\s*)([\w\[\]]+) = \(function\(([^)]*)\)return function\(\.\.\.\)return\(function\(\.\.\.\)(.*)$')
IIFE_F3 = re.compile(r'^(\s*)([\w\[\]]+) = function\(\.\.\.\)return\(function\(\.\.\.\)(.*)$')
IIFE_TAIL = re.compile(r'^\s*\)\((\w+),(\w+),(\w+),(\w+),[^)]*\)[^\w]*end end\)\(([^)]*)\)\s*$')


def collapse_iife(lines):
    """Collapse '(function(a,b,c,d)return function(...)return(function(...)' wrappers
    into 'X = function(...)' with the factory args substituted."""
    out = []
    i = 0
    while i < len(lines):
        m3 = IIFE_F3.match(lines[i])
        if m3:
            ind3, tgt3, inline3 = m3.groups()
            j = i + 1
            tail = -1
            while j < len(lines) and j < i + 4000:
                if re.search(r'\)\(.*\)end\s*$', lines[j]):
                    tail = j
                    break
                j += 1
            if tail > 0:
                out.append('%s%s = (function(...)%s' % (ind3, tgt3, inline3))
                out.extend(lines[i + 1:tail])
                out.append(re.sub(r'end\s*$', '', lines[tail]))
                i = tail + 1
                continue
            out.append(lines[i])
            i += 1
            continue
        m = IIFE_HEAD.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        indent, target, params_s, inline_start = m.groups()
        params = [x.strip() for x in params_s.split(',') if x.strip()]
        joined = '\n'.join(lines[i + 1:])
        # find the tail: '...args)end end)(outer-args)'
        _tm = re.search(r'end\s*end\)\s*\(', joined)
        if not _tm:
            out.append(lines[i])
            i += 1
            continue
        pos = _tm.start()
        # outer args: after 'end end)(' up to the matching close paren
        ostart = _tm.end()
        depth = 1
        k = ostart
        instr = None
        while k < len(joined) and depth > 0:
            ch = joined[k]
            if instr:
                if ch == instr:
                    instr = None
            elif ch == '"' or ch == "'":
                instr = ch
            elif ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
            k += 1
        outer_text = joined[ostart:k - 1]
        # body = everything before the inner call's close paren at pos
        body_text = joined[:pos - 1] if pos > 0 else ''
        # the inner call ')(' ... close at pos-1: body ends at its open ')('
        ipos = body_text.rfind(')(')
        if ipos >= 0:
            body_text = body_text[:ipos]
        body = body_text.split('\n') if body_text.strip() else []
        outer = [x.strip() for x in outer_text.split(',')]
        while len(outer) < len(params):
            outer.append('nil')
        subs = {}
        for pi, pn in enumerate(params):
            subs[pn] = outer[pi]
        body = ([inline_start] if inline_start.strip() else []) + body
        out.append('%s%s = function(...)' % (indent, target))
        for bl in body:
            for kk, v in subs.items():
                bl = re.sub(r'\b%s\b' % re.escape(kk), lambda _m, _v=v: _v, bl)
            out.append(bl)
        out.append('%send' % indent)
        consumed = joined[:k].count('\n') + 1
        i = i + 1 + consumed
    return out


def main(inp, outp):
    text = open(inp).read()
    # normalize the splice artifacts
    lines = text.split('\n')
    lines = recognize_ciphers(lines)
    lines = split_semis(lines)
    lines = split_blocks(lines)
    lines = fold_diffs(lines)
    lines = strip_traces(lines)
    lines = [l for l in lines if not is_plumbing(l)]
    lines = expand_giants(lines)
    lines = drop_shuffles(lines)
    lines = propagate(lines)
    lines = inline_decrypt(lines)
    lines = strip_markers(lines)
    lines = strip_machinery(lines)
    lines = unwrap_repeats(lines)
    lines = fold_diffs(lines)
    lines = deep_propagate(lines)
    lines = inline_decrypt(lines)
    lines = resolve_calls(lines)
    lines = collapse_iife(lines)
    lines = drop_junk_loops(lines)
    lines = drop_dead(lines)
    lines = drop_dead_cells(lines)
    lines = flatten_wrapper(lines)
    lines = readable_names(lines)
    lines = fix_spacing(lines)
    lines = [re.sub(r'\(("(?:[^"\\]|\\.)*"|\'[^\']*\'|\d+)\)\[1\]', r'\1', ln) for ln in lines]
    lines = [re.sub(r'(\d)(else|then|end|do|until|repeat|or|and|not|in)\b', r'\1 \2', l) for l in lines]
    lines = [re.sub(r'(\d)(\.\.)', r'\1 \2', l) for l in lines]
    lines = [re.sub(r'(\.\.)(nil|true|false|\d)', r'\1 \2', l) for l in lines]
    lines = [re.sub(r'\)(?=then\b|else\b|elseif\b|do\b|end\b|until\b)', ') ', l) for l in lines]
    lines = repair_structure(lines)
    lines = wrap_returns(lines)
    lines = style_pass(lines)
    lines = format_lines(lines)
    # final cleanup sweep (runs last: wrap bare literals in index/call position, drop literal-callee calls)
    def _fin(ln):
        ln = re.sub(r'(?<![\w.\)\]])(\"(?:[^\\"]|\\.)*\"|nil|true|false|-?(?:0[xX][0-9a-fA-F]+|\d+(?:\.\d+)?|\.\d+))(\s*\[|\s*\()', r'(\1)\2', ln)
        ln = drop_literal_calls_line(ln)
        return ln
    lines = [_fin(l) for l in lines]
    header = ['-- deobfuscated by discord.gg/printed',
              '-- fulcrum polsec runtime | strings decrypted with the O/Q/U/V ciphers', '']
    open(outp, 'w').write('\n'.join(header + lines) + '\n')
    nfix = heal_syntax(outp)
    print('heal fixes:', nfix)
    print('lines:', len(lines))
    print('output:', outp)


import os as _os
LUAU_CC = _os.environ.get('LUAU_CC') or _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'bin', 'luau-compile')
if not _os.path.exists(LUAU_CC) or not _os.access(LUAU_CC, _os.X_OK):
    for _c in ('luau-compile',):
        import shutil as _sh
        if _sh.which(_c):
            LUAU_CC = _sh.which(_c)
            break


def heal_syntax(path, max_iter=80):
    """Iteratively heal syntax errors using the luau compiler as oracle.
    Fixes missing `end` / `until true` / `)` / leading `;` mechanically."""
    import subprocess
    fixed = 0
    for it in range(max_iter):
        r = subprocess.run([LUAU_CC, '--binary', path],
                           capture_output=True, timeout=120)
        if r.returncode == 0:
            break
        m = re.search(rb'\((\d+),(\d+)\): SyntaxError: ([^\r\n]*)', r.stderr or b'')
        if not m:
            print('heal: unparseable error')
            break
        lno = int(m.group(1))
        msg = m.group(3).decode('utf-8', 'replace')
        lines = open(path).read().split('\n')
        if lno - 1 >= len(lines):
            break
        ind = lines[lno - 1][:len(lines[lno - 1]) - len(lines[lno - 1].lstrip())]
        if msg.startswith("Expected 'end'"):
            lines.insert(lno - 1, ind + 'end')
            fixed += 1
        elif msg.startswith("Expected 'until'"):
            lines.insert(lno - 1, ind + 'until true')
            fixed += 1
        elif msg.startswith("Expected 'do'"):
            # while/for header missing `do`
            lines[lno - 1] = lines[lno - 1].rstrip() + ' do'
            fixed += 1
        elif msg.startswith("Expected ')'") or msg.startswith("Expected ']'") or msg.startswith("Expected '}'"):
            tok = msg.split("'")[1]
            if "got 'end'" in msg:
                # extra `end` before the closer: drop one end-token here
                l = lines[lno - 1]
                l2 = l.replace('end', '', 1) if 'end' in l else l
                if l2.strip() == '':
                    del lines[lno - 1]
                else:
                    lines[lno - 1] = l2
            else:
                lines.insert(lno - 1, ind + tok)
            fixed += 1
        elif 'Incomplete statement' in msg:
            if re.match(r'^\s*[A-Za-z_]\w*\s*$', lines[lno - 1]):
                del lines[lno - 1]
            else:
                lines[lno - 1] = ind + '-- dropped: incomplete statement'
            fixed += 1
        elif 'continue statement must be inside a loop' in msg:
            lines[lno - 1] = ind + 'do end -- continue'
            fixed += 1
        elif (msg.startswith('Expected identifier') or msg.startswith('Incomplete statement')) and \
                lines[lno - 1].lstrip().startswith(')'):
            del lines[lno - 1]
            fixed += 1
        elif 'must be a variable or a field' in msg:
            # assignment to a literal-base: dead anyway -> drop the statement
            lines[lno - 1] = ind + '-- dropped: assignment to literal base'
            fixed += 1
        elif msg.startswith('Expected identifier') and lines[lno - 1].strip() in (
                'nil', 'true', 'false', 'end', 'then', 'else', 'do', 'and', 'or', 'not'):
            del lines[lno - 1]
            fixed += 1
        elif 'Ambiguous syntax' in msg:
            lines[lno - 1] = ind + ';' + lines[lno - 1].lstrip()
            fixed += 1
        elif msg.startswith('Expected <eof>'):
            # the chunk terminated early: drop an orphan closer on the error
            # line, or wrap the top-level `return` above it in do...end
            l = lines[lno - 1]
            st = l.strip()
            if st == 'else' or st.startswith('elseif'):
                del lines[lno - 1]
                fixed += 1
            elif st.startswith('end') or st.startswith('until'):
                kw = st.split()[0]
                idx = l.find(kw)
                l2 = (l[:idx] + l[idx + len(kw):]) if idx >= 0 else l
                if l2.strip() == '':
                    del lines[lno - 1]
                else:
                    lines[lno - 1] = l2
                fixed += 1
            else:
                wrapped = False
                for j in range(lno - 2, max(-1, lno - 15), -1):
                    mj = re.match(r'^(\s*)return\b(.*)$', lines[j])
                    if mj and not lines[j].rstrip().endswith('end'):
                        body = mj.group(2).rstrip()
                        lines[j] = mj.group(1) + 'do return' + body + ' end'
                        wrapped = True
                        break
                if wrapped:
                    fixed += 1
                else:
                    print('heal: stopping at:', msg[:120])
                    break
        else:
            print('heal: stopping at:', msg[:120])
            break
        open(path, 'w').write('\n'.join(lines))
    return fixed



# ============ readable names: flatten VM store cells + typed counters ==========
_BUILTINS = set("""
and break do else elseif end false for function goto if in local nil not or
repeat return then true until while
assert collectgarbage error getfenv getmetatable ipairs loadstring next pairs
pcall print rawequal rawget rawset require select setmetatable tonumber tostring
type unpack warn xpcall
math string table os task coroutine spawn tick time typeof game workspace
script Instance Vector3 CFrame Color3 UDim2 UDim Vector2 BrickColor Enum
self data key seed length out geniter
a b c d e f i
""".split())

_FUNC_BUILTINS = set("""
getfenv print warn pcall tostring tonumber setmetatable getmetatable type
ipairs pairs next select rawget rawset rawequal error assert loadstring spawn
wait tick time typeof require collectgarbage xpcall unpack select
""".split())
_TABLE_BUILTINS = set("math string table os task coroutine game workspace".split())

_NUM_RE = re.compile(r"^-?(0[xX][0-9a-fA-F]+|(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?)$")
_CHAIN_RE = re.compile(r"[A-Za-z_]\w*(?:\[\s*\d+\s*\])+")
_FREE_RE = re.compile(r"(?<![\w.:])([A-Za-z_]\w*)")


def _lit_type(expr):
    e = expr.strip()
    if not e:
        return None
    if e[0] in '"\'':
        return 's'
    if e.startswith('[['):
        return 's'
    if e[0] == '{':
        return 't'
    if e in ('nil', 'true', 'false'):
        return 'v'
    if _NUM_RE.match(e):
        return 'n'
    if e.startswith('function') or e.startswith('(function'):
        return 'f'
    if e in _FUNC_BUILTINS:
        return 'f'
    if e in _TABLE_BUILTINS:
        return 't'
    return None


def _commas_toplevel(masked):
    """indices of top-level commas in masked text"""
    out = []
    depth = 0
    for i, ch in enumerate(masked):
        if ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        elif ch == ',' and depth == 0:
            out.append(i)
    return out


def _split_pair(text, masked):
    """split 'a,b = c,d' into targets/exprs using masked commas; returns
    lists of original-text pieces or None"""
    # find top-level '=' (not ==, <=, >=, ~=)
    depth = 0
    eqpos = -1
    for i, ch in enumerate(masked):
        if ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        elif ch == '=' and depth == 0:
            prv = masked[i - 1] if i > 0 else ''
            nxt = masked[i + 1] if i + 1 < len(masked) else ''
            if prv not in '=<>~' and nxt != '=':
                eqpos = i
                break
    if eqpos < 0:
        return None
    lt_m, rt_m = masked[:eqpos], masked[eqpos + 1:]
    lt, rt = text[:eqpos], text[eqpos + 1:]
    def pieces(seg, segm):
        cs = _commas_toplevel(segm)
        res = []
        prev = 0
        for c in cs:
            res.append(seg[prev:c])
            prev = c + 1
        res.append(seg[prev:])
        return res
    return pieces(lt, lt_m), pieces(rt, rt_m)


def _rewrite_spans(line, spans_repl):
    """spans_repl: list of (start, end, newtext) applied to line (non-overlap)"""
    if not spans_repl:
        return line
    spans_repl = sorted(spans_repl, key=lambda x: x[0])
    out = []
    prev = 0
    for a, b, t in spans_repl:
        if a < prev:
            continue
        out.append(line[prev:a])
        out.append(t)
        prev = b
    out.append(line[prev:])
    return ''.join(out)


# ============ glue splitting + call-on-literal cleanup ==========
GLUE_KW = ('else', 'then', 'end', 'do', 'until', 'repeat', 'or', 'and', 'not', 'in')
_GLUE_PRE = set('0123456789])"\'')
_LIT_PRE = ('nil', 'true', 'false')
_KEYWORD_SET = set('and break do else elseif end false for function goto if in local nil not or repeat return then true until while'.split())
_GLUE_PROTECT = set('floor min again error send friend weekend bend fend mend tend lend band hand rand sand stand land door mirror major minor twin coin join thin skin cannot strengthen'.split())


def split_glue_line(ln):
    """insert spaces in substitution-glued tokens: `v8else`, `nilelse`,
    `]elseaN`, ... Safe: only splits at keyword/literal boundaries when the
    context proves glue (adjacent `]`/digit/quote/`)` or literal prefix)."""
    m2 = _mask_strings_cmts(ln)
    if len(m2) != len(ln):
        return ln
    changed = True
    while changed:
        changed = False
        m2 = _mask_strings_cmts(ln)
        for mm in re.finditer(r'[A-Za-z_][A-Za-z0-9_]*', m2):
            run = mm.group(0)
            a, b = mm.start(), mm.end()
            # trailing keyword: run ends with a keyword
            for kw in GLUE_KW:
                if len(run) > len(kw) and run.endswith(kw) and \
                        run not in _KEYWORD_SET and run not in _GLUE_PROTECT and \
                        run not in _BUILTINS:
                    pre = run[:-len(kw)]
                    ch_before = ln[a + len(pre) - 1] if len(pre) else ''
                    if True:
                        ln = ln[:a + len(pre)] + ' ' + ln[a + len(pre):]
                        changed = True
                        break
            if changed:
                break
            # leading keyword: run starts with a keyword, context shows glue
            for kw in GLUE_KW:
                if len(run) > len(kw) and run.startswith(kw):
                    ch_before = ln[a - 1] if a > 0 else ' '
                    ch_after = ln[a + len(kw)]
                    if ch_before in _GLUE_PRE or ch_before == '=':
                        ln = ln[:a + len(kw)] + ' ' + ln[a + len(kw):]
                        changed = True
                        break
            if changed:
                break
    return ln


def drop_literal_calls_line(ln):
    """`nil (args)` / `"x" (args)` / `5(args)` = call on a literal -> keep the
    literal, drop the (args).  (call-callee substitution artifact; the call
    could only ever error.)"""
    m2 = _mask_strings_cmts(ln)
    if len(m2) != len(ln):
        return ln
    reps = []
    for mm in re.finditer(
            r'(?<!\w)(nil|true|false|-?(?:0[xX][0-9a-fA-F]+|\d+(?:\.\d+)?|\.\d+)|"(?:[^"\\]|\\.)*")\s*(\()',
            m2):
        # find matching close paren for mm.group(2)
        j = mm.end(2) - 1
        depth = 0
        k = j
        while k < len(m2):
            if m2[k] == '(':
                depth += 1
            elif m2[k] == ')':
                depth -= 1
                if depth == 0:
                    break
            k += 1
        if k >= len(m2):
            continue
        reps.append((mm.start(1), k + 1, ln[mm.start(1):mm.end(1)]))
    return _rewrite_spans(ln, reps)



def readable_names(lines):
    # ---- 0) normalize literal-index brackets + strip [1]-of-literal artifacts
    out = []
    for ln in lines:
        if ln.lstrip().startswith('--'):
            out.append(ln)
            continue
        ln = split_glue_line(ln)
        ln = drop_literal_calls_line(ln)
        m2 = _mask_strings_cmts(ln)
        if len(m2) != len(ln):
            out.append(ln)
            continue
        reps = []
        for mm in re.finditer(r'\[\s*(\d+)\s*\]', m2):
            reps.append((mm.start(), mm.end(), '[' + mm.group(1) + ']'))
        ln2 = _rewrite_spans(ln, reps)
        m2 = _mask_strings_cmts(ln2)
        # ("str")[1] -> "str"   (the [1] was the VM cell slot)
        reps = []
        for mm in re.finditer(r'\((?:"[^"]*"|\d+|nil|true|false)\)\[1\]', ln2):
            if m2[mm.start()] != ln2[mm.start()]:
                continue
            raw = ln2[mm.start():mm.end()]
            inner = raw[1:raw.rindex(')')]
            reps.append((mm.start(), mm.end(), inner))
        ln2 = _rewrite_spans(ln2, reps)
        m2 = _mask_strings_cmts(ln2)
        # (literal) -> literal  when not followed by [ or ( and not statement start
        reps = []
        for mm in re.finditer(r'\((?:"[^"]*"|\d+|nil|true|false)\)(?!\[|\()', ln2):
            if mm.start() == 0 or m2[mm.start()] != ln2[mm.start()]:
                continue
            pre_txt = ln2[:mm.start()].rstrip()
            pre = pre_txt[-1:]
            kw_ctx = re.search(r'(if|elseif|while|until|return|not|and|or|then|else|do|,|=)$', pre_txt)
            if pre and (pre.isalnum() or pre in '_)]"\'}') and not kw_ctx:
                continue    # call-arg parens: keep
            raw = ln2[mm.start():mm.end()]
            reps.append((mm.start(), mm.end(), raw[1:-1]))
        ln2 = _rewrite_spans(ln2, reps)
        out.append(ln2)
    lines = out

    # ---- 1) analysis: assignments, function defs, params, chain occurrences
    types = {}          # name-or-chain -> type letter
    param_names = set()
    assign_count = {}   # name/chain -> number of LHS occurrences
    decl_info = {}      # name/chain -> (line_index, literal_expr) for single-target
    chain_occ = {}      # root -> list of (line_idx, start, end, text)
    bare_roots = set()

    def note_type(key, t):
        if t is None:
            return
        cur = types.get(key)
        if cur is None:
            types[key] = t
        elif cur != t:
            types[key] = 'v'

    for i, ln in enumerate(lines):
        stripped = ln.lstrip()
        if stripped.startswith('--'):
            continue
        m2 = _mask_strings_cmts(ln)
        if len(m2) != len(ln):
            continue
        # function defs
        for fm in re.finditer(r'\bfunction\s*\(([^)]*)\)', m2):
            for p in fm.group(1).split(','):
                p = p.strip()
                if re.match(r'^[A-Za-z_]\w*$', p):
                    param_names.add(p)
        for fm in re.finditer(r'\bfunction\s+([A-Za-z_]\w*)\s*\(([^)]*)\)', m2):
            note_type(fm.group(1), 'f')
            for p in fm.group(2).split(','):
                p = p.strip()
                if re.match(r'^[A-Za-z_]\w*$', p):
                    param_names.add(p)
        for fm in re.finditer(r'\bfunction\s+[A-Za-z_]\w*[:.][A-Za-z_\w]*\s*\(([^)]*)\)', m2):
            for p in fm.group(1).split(','):
                p = p.strip()
                if re.match(r'^[A-Za-z_]\w*$', p):
                    param_names.add(p)
        # anonymous function params anywhere: function(...)
        for fm in re.finditer(r'function\s*\(([^)]*)\)', m2):
            for p in fm.group(1).split(','):
                p = p.strip()
                if re.match(r'^[A-Za-z_]\w*$', p):
                    param_names.add(p)
        for fm in re.finditer(r'\bfor\s+([A-Za-z_]\w*)\s*[=,]', m2):
            param_names.add(fm.group(1))
        for fm in re.finditer(r'\bfor\s+([A-Za-z_]\w*)\s+([A-Za-z_]\w*)\s+in\b', m2):
            param_names.add(fm.group(1)); param_names.add(fm.group(2))
        # assignments
        body_m = m2
        is_local = False
        bm = re.match(r'^(\s*)(local\s+)(.*)$', body_m)
        work_m = bm.group(3) if bm else re.sub(r'^\s*', '', body_m)
        work_t = ln[len(ln) - len(work_m):]
        pr = _split_pair(work_t, work_m)
        if pr:
            tgts, exprs = pr
            single = len(tgts) == 1 and re.match(r'^\s*[A-Za-z_][\w\[\]\s]*\s*$', tgts[0]) and tgts[0].strip()
            for ti, tg in enumerate(tgts):
                tg_strip = tg.strip()
                if not re.match(r'^[A-Za-z_]\w*(?:\[\s*\d+\s*\])*$', tg_strip):
                    continue
                assign_count[tg_strip] = assign_count.get(tg_strip, 0) + 1
                ex = exprs[ti] if ti < len(exprs) else ''
                note_type(tg_strip, _lit_type(ex))
                if single and ti == 0:
                    decl_info[tg_strip] = (i, ex.strip())
        # chain occurrences
        for cm in _CHAIN_RE.finditer(m2):
            txt = cm.group(0)
            root = re.match(r'[A-Za-z_]\w*', txt).group(0)
            chain_occ.setdefault(root, []).append((i, cm.start(), cm.end(), txt))
        # bare identifier occurrences (root not immediately followed by '[')
        for im in _FREE_RE.finditer(m2):
            nm = im.group(1)
            j = im.end()
            if j < len(m2) and m2[j] == '[':
                continue    # part of a chain occurrence
            bare_roots.add(nm)

    # ---- 2) build name map: chains under bare-less roots, then free idents
    used_final = set(_BUILTINS)
    counters = {'s': 0, 'n': 0, 't': 0, 'f': 0, 'v': 0}

    def new_name(t):
        while True:
            counters[t] += 1
            nm = '%s%d' % (t, counters[t])
            if nm not in used_final and nm not in types and nm not in chain_occ:
                used_final.add(nm)
                return nm

    name_map = {}

    # rule B: flatten maximal chains of bare-less roots
    chain_targets = []   # (line_idx, start, end, text, newname)
    seen_chain = {}
    for i, ln in enumerate(lines):
        m2 = _mask_strings_cmts(ln)
        if len(m2) != len(ln):
            continue
        for cm in _CHAIN_RE.finditer(m2):
            txt = cm.group(0)
            root = re.match(r'[A-Za-z_]\w*', txt).group(0)
            if root in bare_roots and (root in param_names or root in _BUILTINS):
                continue
            if txt not in seen_chain:
                seen_chain[txt] = new_name(types.get(txt, 'v'))
            chain_targets.append((i, cm.start(), cm.end(), txt, seen_chain[txt]))

    # rule A: bare roots whose only literal chains are exactly [1] -> collapse
    collapse_roots = set()
    for root, occs in chain_occ.items():
        if root in bare_roots and root not in _BUILTINS:
            if all(o[3] == root + '[1]' for o in occs):
                collapse_roots.add(root)

    # ---- 3) apply chain replacements + collapses per line
    per_line = {}
    for i, a, b, txt, nm in chain_targets:
        per_line.setdefault(i, []).append((a, b, nm))
    out = []
    for i, ln in enumerate(lines):
        reps = []
        for a, b, nm in per_line.get(i, []):
            pre = ln[a - 1] if a > 0 else ' '
            post = ln[b] if b < len(ln) else ' '
            txt = nm
            if pre not in ' \t' and (pre.isalnum() or pre == '_'):
                txt = ' ' + txt
            if post.isalnum() or post == '_':
                txt = txt + ' '
            reps.append((a, b, txt))
        if collapse_roots:
            m2 = _mask_strings_cmts(ln)
            if len(m2) == len(ln):
                for root in collapse_roots:
                    for mm in re.finditer(re.escape(root + '[1]'), m2):
                        reps = reps + [(mm.start(), mm.end(), root)]
        ln2 = _rewrite_spans(ln, reps)
        out.append(split_glue_line(ln2))
    lines = out

    # ---- 4) free identifiers
    id_first = {}
    for i, ln in enumerate(lines):
        m2 = _mask_strings_cmts(ln)
        if len(m2) != len(ln):
            continue
        for im in _FREE_RE.finditer(m2):
            nm = im.group(1)
            if nm in _BUILTINS or nm in seen_chain.values() or nm in used_final:
                continue
            if nm not in id_first:
                id_first[nm] = types.get(nm, 'v')
    for nm, t in id_first.items():
        if nm in param_names:
            t = 'v'
        name_map[nm] = new_name(t)

    out = []
    for ln in lines:
        m2 = _mask_strings_cmts(ln)
        if len(m2) != len(ln):
            out.append(ln)
            continue
        reps = []
        for im in _FREE_RE.finditer(m2):
            nm = im.group(1)
            if nm in name_map:
                reps.append((im.start(1), im.end(1), name_map[nm]))
        out.append(_rewrite_spans(ln, reps))
    lines = out

    # ---- 5) inline primitive constants (single-assign, single-target decl)
    inlineable = {}
    for key, (li, ex) in decl_info.items():
        t = _lit_type(ex)
        if t in ('s', 'n', 'v') and ex in ('nil', 'true', 'false') or t in ('s', 'n'):
            if key not in param_names and key not in _BUILTINS:
                if assign_count.get(key, 0) == 1:
                    nm = seen_chain.get(key) or name_map.get(key, key)
                    if nm not in _BUILTINS:
                        inlineable[nm] = ex
    if inlineable:
        drop = set()
        out = []
        for i, ln in enumerate(lines):
            stripped = ln.lstrip()
            hit_decl = None
            for nm, ex in inlineable.items():
                if re.match(r'^(local\s+)?' + re.escape(nm) + r'\s*=\s*' + re.escape(ex) + r'\s*$', stripped):
                    hit_decl = (nm, i)
                    break
            if hit_decl and hit_decl[1] == i:
                drop.add(nm)
                continue    # drop the decl line entirely
            m2 = _mask_strings_cmts(ln)
            if len(m2) != len(ln):
                out.append(ln)
                continue
            reps = []
            for im in _FREE_RE.finditer(m2):
                nm = im.group(1)
                if nm in inlineable:
                    val = inlineable[nm]
                    a, b = im.start(1), im.end(1)
                    pre = ln[a - 1] if a > 0 else ' '
                    post = ln[b] if b < len(ln) else ' '
                    if val in ('nil', 'true', 'false') or val.startswith('"') or val.startswith("'"):
                        txt = val
                        if (pre.isalnum() or pre == '_') :
                            txt = ' ' + txt
                        if post.isalnum() or post == '_':
                            txt = txt + ' '
                    else:
                        post2 = post
                        if post2 in '([.' or post2.isdigit():
                            txt = '(' + val + ')'
                        else:
                            txt = val
                            if pre.isalnum() or pre == '_':
                                txt = ' ' + txt
                            if post2.isalnum() or post2 == '_':
                                txt = txt + ' '
                    reps.append((a, b, txt))
            out.append(_rewrite_spans(ln, reps))
        lines = out
    # drop calls on literal callees produced by inlining (`"floor"(args)` -> `"floor"`)
    lines = [drop_literal_calls_line(l) for l in lines]
    # glue created by inlining: number|literal|keyword boundaries
    out = []
    for l in lines:
        l = re.sub(r'(\d)(else|then|end|do|until|repeat|or|and|not|in)\b', r'\1 \2', l)
        l = re.sub(r'\b(nil|true|false)(else|then|end|do|until|repeat|or|and|not|in)\b', r'\1 \2', l)
        l = re.sub(r'(\d)(\.\.)', r'\1 \2', l)
        l = re.sub(r'(\.\.)(nil|true|false|\d)', r'\1 \2', l)
        l = re.sub(r'\)(?=then\b|else\b|elseif\b|do\b|end\b|until\b)', ') ', l)
        out.append(l)
    return out


def style_pass(lines):
    out = []
    for ln in lines:
        stripped = ln.lstrip()
        if stripped.startswith('--'):
            out.append(ln)
            continue
        m2 = _mask_strings_cmts(ln)
        if len(m2) != len(ln):
            out.append(ln)
            continue
        # compound assignment: X = X + Y -> X += Y (also -, *, /, %, ..)
        mm = re.match(r'^(\s*)([A-Za-z_]\w*(?:\[[^\]]+\])*) = \2 (\.\.|[+\-*/%]) (.+)$', m2)
        if mm:
            a, b, op = mm.start(3), mm.end(3), mm.group(3)
            ln = ln[:mm.start(2)] + mm.group(2) + ' ' + op + '= ' + ln[mm.end(3) + 1:]
        out.append(ln)
    # blank-line cosmetics: collapse runs of blanks, add blank before top-level blocks
    res = []
    for ln in out:
        if ln.strip() == '' and res and res[-1].strip() == '':
            continue
        res.append(ln)
    out = []
    for i, ln in enumerate(res):
        st = ln.lstrip()
        if (not ln.startswith((' ', '\t')) and ln.strip() != '' and res and res[-1].strip() != ''
                and re.match(r'^(if|for|while|repeat|function|do)\b', st)
                and not res[-1].lstrip().startswith(('else', 'then', 'do'))):
            out.append('')
        out.append(ln)
    return out



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
