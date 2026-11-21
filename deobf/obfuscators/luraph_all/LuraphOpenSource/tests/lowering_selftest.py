"""Regression test for the lowering back end (run by `node selftest.js`).

1. random control-flow graphs must lower without an exception and leave no
   `unstructured jump` stub;
2. a crashing readability pass must cost that function its tidying only
   (core/backend.py keeps the structured body), never raise.
"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "core"))

import ir as D            # noqa: E402
import luasym as S        # noqa: E402
from luasym import Const, Reg, Bin, Global   # noqa: E402
import backend            # noqa: E402
import idioms             # noqa: E402


class St:
    def __init__(self, k):
        self.k, self.mode, self.pc = k, k[0], k[1]

    def key(self, link):
        return self.k


def graph(rng, n):
    keys = [(0, i, 0) for i in range(n)]
    order = []
    for i, k in enumerate(keys):
        stmts = [D.Assign(Reg(rng.randrange(4)), Bin("Add", Reg(rng.randrange(4)), Const(rng.randrange(9))))]
        if rng.random() < .4:
            stmts.append(D.CallStmt("%d" % i, Global("print"), S.Multi([Const(i)])))

        def nxt():
            return D.Node([], outcome=D.Next(St(keys[rng.randrange(n)])))
        r = rng.random()
        if i == n - 1 or r < .12:
            node = D.Node(stmts, outcome=D.Ret(S.Multi([Reg(0)])))
        elif r < .55:
            node = D.Node(stmts, cond=Bin("CompareLt", Reg(rng.randrange(4)), Const(rng.randrange(20))),
                          then=nxt(), els=nxt())
        else:
            node = D.Node(stmts, outcome=D.Next(St(keys[rng.randrange(n)])))
        order.append((k, node))
    return keys[0], order


def lower(seed):
    rng = random.Random(seed)
    entry, order = graph(rng, random.Random(seed).randrange(5, 30))
    return backend.lower(entry, order, D, None, "r", {}, lambda x, names: None)


bad = 0
for seed in range(120):
    try:
        lines = lower(seed)[0]
    except Exception as ex:
        print("FAIL  seed %d raised %s: %s" % (seed, type(ex).__name__, ex))
        bad += 1
        continue
    if any("unstructured jump" in l for l in lines):
        print("FAIL  seed %d left an unstructured-jump stub" % seed)
        bad += 1
print("%s  120 random CFGs lowered, no exception, no goto stub" % ("PASS" if not bad else "FAIL"))

orig = idioms.and_or
idioms.and_or = lambda b: (_ for _ in ()).throw(KeyError("injected"))
try:
    lines = lower(3)[0]
    ok = bool(lines)
except Exception as ex:
    ok = False
    print("      guard raised", type(ex).__name__, ex)
finally:
    idioms.and_or = orig
print("%s  a failing readability pass does not abort the function" % ("PASS" if ok else "FAIL"))
sys.exit(0 if (ok and not bad) else 1)
