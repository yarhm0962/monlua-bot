#!/usr/bin/env python3
"""vmwalk.py — CFG walker for the PolSec Fulcrum variant (XOR-keyed dispatcher).

Concrete execution model:
  h   = PC (int)
  F,M,q,f = channel values (ints). Decode: u = F ^ h; L = u//32; op = u%32;
            e = (q==F) ? L : ((q ^ h)//32).
  Block id = (L, op, e). Transitions inside a block body set these values.
"""
import re, sys, pickle
sys.path.insert(0, '/workspace/monlua-bot/deobf/fulcrum-engine')
import vmtree

BX = (1 << 32) - 1

def bxor(a, b):
    return (a ^ b) & BX

class Walker:
    def __init__(self, src, root):
        self.src = src
        self.root = root
        self.leafcache = {}

    def leaf_for(self, L, op, e):
        key = (L, op, e)
        if key in self.leafcache:
            return self.leafcache[key]
        env = {'L': L, 'u': op, 'e': e}
        self._path = []
        kids = self._resolve(self.root, env)
        path = list(self._path)
        self.leafcache[key] = (path, kids)
        return path, kids

    def _resolve(self, kids, env):
        runs = []
        for x in kids:
            if x[0] == 'if':
                node = x[1]
                hit = None
                for cond, ch in node['branches']:
                    if self._ev(cond, env):
                        hit = (cond, ch); break
                if hit is None and node['else'] is not None:
                    hit = ('(else)', node['else'])
                if hit is not None:
                    self._path.append(hit[0])
                    r = self._resolve(hit[1], env)
                    if r is not None:
                        return r
                    self._path.pop()
                    continue
                continue
            runs.append(x)
        return runs or None

    def _ev(self, cond, env):
        try:
            return bool(eval(cond.replace('~=', '!='), {'__builtins__': {}}, dict(env)))
        except Exception:
            return False

    def leaf_text(self, kids):
        return ';'.join(self.src[x[1]:x[2]] if x[0] == 'run' else self.src[x[2]:x[3]]
                        for x in kids)

# --- transition extraction -------------------------------------------------

RE_H_ADD = re.compile(r'\bh=\((\d+)\+h\)|\bh=\(h\+(\d+)\)|\bh=h\+(\d+)\b|\bh=(\d+)\+h\b')
RE_SET_KEY = re.compile(r'\b([FfqM])=I\((\d+),h\)|\b([FfqM])=I\(h,(\d+)\)')
RE_COPY = re.compile(r'\b([FfqM])=([A-Za-z_]\w*)\b')
RE_PAIR = re.compile(r'\b([FfqmM]),([FfqmM])=I\((\d+),h\),I\((\d+),h\)')

def parse_transitions(text):
    """Extract ordered (kind, args) events that mutate dispatcher state.
    kinds: h_add(delta), set(var, key), copy(dst, src), swap(a, b)"""
    events = []
    for m in RE_PAIR.finditer(text):
        events.append(('set2', m.group(1), int(m.group(3)), m.group(2), int(m.group(4))))
    text2 = RE_PAIR.sub(' ', text)
    pos = 0
    # walk matches of set/copy/h in textual order
    pats = [RE_SET_KEY, RE_COPY, RE_H_ADD]
    while pos < len(text2):
        best = None
        for p in pats:
            m = p.search(text2, pos)
            if m and (best is None or m.start() < best[0]):
                best = (m.start(), m)
        if best is None:
            break
        m = best[1]
        if m.re is RE_SET_KEY:
            var = m.group(1) or m.group(3)
            key = int(m.group(2) or m.group(4))
            events.append(('set', var, key))
        elif m.re is RE_COPY:
            events.append(('copy', m.group(1), m.group(2)))
        else:
            d = int(m.group(1) or m.group(2) or m.group(3) or m.group(4))
            events.append(('h_add', d))
        pos = m.end()
    return events

def apply_events(events, st, vals=None):
    """Apply ordered events; returns (st, ok). ok=False on unresolvable copy."""
    if vals is None:
        vals = {}
    for ev in events:
        k = ev[0]
        if k == 'h_add':
            st['h'] = (st['h'] + ev[1]) & BX
        elif k == 'h_set':
            st['h'] = ev[1]
        elif k == 'set':
            st[ev[1]] = bxor(ev[2], st['h'])
        elif k == 'set2':
            st[ev[1]] = bxor(ev[2], st['h'])
            st[ev[3]] = bxor(ev[4], st['h'])
        elif k == 's':
            st['s'] = ev[1]
        elif k == 'copy':
            st[ev[1]] = st[ev[2]]
        elif k == 'copyv':
            v = vals.get(ev[2])
            if v is None:
                return st, False
            st[ev[1]] = v
        elif k == 'copy_unknown':
            return st, False
        elif k == 'set_from':
            src = vals.get(ev[2], st.get(ev[2]))
            if src is None:
                return st, False
            st[ev[1]] = bxor(src, ev[3])
        elif k == 'add':
            st[ev[1]] = (st[ev[1]] + ev[2]) & BX
        elif k == 'set_chan_num':
            st[ev[1]] = ev[2]
        elif k == 'setv':
            var, form = ev[1], ev[2]
            if form[0] == 'xorh':
                vals[var] = bxor(form[1], st['h'])
            elif form[0] == 'xor':
                src = vals.get(form[1], st.get(form[1]))
                if src is None:
                    vals.pop(var, None)
                else:
                    vals[var] = bxor(src, form[2])
            else:
                vals[var] = form[1]
        elif k == 'addv':
            var, d, src = ev[1], ev[2], ev[3]
            cur = vals.get(src, st.get(src))
            if isinstance(cur, int):
                vals[var] = (cur + d) & BX
            else:
                vals.pop(var, None)
    return st, True


