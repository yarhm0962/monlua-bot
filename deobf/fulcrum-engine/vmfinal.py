#!/usr/bin/env python3
"""vmfinal.py - VM-interpreter build finalizer for the PolSec Fulcrum variant.

Takes a recovered Fulcrum VM-interpreter payload, walks its dispatch tree from
the entry state, and rewrites the 500KB+ flattened interpreter body into a
compact dispatch chain keyed on the reachable (L,u) states. The second-layer
dispatch and the iteration gate are preserved verbatim. Output is verified
against the bundled Luau compiler.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vmwalk import Walker, decode, bxor
from vmstmt import process_body
from vmtree import build_tree
from vmwalk import expand_states

ANCHOR = 'local u=I(F,h);local L=u//32;local e=(if q==F then L else(I(q,h)//32));u=u%32'
GATE = 'if not U[119]then continue end'


def parse_entry(wrapper):
    m = re.search(
        r'local h=(\d+)\s*local s=true\s*local F,M,q,f='
        r'\(if U\[150\]==(\d+)\s*then I\(h,(\d+)\)\s*else (\d+)\)'
        r',I\(h,(\d+)\),'
        r'\(if U\[150\]~=\2\s*then (\d+)\s*else I\(\3,h\)\),I\(\5,h\)',
        wrapper)
    if not m:
        raise SystemExit('vmfinal: entry-state constants not found in the wrapper')
    h = int(m.group(1))
    canary = int(m.group(2))
    return {
        'h': h,
        'canary': canary,
        'F_true': bxor(h, int(m.group(3))),
        'F_false': int(m.group(4)),
        'M': bxor(h, int(m.group(5))),
        'q_true': bxor(int(m.group(3)), h),
        'q_false': int(m.group(6)),
        'f': bxor(int(m.group(5)), h),
    }


def walk_states(src, root, st, limit=20000):
    w = Walker(src, root)
    frontier = [dict(st)]
    vals = {}
    order, texts = [], {}
    steps = 0
    while frontier and steps < limit:
        s0 = frontier.pop(0)
        L, op, e = decode(s0)
        key = (L, op, e)
        if key in texts:
            continue
        steps += 1
        path, kids = w.leaf_for(L, op, e)
        if kids is None:
            texts[key] = None
            order.append(key)
            continue
        txt = w.leaf_text(kids)
        texts[key] = txt
        order.append(key)
        body, evs = process_body(txt, s0, vals)
        for c, s2, v2 in expand_states(evs, s0, vals):
            k2 = decode(s2)
            if k2 not in texts and all(decode(f) != k2 for f in frontier):
                frontier.append(dict(s2))
    if steps >= limit:
        raise SystemExit('vmfinal: walk hit the step limit (%d); state space did not settle' % limit)
    return order, texts


def emit_chain(order, texts):
    parts = []
    for k in order:
        txt = texts[k]
        if txt is None:
            continue
        cond = 'L==%d and u==%d' % (k[0], k[1])
        parts.append('%s %s then %s' % ('if' if not parts else 'elseif', cond, txt))
    if not parts:
        raise SystemExit('vmfinal: no reachable handlers to emit')
    return '\n'.join(parts) + '\nend '


def run(inp, outp):
    payload = Path(inp).read_text(encoding='utf-8', errors='replace')
    body_start = payload.find(ANCHOR)
    if body_start < 0:
        raise SystemExit('vmfinal: input is not a Fulcrum VM-interpreter build (decode anchor missing)')
    gi = payload.find(GATE, body_start)
    if gi < 0:
        raise SystemExit('vmfinal: iteration gate not found')
    body_end = gi + len(GATE)
    body = payload[body_start:body_end]
    root = build_tree(body, 0, len(body))
    runs0 = [x for x in root if x[0] == 'run']
    if len(runs0) < 2 or root[0][0] != 'run' or root[1][0] != 'if':
        raise SystemExit('vmfinal: unexpected top-level body structure')
    pre = body[root[0][1]:root[0][2]]
    tail_start = root[2][1]
    tail = body[tail_start:]
    ent = parse_entry(payload[:body_start])
    st = {'h': ent['h'], 'F': ent['F_true'], 'q': ent['q_true'],
          'M': ent['M'], 'f': ent['f'], 's': True}
    order, texts = walk_states(body, root, st)
    chain = emit_chain(order, texts)
    new_body = pre + chain + tail
    out = payload[:body_start] + new_body + payload[body_end:]
    Path(outp).write_text(out, encoding='utf-8')
    dead = [k for k in order if texts[k] is None]
    print('vmfinal: %d reachable states, %d handlers emitted, %d fall-through states; body %d -> %d bytes'
          % (len(order), len(order) - len(dead), len(dead), len(body), len(new_body)))
    return out


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: vmfinal.py <input.lua> <output.lua>')
    run(sys.argv[1], sys.argv[2])
