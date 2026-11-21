#!/usr/bin/env python3
"""vmemit.py — two-pass CFG emitter for the PolSec Fulcrum variant."""
import re, sys, pickle
sys.path.insert(0, '/workspace/monlua-bot/deobf/fulcrum-engine')
from vmwalk import Walker, decode, initial_state, expand_states
from vmstmt import process_body, toks2
from vmwalk2 import tokens

RE_HJUNK = re.compile(r'\(h\+(\d+)\)-\(h\+(\d+)\)')

def fold_numeric(txt):
    def hcancel(m):
        return str(int(m.group(2)) - int(m.group(1)))
    txt = RE_HJUNK.sub(hcancel, txt)
    num = re.compile(r'\((-?\d+)\s*([+\-*])\s*(-?\d+)\)')
    prev = None
    for _ in range(12):
        if prev == txt: break
        prev = txt
        txt = num.sub(lambda m: str(eval('%d%s%d' % (int(m.group(1)), m.group(2), int(m.group(3))))), txt)
        txt = re.sub(r'\((-?\d+)\)', r'\1', txt)
    return txt

def has_toplevel_terminator(txt):
    depth = 0
    skip_do = False
    toks = toks2(txt)
    i = 0
    from vmstmt import skip_exprif
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
            if depth > 0: depth -= 1
        elif depth == 0 and w in ('return', 'break', 'continue'):
            return w
        i += 1
    return None

class Emitter:
    def __init__(self, src, root, limit=8000):
        self.src = src
        self.w = Walker(src, root)
        self.limit = limit

    def leaf_body(self, kids):
        parts = []
        prev = ''
        for x in kids:
            seg = self.src[x[1]:x[2]] if x[0] == 'run' else self.src[x[2]:x[3]]
            if parts and prev and seg and prev[-1].isalnum() and (seg[0].isalnum() or seg[0] == '_'):
                parts.append(' ')
            parts.append(seg)
            prev = seg
        return ''.join(parts)

    def explore(self):
        labels = {}
        blocks = {}
        order = []
        frontier = [(None, initial_state(), {})]
        notes = []
        steps = 0
        while frontier and steps < self.limit:
            cond_in, st, vals = frontier.pop(0)
            L, op, e = decode(st)
            key = (L, op, e)
            if key in labels:
                continue
            lbl = len(order)
            labels[key] = lbl
            order.append(key)
            path, kids = self.w.leaf_for(L, op, e)
            steps += 1
            if kids is None:
                blocks[lbl] = {'body': '-- dead end at key %r' % (key,), 'edges': [], 'term': 'dead'}
                continue
            txt = self.leaf_body(kids)
            body, evs = process_body(txt, st, vals)
            body = fold_numeric(body)
            term = has_toplevel_terminator(body)
            edges = []
            if term is None:
                succs = expand_states(evs, st, vals)
                if not succs:
                    edges = [('unresolvable-copy', None)]
                    notes.append('unresolvable state at block %d key %r' % (lbl, key))
                else:
                    seen = {}
                    for c, s2, v2 in succs:
                        L2, o2, e2 = decode(s2)
                        k2 = (L2, o2, e2)
                        if k2 in seen:
                            continue
                        seen[k2] = True
                        frontier.append((c, s2, v2))
                        edges.append((c, k2))
            blocks[lbl] = {'body': body, 'edges': edges, 'term': term, 'key': key, 'path': path}
        return labels, blocks, order, notes, steps

    def emit(self, labels, blocks, order):
        out = []
        for lbl in range(len(order)):
            key = order[lbl]
            b = blocks[lbl]
            out.append('::L%d::' % lbl)
            if b['body'].strip():
                out.append(b['body'])
            term = b.get('term')
            edges = b.get('edges', [])
            if term == 'return':
                continue
            if term == 'dead':
                continue
            if not edges:
                continue
            if edges[0][0] == 'unresolvable-copy':
                out.append('-- unresolvable channel copy; chain stops here')
                continue
            if len(edges) == 1 and edges[0][0] is None:
                out.append('goto L%d' % labels[edges[0][1]])
            elif all(e[0] is None for e in edges):
                out.append('goto L%d' % labels[edges[0][1]])
            else:
                parts = []
                for c, k2 in edges:
                    if c is None:
                        parts.append('else goto L%d' % labels[k2])
                    else:
                        parts.append('if %s then goto L%d' % (c, labels[k2]) if not parts else 'elseif %s then goto L%d' % (c, labels[k2]))
                if parts:
                    parts.append('end')
                out.append(' '.join(parts))
        return '\n'.join(out)

if __name__ == '__main__':
    src = open('/tmp/vm_while_inner.lua', encoding='utf-8', errors='replace').read()
    root = pickle.load(open('/tmp/vmtree.pkl', 'rb'))
    em = Emitter(src, root)
    labels, blocks, order, notes, steps = em.explore()
    text = em.emit(labels, blocks, order)
    open('/tmp/vm_chain_output.lua', 'w').write(text)
    print('blocks:', len(order), 'steps:', steps, 'bytes:', len(text))
    for n in notes[:10]:
        print('NOTE:', n)
    # edge stats
    branchy = sum(1 for b in blocks.values() if len(b.get('edges', [])) > 1)
    print('branching blocks:', branchy)