def apply_one(ev, st, vals):
    """Apply one event; returns (st, vals, ok)."""
    k = ev[0]
    if k == 'h_add':
        st['h'] = (st['h'] + ev[1]) & BX
    elif k == 'h_set':
        st['h'] = ev[1]
    elif k == 'set':
        st[ev[1]] = bxor(ev[2], st['h'])
    elif k == 'set2':
        st[ev[1]] = bxor(ev[2], st['h'])
        st[ev[3]] = bxor(ev[4], st['h'])
    elif k == 's':
        st['s'] = ev[1]
    elif k == 'copy':
        st[ev[1]] = st[ev[2]]
    elif k == 'copyv':
        v = vals.get(ev[2])
        if v is None:
            return st, vals, False
        st[ev[1]] = v
    elif k == 'copy_unknown':
        return st, vals, False
    elif k == 'set_from':
        src = vals.get(ev[2], st.get(ev[2]))
        if src is None:
            return st, vals, False
        st[ev[1]] = bxor(src, ev[3])
    elif k == 'add':
        st[ev[1]] = (st[ev[1]] + ev[2]) & BX
    elif k == 'set_chan_num':
        st[ev[1]] = ev[2]
    elif k == 'setv':
        var, form = ev[1], ev[2]
        if form[0] == 'xorh':
            vals[var] = bxor(form[1], st['h'])
        elif form[0] == 'xor':
            src = vals.get(form[1], st.get(form[1]))
            if src is None:
                vals.pop(var, None)
            else:
                vals[var] = bxor(src, form[2])
        elif form[0] == 'add':
            cur = vals.get(form[2], st.get(form[2]))
            nv = (cur + form[1]) & BX if isinstance(cur, int) else None
            if nv is None:
                vals.pop(var, None)
            else:
                vals[var] = nv
        else:
            vals[var] = form[1]
    elif k == 'addv':
        var, d, src = ev[1], ev[2], ev[3]
        cur = vals.get(src, st.get(src))
        if isinstance(cur, int):
            vals[var] = (cur + d) & BX
        else:
            vals.pop(var, None)
    return st, vals, True


def expand_states(events, st, vals):
    """Returns a list of (cond_text_or_None, st, vals). Cross-products branches."""
    out = [(None, dict(st), dict(vals))]
    for ev in events:
        if ev[0] == 'branch':
            new = []
            for cond, s, v in out:
                for bcond, bev in ev[1]:
                    for c2, s2, v2 in expand_states(bev, s, v):
                        if cond is None:
                            c = c2 if c2 is not None else bcond
                        else:
                            c = cond + ' and ' + (c2 or bcond or 'true')
                        new.append((c, s2, v2))
            out = new
        else:
            nxt = []
            for cond, s, v in out:
                s2, v2, ok = apply_one(ev, s, v)
                if ok:
                    nxt.append((cond, s2, v2))
            if not nxt:
                return []
            out = nxt
    return out


def decode(st):
    u = bxor(st['F'], st['h'])
    L = u // 32
    op = u % 32
    e = L if st['q'] == st['F'] else (bxor(st['q'], st['h']) // 32)
    return L, op, e

def initial_state(canary=None):
    h = 226429
    if canary is None:
        canary = True
    if canary:
        return {'h': h, 'F': bxor(h, 42260423), 'q': bxor(42260423, h),
                'M': bxor(h, 62590010), 'f': bxor(62590010, h), 's': True}
    return {'h': h, 'F': 283305, 'q': 1260774,
            'M': bxor(h, 62590010), 'f': bxor(62590010, h), 's': True}

if __name__ == '__main__':
    src = open('/tmp/vm_while_inner.lua', encoding='utf-8', errors='replace').read()
    root = pickle.load(open('/tmp/vmtree.pkl', 'rb'))
    w = Walker(src, root)
    st = initial_state()
    seen = {}
    steps = 0
    chain = []
    while steps < 60:
        L, op, e = decode(st)
        key = (L, op, e)
        if key in seen:
            print('CYCLE back to', key, 'after', steps, 'steps')
            break
        seen[key] = steps
        path, kids = w.leaf_for(L, op, e)
        if kids is None:
            print('DEAD END at', key, 'step', steps)
            break
        txt = w.leaf_text(kids)
        chain.append((key, path[-1] if path else '?', txt))
        evs = parse_transitions(txt)
        st, ok = apply_events(evs, dict(st))
        if not ok:
            print('UNRESOLVABLE at step', steps); break
        steps += 1
    print('walked', steps, 'blocks')
    for i, (key, last, txt) in enumerate(chain[:12]):
        print('--- step %d key=%s op-path=%s' % (i, key, last))
        print('   ', txt[:220].replace('\n', ' '))
