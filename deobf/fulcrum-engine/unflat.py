#!/usr/bin/env python3
"""unflat.py — un-flatten Fulcrum two-register dispatch regions.

Grammar (validated on 440.txt):
  local base=NNN; local FLAG=true; local A,B,...=<init>;   -- dispatch regs
  while <FLAG|true> do
      if (A-base)==K1 [and (B-base)==K2 ...] then
          repeat
              <statements: literal assigns, decrypt calls, register shuffles,
               API calls, real ifs>
              base=base+JUNK
              FLAG=true
              A,B = base+K1', base+K2'      -- next block key (base cancels)
              SHADOW=A
          until <pretrue-flag or false>
      elseif ...
  end

Keys: (A-base, B-base) pairs resolve to constant ints (base cancels).
Walk the CFG from the init key, evaluate statements into a register store,
replace decrypt calls with decrypted strings, drop the junk (dispatch writes,
base advances, shuffle-only blocks), and emit structured Lua.
"""
import ast, json, re, sys
from pathlib import Path

sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import tool as T
from tool import literal, NonConstant, fulcrum_decrypt, DEC, parse_int_table, parse_arglist
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import lualex
from lualex import tokenize, P


# --------------------------------------------------------------- expression eval
class Sym:
    """Symbolic value: either concrete (int/str/list/bool/None) or opaque."""
    __slots__ = ('kind', 'val', 'text')

    def __init__(self, kind, val, text=''):
        self.kind = kind      # 'int','str','list','bool','nil','fn','opaque'
        self.val = val
        self.text = text

    def __repr__(self):
        return f'Sym({self.kind},{self.val})'


def sym_const(v):
    if isinstance(v, bool):
        return Sym('bool', v)
    if isinstance(v, int):
        return Sym('int', v)
    if isinstance(v, str):
        return Sym('str', v)
    if isinstance(v, list):
        return Sym('list', v)
    if v is None:
        return Sym('nil', None)
    return Sym('opaque', v)


def fold_expr(text, store, extras=None):
    if len(text) > 5000:
        return Sym('opaque', None, text)
    """Evaluate an expression against the register store.
    Returns Sym. Understands: ints, strings, tables of ints, names, indexing
    (a[1], aN[534][8][1]), arithmetic, #, comparisons, and/or/not, if-exprs,
    calls to bZ/cb/cc/ce (decrypt), function(...) -> 'fn'."""
    text = text.strip()
    if not text:
        return Sym('nil', None)
    if extras is None:
        extras = {}
    env = dict(store)
    env.update(extras)
    try:
        node = ast.parse(T.lua2py(text), mode='eval').body
    except SyntaxError:
        return Sym('opaque', None, text)
    return _ev(node, env, text)


def _keypath(n):
    """ast Subscript chain -> tuple of keys (ints/strings) or None."""
    keys = []
    while isinstance(n, ast.Subscript):
        k = n.slice
        if isinstance(k, ast.Constant) and isinstance(k.value, (int, str)):
            keys.append(k.value)
            n = n.value
        else:
            return None
    if isinstance(n, ast.Name):
        keys.append(n.id)
        return tuple(reversed(keys))
    return None


def _get(env, path):
    root = path[0]
    flat = root + ''.join('[%s]' % (k,) for k in path[1:])
    if flat in env:
        return ('hit', env[flat])
    if root not in env:
        return ('noroot', None)
    cur = env.get(root)
    for k in path[1:]:
        if isinstance(cur, Sym):
            if cur.kind == 'list' and isinstance(k, int) and 1 <= k <= len(cur.val):
                cur = cur.val[k - 1] if isinstance(cur.val[k-1], Sym) else sym_const(cur.val[k-1])
                continue
            if cur.kind == 'opaque' and isinstance(cur.val, dict) and k in cur.val:
                cur = cur.val[k]
                continue
            return ('hit', None)
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
            continue
        return ('hit', None)
    return ('hit', cur)


def _sig(v):
    if isinstance(v, Sym):
        if v.kind == 'list':
            return ('list', tuple(_sig(x) for x in v.val))
        return (v.kind, v.val)
    return ('raw', v)


def fold_inv(expr, store, base):
    """Fold expr; if the base cancels out, the two-eval trick yields a constant."""
    try:
        v0 = fold_expr(expr, store, {base: sym_const(0)})
        v1 = fold_expr(expr, store, {base: sym_const(1)})
        if v0.kind == v1.kind and v0.kind not in ('opaque', 'nil') and _sig(v0) == _sig(v1):
            return v0
    except Exception:
        pass
    return fold_expr(expr, store)


def _truthy(v):
    if v.kind == 'nil':
        return False
    if v.kind == 'bool':
        return bool(v.val)
    return True


def _ev(n, env, text):
    if isinstance(n, ast.Constant):
        return sym_const(n.value)
    if isinstance(n, ast.Name):
        if n.id in ('nil',):
            return Sym('nil', None)
        if n.id == 'true':
            return Sym('bool', True)
        if n.id == 'false':
            return Sym('bool', False)
        v = env.get(n.id)
        if isinstance(v, Sym):
            return v
        if n.id in KNOWN_GLOBALS:
            return Sym('fn', n.id)
        return Sym('nil', None)
    if isinstance(n, ast.Set):
        return Sym('list', [_ev(e, env, text) for e in n.elts])
    if isinstance(n, ast.Dict):
        if not n.keys and not n.values:
            return Sym('list', [])
        return Sym('opaque', None, text)
    if isinstance(n, ast.List):
        items = []
        for e in n.elts:
            v = _ev(e, env, text)
            if v.kind not in ('int', 'bool', 'nil', 'str'):
                items.append(v)   # allow opaque entries
            else:
                items.append(v)
        return Sym('list', items)
    if isinstance(n, ast.UnaryOp):
        v = _ev(n.operand, env, text)
        if isinstance(n.op, ast.Not):
            if v.kind in ('bool', 'nil'):
                return Sym('bool', not _truthy(v))
            return Sym('opaque', None, text)
        if isinstance(n.op, ast.USub) and v.kind == 'int':
            return Sym('int', -v.val)
        if isinstance(n.op, ast.UAdd) and v.kind == 'int':
            return v
        return Sym('opaque', None, text)
    if isinstance(n, ast.BinOp):
        a = _ev(n.left, env, text)
        b = _ev(n.right, env, text)
        if a.kind == 'int' and b.kind == 'int':
            if isinstance(n.op, ast.Add): return Sym('int', a.val + b.val)
            if isinstance(n.op, ast.Sub): return Sym('int', a.val - b.val)
            if isinstance(n.op, ast.Mult): return Sym('int', a.val * b.val)
            if isinstance(n.op, ast.FloorDiv): return Sym('int', a.val // b.val if b.val else 0)
            if isinstance(n.op, ast.Mod): return Sym('int', a.val % b.val if b.val else 0)
        return Sym('opaque', None, text)
    if isinstance(n, ast.Compare):
        a = _ev(n.left, env, text)
        res = True
        for op, comp in zip(n.ops, n.comparators):
            b = _ev(comp, env, text)
            if a.kind in ('int', 'bool', 'str', 'nil') and b.kind in ('int', 'bool', 'str', 'nil') and a.kind == b.kind:
                if isinstance(op, ast.Eq): ok = a.val == b.val
                elif isinstance(op, ast.NotEq): ok = a.val != b.val
                elif isinstance(op, ast.Lt): ok = a.val < b.val
                elif isinstance(op, ast.LtE): ok = a.val <= b.val
                elif isinstance(op, ast.Gt): ok = a.val > b.val
                elif isinstance(op, ast.GtE): ok = a.val >= b.val
                else: return Sym('opaque', None, text)
            else:
                return Sym('opaque', None, text)
            if not ok:
                return Sym('bool', False)
            a = b
        return Sym('bool', True)
    if isinstance(n, ast.BoolOp):
        vals = [_ev(v, env, text) for v in n.values]
        if all(v.kind in ('bool', 'nil') for v in vals):
            if isinstance(n.op, ast.And):
                return Sym('bool', all(_truthy(v) for v in vals))
            return Sym('bool', any(_truthy(v) for v in vals))
        if isinstance(n.op, ast.Or):
            for v in vals:
                if _truthy(v):
                    return v
            return vals[-1]
        if isinstance(n.op, ast.And):
            for v in vals:
                if not _truthy(v):
                    return v
            return vals[-1]
        return Sym('opaque', None, text)
    if isinstance(n, ast.Subscript):
        path = _keypath(n)
        if path:
            found, v = _get(env, path)
            if found == 'noroot':
                return Sym('nil', None)
            if isinstance(v, Sym):
                return v
            root = env.get(path[0])
            if isinstance(root, Sym) and root.kind == 'opaque':
                return Sym('opaque', None, text)
            return Sym('nil', None)
        return Sym('opaque', None, text)
    if isinstance(n, ast.Attribute):
        base = n.value
        if isinstance(base, ast.Name) and base.id in ('string', 'table', 'task', 'math', 'os', 'buffer', 'bit32', 'coroutine', 'utf8', 'game', 'Instance', 'Vector2', 'Vector3', 'CFrame', 'Color3', 'UDim2', 'Enum', 'self'):
            return Sym('fn', base.id + '.' + n.attr)
        return Sym('opaque', None, text)
    if isinstance(n, ast.Call):
        f = n.func
        fname = f.id if isinstance(f, ast.Name) else None
        if fname in FN_SYMS and not n.args and not getattr(n, 'keywords', []):
            return Sym('fn', fname)
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id in ('string','table','task','math','os','buffer','bit32','game','Instance') and not n.args:
            return Sym('fn', f.value.id + '.' + f.attr)
        if fname in DEC:
            args = [_ev(a, env, text) for a in n.args]
            if len(args) == 3 and args[0].kind == 'list' and args[1].kind == 'list' and args[2].kind == 'int':
                data = [x.val if isinstance(x, Sym) else None for x in args[0].val]
                key = [x.val if isinstance(x, Sym) else None for x in args[1].val]
                if all(isinstance(x, int) for x in data + key) and len(key) == 5:
                    try:
                        pt = fulcrum_decrypt(DEC[fname], data, key, args[2].val)
                        try:
                            s = pt.decode('utf-8')
                        except UnicodeDecodeError:
                            s = pt.decode('latin-1')
                        return Sym('str', s)
                    except Exception:
                        pass
            return Sym('opaque', None, text)
        # generic callee resolution via store (aN[15] -> 'bZ', aN[211] -> 'string.char')
        fnm = None
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id in ('string','table','math','os','task','buffer','bit32'):
            fnm = f.value.id + '.' + f.attr
        else:
            try:
                path = _keypath_str(ast.unparse(f))
            except Exception:
                path = None
            if path:
                res = _get(env, path)
                v = res[1] if isinstance(res, tuple) else res
                if isinstance(v, Sym) and v.kind == 'fn':
                    fnm = v.val
        if fnm in DEC:
            args = [_ev(a, env, text) for a in n.args]
            if len(args) == 3 and args[0].kind == 'list' and args[1].kind == 'list' and args[2].kind == 'int':
                data = [x.val if isinstance(x, Sym) else None for x in args[0].val]
                key = [x.val if isinstance(x, Sym) else None for x in args[1].val]
                if all(isinstance(x, int) for x in data + key) and len(key) == 5:
                    try:
                        pt = fulcrum_decrypt(DEC[fnm], data, key, args[2].val)
                        try:
                            s2 = pt.decode('utf-8')
                        except UnicodeDecodeError:
                            s2 = pt.decode('latin-1')
                        return Sym('str', s2)
                    except Exception:
                        pass
            return Sym('opaque', None, text)
        if fnm == 'string.char':
            args = [_ev(a, env, text) for a in n.args]
            if args and all(a.kind == 'int' for a in args):
                return Sym('str', ''.join(chr(a.val % 256) for a in args))
        if fnm == 'tonumber':
            args = [_ev(a, env, text) for a in n.args]
            if args and args[0].kind in ('int', 'str'):
                return args[0]
        return Sym('opaque', None, text)
    if isinstance(n, ast.IfExp):
        c = _ev(n.test, env, text)
        if c.kind in ('bool', 'nil'):
            return _ev(n.body if _truthy(c) else n.orelse, env, text)
        return Sym('opaque', None, text)
    return Sym('opaque', None, text)


# --------------------------------------------------------------- init loop (ba)
def eval_ba_tree(src):
    """Execute the outer `for ba=A,B,-7` dispatch tree concretely for every ba
    value; return (store, per_ba_slices)."""
    toks = tokenize(src)
    p = P(toks)
    while not (p.at('kw', 'for') and p.t[p.i + 1][1] == 'ba'):
        p.next()
    p.next()                    # 'for'
    p.expect('name')            # 'ba'
    p.expect('op', '=')
    v0 = p.peek()[2]; p.expr()
    a = T.literal(src[v0:p.t[p.i-1][2] + len(p.t[p.i-1][1])])
    p.expect('op', ',')
    v0 = p.peek()[2]; p.expr()
    b = T.literal(src[v0:p.t[p.i-1][2] + len(p.t[p.i-1][1])])
    step = -7
    if p.at('op', ','):
        p.next()
        v0 = p.peek()[2]; p.expr()
        step = T.literal(src[v0:p.t[p.i-1][2] + len(p.t[p.i-1][1])])
    p.expect('kw', 'do')
    body_start = p.peek()[2]
    p.block('end')
    p.expect('kw', 'end')
    body_end = p.t[p.i-1][2] + len(p.t[p.i-1][1])
    body = src[body_start:body_end]
    store = {}
    slices = {}
    vals = list(range(a, b + (1 if step > 0 else -1), step))
    for ba in vals:
        stmts = walk_ba_body(body, ba, store)
        slices[ba] = stmts
    return store, slices, vals


def literal_eval_ba(text, ba):
    """Fold an int expression that may reference `ba`."""
    class BV(ast.NodeTransformer):
        pass
    def walk(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, bool)):
            return n.value, {}
        if isinstance(n, ast.Name):
            if n.id == 'ba':
                return 0, {'ba': 1}
            return 0, {n.id: 1}
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            c, v = walk(n.operand)
            return (not c), v
        if isinstance(n, ast.BoolOp):
            vals = [walk(v) for v in n.values]
            if all(not v for _, v in vals):
                if isinstance(n.op, ast.And):
                    return all(c for c, _ in vals), {}
                return any(c for c, _ in vals), {}
            raise NonConstant()
        if isinstance(n, ast.Compare):
            a, x = walk(n.left)
            terms = dict(x)
            for op, comp in zip(n.ops, n.comparators):
                b, y = walk(comp)
                for k, v in y.items():
                    terms[k] = terms.get(k, 0) + v
                if isinstance(op, ast.Eq): ok = a == b
                elif isinstance(op, ast.NotEq): ok = a != b
                elif isinstance(op, ast.Lt): ok = a < b
                elif isinstance(op, ast.LtE): ok = a <= b
                elif isinstance(op, ast.Gt): ok = a > b
                elif isinstance(op, ast.GtE): ok = a >= b
                else: raise NonConstant()
                if not ok:
                    return False, {}
                a = b
            return True, {}
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            c, v = walk(n.operand)
            sgn = -1 if isinstance(n.op, ast.USub) else 1
            return c * sgn, {k: sgn * x for k, x in v.items()}
        if not isinstance(n, ast.BinOp):
            raise NonConstant()
        a, x = walk(n.left)
        b, y = walk(n.right)
        if isinstance(n.op, (ast.Add, ast.Sub)):
            sgn = -1 if isinstance(n.op, ast.Sub) else 1
            keys = x.keys() | y.keys()
            return a + sgn * b, {k: x.get(k, 0) + sgn * y.get(k, 0) for k in keys}
        if isinstance(n.op, ast.Mult):
            if any(x.values()) and any(y.values()):
                raise NonConstant()
            if any(x.values()):
                return a * b, {k: v * b for k, v in x.items()}
            return a * b, {k: v * a for k, v in y.items()}
        if isinstance(n.op, ast.FloorDiv):
            if not y and not x:
                return a // b, {}
            raise NonConstant()
        if isinstance(n.op, ast.Mod):
            if not y and not x:
                return a % b, {}
            raise NonConstant()
        raise NonConstant()
    try:
        n = ast.parse(T.lua2py(text.strip()), mode='eval').body
        c, terms = walk(n)
        for k, x in terms.items():
            if k == 'ba':
                c += x * ba
            elif x != 0:
                raise NonConstant()
        return c
    except Exception:
        return None


def canon_name(name, ba=None, env=None):
    """Canonicalize `aN[ba-350]` style names by folding the indices."""
    out = ''
    i = 0
    while i < len(name):
        ch = name[i]
        if ch == '[':
            j = name.index(']', i)
            inner = name[i+1:j]
            v = None
            if ba is not None:
                v = literal_eval_ba(inner, ba)
            if v is None and env is not None:
                sv = fold_expr(inner, env)
                if sv.kind == 'int':
                    v = sv.val
            if v is None:
                try:
                    v = int(inner)
                except ValueError:
                    return None
            out += '[%d]' % v
            i = j + 1
        else:
            out += ch
            i += 1
    return out


def walk_ba_body(body, ba, store):
    """Evaluate one ba-iteration: follow ba-pure ifs, collect other statements."""
    toks = tokenize(body)
    p = P(toks)
    collected = []
    _walk_ba_block(p, body, ba, store, collected)
    return collected


def _walk_ba_block(p, src, ba, store, collected):
    while True:
        t = p.peek()
        if t[0] == 'eof' or (t[0] == 'kw' and t[1] in ('end', 'else', 'elseif', 'until')):
            return
        if p.at('op', ';'):
            p.next(); continue
        if t[0] == 'kw' and t[1] == 'if':
            save = p.i
            p.next()               # skip 'if'
            c0 = p.peek()[2]
            p.expr()
            cond = src[c0:p.t[p.i-1][2] + len(p.t[p.i-1][1])]
            p.i = save
            try:
                from tool import bool_cond
                val = bool_cond(cond, ba)
            except NonConstant:
                val = None
                try:
                    val = bool_cond(cond, ba)
                except Exception:
                    val = None
            if val is True:
                p.expect('kw', 'if'); p.expr(); p.expect('kw', 'then')
                _walk_ba_block(p, src, ba, store, collected)
                if p.at_kw('elseif'):
                    while p.at_kw('elseif'):
                        p.next(); p.expr(); p.expect('kw', 'then')
                        p.block('elseif', 'else', 'end')
                if p.at_kw('else'):
                    p.next(); p.block('end')
                p.expect('kw', 'end')
                continue
            elif val is False:
                # skip this branch; handle elseif/else chains
                p.expect('kw', 'if'); p.expr(); p.expect('kw', 'then')
                p.block('elseif', 'else', 'end')
                taken = False
                while p.at_kw('elseif'):
                    p.next()
                    c0 = p.peek()[2]
                    p.expr()
                    cond = src[c0:p.t[p.i-1][2] + len(p.t[p.i-1][1])]
                    p.expect('kw', 'then')
                    cond = cond.strip()
                    if taken:
                        p.block('elseif', 'else', 'end')
                        continue
                    try:
                        from tool import bool_cond
                        v2 = bool_cond(cond, ba)
                    except Exception:
                        v2 = None
                    if v2 is True:
                        _walk_ba_block(p, src, ba, store, collected)
                        taken = True
                    else:
                        p.block('elseif', 'else', 'end')
                if p.at_kw('else'):
                    p.next()
                    if not taken:
                        _walk_ba_block(p, src, ba, store, collected)
                    else:
                        p.block('end')
                p.expect('kw', 'end')
                continue
            else:
                # non-ba condition: capture whole if as slice text
                s0 = p.peek()[2]
                p.stmt()
                e = p.t[p.i-1]
                collected.append(src[s0:e[2] + len(e[1])])
                continue
        # ordinary statement: capture + try to evaluate simple assignments
        s0 = p.peek()[2]
        p.stmt()
        e = p.t[p.i-1]
        stmt = src[s0:e[2] + len(e[1])]
        collected.append(stmt)
        m = re.match(r'\s*([A-Za-z_][A-Za-z_0-9]*(?:\[[^\]]+\])*)\s*=\s*(.+?)\s*$', stmt, re.S)
        if m:
            key = canon_name(m.group(1), ba)
            val = literal_eval_ba(m.group(2), ba)
            if val is not None and key:
                store[key] = sym_const(val)
    return


def main_init(path):
    src = open(path, encoding='utf-8', errors='replace').read()
    store, slices, vals = eval_ba_tree(src)
    print('ba values:', len(vals), vals[:5], '...', vals[-3:])
    print('store entries:', len(store))
    json.dump({k: (v.kind, v.val if v.kind in ('int', 'bool', 'nil') else str(v.val)[:60])
               for k, v in store.items() if isinstance(v, Sym)},
              open('init_store.json', 'w'), indent=1)
    nz = sum(1 for s in slices.values() if s)
    print('slices with statements:', nz)
    for ba in vals[:8]:
        print('ba', ba, '->', len(slices[ba]), 'stmts', [s[:40] for s in slices[ba][:2]])


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'init':
    main_init(sys.argv[2])


# --------------------------------------------------------------- region walker
JUNK_REGS = set()   # filled per region: base, flag, dispatch regs, shadow


def stmts_of_block(body):
    """Split a statement sequence robustly using the construct-stack tokenizer."""
    try:
        toks = tokenize(body)
    except Exception:
        return [body] if body.strip() else []
    spans = []
    prev_end = 0
    stack = []
    prev = None
    for tt in toks:
        w = tt[1]
        o = tt[2]
        if tt[0] == 'string':
            prev = w
            continue
        if not stack and prev is not None:
            _bound = False
            if w in ('local', 'return', 'break'):
                _bound = True
            elif w in ('if', 'for', 'while', 'repeat', 'function'):
                _expr_ctx = prev in ('=', '(', ',', '[', '~', 'and', 'or', 'not', 'return',
                                     '+', '-', '*', '/', '..', '<', '>', '<=', '>=', '==', '~=', '%', '#')
                _bound = not _expr_ctx
            if _bound:
                spans.append((prev_end, o))
                prev_end = o
        if w == 'if':
            expr_ctx = prev in ('=', '(', ',', '[', '~', 'and', 'or', 'not', 'return',
                                '+', '-', '*', '/', '..', '<', '>', '<=', '>=', '==', '~=', '%', '#')
            stack.append('expr-if' if expr_ctx else 'stmt-if')
        elif w in ('function', 'do'):
            stack.append('block')
        elif w == 'repeat':
            stack.append('loop')
        elif w in ('end', 'until'):
            if stack:
                stack.pop()
        elif w == 'else' and stack and stack[-1] == 'expr-if':
            stack.pop()
        elif w == ';' and not stack:
            spans.append((prev_end, o))
            prev_end = o + 1
        prev = w
    spans.append((prev_end, len(body)))
    out = []
    for a, b in spans:
        seg = body[a:b].strip()
        if seg:
            out.append(seg)
    return out


def eval_key_expr(text, base_name, store):
    """Evaluate `fD+1599997` style exprs -> key int (base coefficient must be 1
    or 0; returns the const with base subtracted)."""
    v0 = fold_expr(text, store, {base_name: sym_const(0)})
    v1 = fold_expr(text, store, {base_name: sym_const(1)})
    if v0.kind == 'int' and v1.kind == 'int':
        coeff = v1.val - v0.val
        return v0.val, coeff
    return None, None


def extract_terminator(stmts, A, B, base_name, store):
    """Find dispatch-register writes. Returns (kind, payload, kept_stmts).
    kind: 'goto' (pair), 'branch' (cond, pair1, pair2), 'return', 'none'."""
    kept = []
    gotos = []       # (cond_text or None, coarse, fine)
    retn = None
    i = 0
    n = len(stmts)
    while i < n:
        st = stmts[i]
        m = re.match(r'\s*(?:' + re.escape(A) + r')\s*,\s*(?:' + re.escape(B) + r')\s*=\s*(.+?)\s*,\s*(.+?)\s*$', st, re.S)
        if m:
            c1, k1 = eval_key_expr(m.group(1), base_name, store)
            c2, k2 = eval_key_expr(m.group(2), base_name, store)
            if c1 is not None and k1 == 1 and c2 is not None and k2 == 1:
                gotos.append((None, c1, c2))
                i += 1
                continue
        m2 = re.match(r'\s*(?:' + re.escape(A) + r')\s*=\s*(.+?)\s*;?\s*$', st, re.S)
        m3 = re.match(r'\s*(?:' + re.escape(B) + r')\s*=\s*(.+?)\s*;?\s*$', st, re.S)
        # separate single assignments A=..; B=.. possibly in sequence
        if m2 and not m3:
            c1, k1 = eval_key_expr(m2.group(1), base_name, store)
            # look ahead for B=...
            if i + 1 < n:
                m4 = re.match(r'\s*(?:' + re.escape(B) + r')\s*=\s*(.+?)\s*$', stmts[i + 1], re.S)
                if m4:
                    c2, k2 = eval_key_expr(m4.group(1), base_name, store)
                    if c1 is not None and k1 == 1 and c2 is not None and k2 == 1:
                        gotos.append((None, c1, c2))
                        i += 2
                        continue
            kept.append(st); i += 1
            continue
        if m3 and not m2:
            kept.append(st); i += 1
            continue
        if re.match(r'\s*return\b', st):
            retn = st
            i += 1
            continue
        kept.append(st)
        i += 1
    return gotos, retn, kept


# ---------------------------------------------------------------- exec + walk
KNOWN_GLOBALS = {'string', 'table', 'math', 'os', 'game', 'workspace', 'Instance',
                 'Vector3', 'CFrame', 'Color3', 'UDim2', 'task', 'debug', 'utf8',
                 'buffer', 'coroutine', 'pcall', 'xpcall', 'error', 'assert',
                 'tonumber', 'tostring', 'type', 'select', 'rawget', 'rawset',
                 'setmetatable', 'getmetatable', 'getfenv', 'setfenv', 'pairs',
                 'ipairs', 'next', 'unpack', 'require', 'wait', 'tick', 'time',
                 'print', 'warn', 'spawn', 'delay', 'typeof', 'newproxy', 'self',
                 'script', 'shared', '_G', '_VERSION'}

FN_SYMS = {
    'getfenv': 'getfenv', 'string': 'string', 'string.char': 'string.char',
    'string.format': 'string.format', 'string.sub': 'string.sub',
    'string.rep': 'string.rep', 'string.byte': 'string.byte',
    'string.gsub': 'string.gsub', 'string.find': 'string.find',
    'table.insert': 'table.insert', 'table.concat': 'table.concat',
    'table.remove': 'table.remove', 'tostring': 'tostring', 'tonumber': 'tonumber',
    'pcall': 'pcall', 'warn': 'warn', 'print': 'print', 'error': 'error',
    'setmetatable': 'setmetatable', 'rawset': 'rawset', 'rawget': 'rawget',
    'type': 'type', 'select': 'select', 'pairs': 'pairs', 'ipairs': 'ipairs',
    'next': 'next', 'assert': 'assert', 'unpack': 'unpack',
}


def emit_expr(text, store, names=None):
    """Rewrite an expression: fold/inline known values, resolve fn names.
    Returns the emitted Lua text."""
    v = fold_expr(text, store)
    return emit_sym(v, text, names)


def emit_sym(v, fallback, store=None, names=None):
    if v.kind == 'str':
        sv = v.val
        try:
            sv2 = sv.encode('latin-1').decode('utf-8')
            sv = sv2
        except Exception:
            pass
        return lua_quote(sv)
        return lua_quote(v.val)
    if v.kind == 'int':
        return str(v.val)
    if v.kind == 'bool':
        return 'true' if v.val else 'false'
    if v.kind == 'nil':
        return 'nil'
    if v.kind == 'fn':
        return v.val
    if v.kind == 'list':
        parts = []
        for item in v.val:
            if isinstance(item, Sym):
                parts.append(emit_sym(item, '?', store))
            else:
                parts.append('?')
        return '{' + ', '.join(parts) + '}'
    # opaque: try to rewrite sub-names mechanically
    return rewrite_names(fallback, store or {}, names)


def lua_quote(s):
    out = '"'
    for ch in s:
        if ch in '"\\':
            out += '\\' + ch
        elif ord(ch) < 32 or ord(ch) == 127:
            out += '\\%d' % ord(ch)
        else:
            out += ch
    return out + '"'


def rewrite_names(text, store, names=None):
    """Replace `aN[211]` etc with their known fn names; replace registers with
    their canonical names via `names` map."""
    def sub(m):
        key = m.group(0)
        if names and key in names:
            return names[key]
        res = _get(store, _keypath_str(key))
        v = res[1] if isinstance(res, tuple) else res
        if isinstance(v, Sym) and v.kind == 'fn':
            return v.val
        return key
    pat = re.compile(r'\b[A-Za-z_]\w*(?:\[\d+\])+|\b[A-Za-z_]\w*')
    return pat.sub(sub, text)


def _keypath_str(name):
    parts = re.findall(r'[A-Za-z_]\w*|\[\d+\]', name)
    out = []
    for p in parts:
        if p.startswith('['):
            out.append(int(p[1:-1]))
        else:
            out.append(p)
    return tuple(out)


def exec_stmt(st, store):
    """Execute one statement against the store.
    Returns (emitted_text_or_None, kind) where kind in
    ('plumbing','real','goto','return','branch','loopjunk','dead', 'guard')."""
    st = st.strip()
    if not st:
        return None, 'plumbing'
    # do ... end shuffle block
    if st.startswith('do ') or st.startswith('do;'):
        inner = st[3:-3] if st.endswith('end') else st[3:]
        for sub in stmts_of_block('do ' + inner + ' end') if False else [inner]:
            pass
        # execute inner assignments silently
        for sub_stmt in split_semicolons(inner):
            m = re.match(r'([A-Za-z_]\w*(?:\[\d+\])*)\s*=\s*(.+)$', sub_stmt.strip(), re.S)
            if m:
                lhs, rhs = m.group(1), m.group(2).strip()
                if rhs.startswith('local') or rhs.startswith('local '):
                    continue
                if re.match(r'^(dN|[a-z]{1,3}\[?\d*\]?)$', rhs) or True:
                    v = fold_expr(rhs, store)
                    if v.kind != 'opaque':
                        key = canon_name(lhs) or lhs
                        store[key] = v
        return None, 'plumbing'
    # dispatch-register / base writes
    if re.match(r'^(fD|fE|fF|fG|fH|fI|fJ|fK|cA|cB|cC|cD|dJ|dE|dG|fs|fr|cx|dL|cr|cs|ct|cu|cp|cq|cn|co|cj|ci|ck|cl|cm)\s*=', st):
        # might still be a real register! classification happens with region info
        pass
    return st, 'unknown'


def split_semicolons(text):
    out, depth, cur, instr = [], 0, '', None
    i = 0
    while i < len(text):
        ch = text[i]
        if instr:
            cur += ch
            if ch == '\\':
                if i + 1 < len(text):
                    cur += text[i+1]; i += 1
            elif ch == instr:
                instr = None
        elif ch in '"\'':
            instr = ch
            cur += ch
        elif ch in '({[':
            depth += 1; cur += ch
        elif ch in '})]':
            depth -= 1; cur += ch
        elif ch == ';' and depth <= 0:
            out.append(cur); cur = ''
        else:
            cur += ch
        i += 1
    if cur.strip():
        out.append(cur)
    return out


_TOKCACHE = {}
_TOKCAP = 12

def _tokcache_put(key, val):
    if len(_TOKCACHE) >= _TOKCAP:
        _TOKCACHE.clear()
    _TOKCACHE[key] = val



def split_if_statement(text, off=0):
    """Parse a top-level if-STATEMENT with elseif/else support.
    Returns (branches, else_body_text, else_off, end_at) where
    branches = [(cond, body_text, body_off), ...]; end_at = offset just past 'end'.
    Uses a construct stack so if-EXPRESSION then/else tokens are never confused
    with statement branch markers. None if text does not start with a statement-'if'."""
    try:
        toks = tokenize(text)
    except Exception:
        return None
    if not toks or toks[0][1] != 'if':
        return None
    # classify statement-'if' vs expression-'if' by predecessor
    prev = None
    kinds = []
    for tt in toks:
        if tt[0] == 'string':
            kinds.append(False)
            prev = tt[1]
            continue
        if tt[1] == 'if':
            expr_ctx = prev in ('=', '(', ',', '[', '~', 'and', 'or', 'not', 'return',
                                '+', '-', '*', '/', '..', '<', '>', '<=', '>=', '==', '~=', '%', '#')
            kinds.append(not expr_ctx)
        else:
            kinds.append(False)
        prev = tt[1]
    if not kinds[0]:
        return None
    stack = ['stmt-if']     # the token-0 statement if
    branches = []
    cond_start = toks[0][2] + 2
    then_at = None
    else_off = None
    end_at = None
    i = 0
    while i < len(toks):
        tt = toks[i]
        word = tt[1]
        o = tt[2]
        if tt[0] == 'string':
            i += 1
            continue
        if word == 'if':
            if i > 0:
                stack.append('stmt-if' if kinds[i] else 'expr-if')
        elif word in ('function', 'do'):
            stack.append('block')
        elif word == 'repeat':
            stack.append('loop')
        elif word in ('end', 'until'):
            if stack:
                stack.pop()
            if not stack:
                end_at = o + len(word)
                break
        elif word == 'then':
            if len(stack) == 1 and stack[0] == 'stmt-if':
                then_at = o + len(word)
        elif word == 'elseif':
            if len(stack) == 1:
                if cond_start is not None and then_at is not None:
                    branches.append((text[cond_start:then_at - 4].strip(), text[then_at:o], off + then_at))
                cond_start = o + len('elseif')
                then_at = None
            elif stack and stack[-1] == 'expr-if':
                pass  # elseif inside an if-expression
        elif word == 'else':
            if len(stack) == 1 and stack[0] == 'stmt-if':
                if cond_start is not None and then_at is not None:
                    branches.append((text[cond_start:then_at - 4].strip(), text[then_at:o], off + then_at))
                    cond_start = None
                then_at = then_at
                else_off = o + 4
                # the else-body runs until the root's end (handled below)
            elif stack and stack[-1] == 'expr-if':
                stack.pop()   # the if-expression's own else closes it
        i += 1
    if end_at is None:
        return None
    if cond_start is not None and then_at is not None:
        branches.append((text[cond_start:then_at - 4].strip(), text[then_at:end_at - 3], off + then_at))
    if not branches:
        return None
    else_body = text[else_off:end_at - 3] if else_off is not None else ''
    return branches, else_body, (off + else_off if else_off is not None else None), end_at


class ChainTree:
    """Pre-parsed dispatch chain for fast key lookups (text-based parser)."""

    def __init__(self, toks, src):
        self.toks = toks
        self.src = src
        self.vars = set()
        self.forms = set(re.findall(r'\((\w+)-(\w+)\)', src))
        self.root = self._parse(src, 0)

    def _parse(self, text, off):
        res = split_if_statement(text, off)
        if res is None:
            return ('leaf', (off, off + len(text)))
        branches, else_body, else_off, end_at = res
        # a body whose if-cond is NOT dispatch-shaped is a leaf (e.g. guard ifs)
        if not re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', branches[0][0] or ''):
            return ('leaf', (off, off + len(text)))
        out = []
        for cond, body, body_off in branches:
            disp = re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', cond) is not None
            if disp:
                out.append((cond, self._parse(body, body_off)))
            else:
                out.append((cond, ('leaf', (body_off, body_off + len(body)))))
        else_node = None
        if else_body is not None and else_body.strip():
            # else body may itself be a dispatch chain
            eres = split_if_statement(else_body, else_off) if else_off is not None else None
            if eres is not None and re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', eres[0][0][0] or ''):
                else_node = self._parse(else_body, else_off)
            else:
                else_node = self._parse(else_body, else_off) if eres is not None else ('leaf', (else_off or 0, (else_off or 0) + len(else_body)))
        return ('chain', out, else_node)

    def lookup(self, env, subs=None, plain_subs=None):
        node = self.root
        guard = 0
        while node[0] == 'chain' and guard < 64:
            guard += 1
            _, branches, else_body = node
            taken = None
            for cond, body in branches:
                if subs:
                    for k, val in subs.items():
                        cond = cond.replace(k, ' ' + val + ' ')
                if plain_subs:
                    for k, val in plain_subs.items():
                        cond = re.sub(r'\b' + re.escape(k) + r'\b', ' ' + str(val) + ' ', cond)
                v = fold_expr(cond, env)
                if v.kind == 'bool':
                    if v.val:
                        taken = body
                        break
                elif v.kind == 'nil':
                    if _truthy(v):
                        taken = body
                        break
                else:
                    return ('leaf', (0, 0)), 'OPAQUECOND:' + cond
            if taken is None:
                taken = else_body
            if taken is None:
                return ('leaf', (0, 0)), ''
            node = taken
        if node[0] == 'leaf':
            return node, self.src[node[1][0]:node[1][1]]
        return ('leaf', (0, 0)), ''


def find_leaf(tree_src, key1, key2, var1, var2, base=None, regvals=None, plain_subs=None):
    """Evaluate the dispatch if-chain with concrete keys; return leaf body."""
    tree = _TOKCACHE.get(('tree', id(tree_src)))
    if tree is None:
        toks = tokenize(tree_src)
        tree = ChainTree(toks, tree_src)
        _TOKCACHE[('tree', id(tree_src))] = tree
    subs = {}
    if regvals:
        for a, b in tree.forms:
            if a in regvals and b in regvals:
                subs['(%s-%s)' % (a, b)] = str(regvals[a] - regvals[b])
    elif base:
        subs['(%s-%s)' % (var1, base)] = str(key1)
        if var2:
            subs['(%s-%s)' % (var2, base)] = str(key2)
    env = {}
    node, text = tree.lookup(env, subs, plain_subs)
    return text


def _old_find_leaf(tree_src, key1, key2, var1, var2):
    toks = _TOKCACHE.get(tree_src)
    if toks is None:
        toks = tokenize(tree_src)
        _TOKCACHE[tree_src] = toks
    p = P(toks)
    env = {var1: sym_const(key1)}
    if var2:
        env[var2] = sym_const(key2)

    def cond_val(text):
        v = fold_expr(text, env)
        return v.val if v.kind == 'bool' else None

    def is_disp(pp):
        return (pp.peek(1)[0] == 'name' and pp.peek(1)[1] in (var1, var2)
                and pp.peek(2)[0] == 'op'
                and pp.peek(2)[1] in ('<=', '>=', '~=', '==', '<', '>'))

    def walk_chain():
        p.expect('kw', 'if')
        while True:
            c0 = p.peek()[2]
            p.expr()
            cond = tree_src[c0:p.t[p.i-1][2] + len(p.t[p.i-1][1])]
            p.expect('kw', 'then')
            val = cond_val(cond)
            if val is True:
                return take_body()
            p.block('elseif', 'else', 'end')
            if p.at_kw('elseif'):
                p.next()
                continue
            if p.at_kw('else'):
                p.next()
                return take_body()
            return ''

    def take_body():
        s0 = p.peek()[2]
        if p.at('kw', 'if') and is_disp(p):
            return walk_chain()
        p.block('elseif', 'else', 'end')
        e = p.t[p.i-1]
        return tree_src[s0:e[2] + len(e[1])]

    return walk_chain()


def region_vars(src):
    """Detect (base, A, B, flag, shadow) of a flattened region."""
    seen = re.findall(r'\((\w+)-(\w+)\)', src)
    base = A = B = flag = shadow = None
    pairs = []
    for a, b in seen:
        if base is None:
            base = b
        if b == base and a != base and a not in [p[0] for p in pairs]:
            pairs.append((a, b))
    if pairs:
        A = pairs[0][0]
        B = pairs[1][0] if len(pairs) > 1 else None
    m2 = re.search(r'while ([A-Za-z_]\w*|true) do', src)
    flag = m2.group(1) if m2 else 'true'
    if A:
        m3 = re.search(r'(\w+)\s*=\s*' + re.escape(A) + r'\s*[;,]', src)
        shadow = m3.group(1) if m3 else None
    return base, A, B, flag, shadow


WRAP_RE = re.compile(r'^(?:repeat)\b', re.S)


class Walker:
    def __init__(self, store, base, A, B, flag, shadow):
        self.store = dict(store)
        self.base, self.A, self.B = base, A, B
        self.flag, self.shadow = flag, shadow
        self._pairpend = {}
        self.emitted = []           # flat list of output lines (v1)
        self.warnings = []
        self.steps = 0
        self.cache_hits = set()

    # ---- statement execution
    def exec_body(self, body, out, depth=0):
        """Execute statements; collect gotos. Returns list of gotos."""
        stmts = stmts_of_block(body)
        return self.exec_stmts(stmts, out, depth)

    def exec_stmts(self, stmts, out, depth=0):
        gotos = []
        if depth > 30:
            return gotos
        i = 0
        while i < len(stmts):
            st = stmts[i].strip()
            if not st:
                i += 1; continue
            # repeat ... until COND  (one-shot unwrap)
            m = re.match(r'^repeat\b(.*)\buntil\s+(.+?)\s*$', st, re.S)
            if m:
                if re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', m.group(1)):
                    out.append(('call', st))
                    i += 1; continue
                cond = m.group(2)
                v = fold_expr(cond, self.store)
                if v.kind != 'bool' or not v.val:
                    self.warnings.append('repeat-until %r not pre-true; one-shot assumed' % cond[:40])
                inner = self.stmts_inside(m.group(1))
                gotos += self.exec_stmts(inner, out, depth + 1)
                i += 1; continue
            # do ... end block (shuffle or real)
            m = re.match(r'^do\b(.*)\bend\s*$', st, re.S)
            if m:
                inner = self.stmts_inside(m.group(1))
                gotos += self.exec_stmts(inner, out, depth + 1)
                i += 1; continue
            # while X do ... end
            m = re.match(r'^while\s+(.+?)\s+do\b(.*)\bend\s*$', st, re.S)
            if m:
                if re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', st):
                    out.append(('call', st))
                    i += 1; continue
                v = fold_expr(m.group(1), self.store)
                if v.kind == 'bool' and not v.val:
                    pass  # dead loop
                else:
                    self.warnings.append('while %r truthy: anti-emulation trap dropped' % m.group(1)[:40])
                i += 1; continue
            # if ... then ... else ... end
            if re.match(r'^if\b', st):
                g2 = self.exec_if(st, out, depth)
                gotos += g2
                i += 1; continue
            # return
            if re.match(r'^return\b', st):
                out.append(('return', st))
                i += 1; continue
            # plain statement
            g = self.exec_plain(st, out)
            gotos += g
            i += 1
        return gotos

    def stmts_inside(self, text):
        return stmts_of_block(text)

    def exec_if(self, st, out, depth):
        """Handle an if-statement via the robust split; folds, guards, branch terminators."""
        res = split_if_statement(st, 0)
        if res is None:
            out.append(('call', st))
            return []
        branches, else_body, _else_off, _end_at = res
        # region-shaped dispatch cond?  hand the whole statement to the emitter
        if depth > 0 and re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', branches[0][0] or ''):
            out.append(('call', st))
            return []
        # fold branch conds in order
        for cond, body, _bo in branches:
            v = fold_expr(cond, self.store)
            if v.kind == 'bool':
                if v.val:
                    return self.exec_body(body, out, depth + 1)
                continue
            if v.kind == 'nil' and _truthy(v):
                return self.exec_body(body, out, depth + 1)
            # non-foldable cond: dispatch-region body?  hand to the emitter as a subregion
            if depth > 0 and re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', cond or ''):
                out.append(('call', st))
                return []
            # non-foldable cond
            g_then = self.scan_gotos(body)
            g_else = self.scan_gotos(else_body) if else_body else []
            if g_then or g_else:
                out.append(('branch', cond, body, else_body))
                return [('branch', cond, g_then, g_else)]
            out.append(('if', cond, body, else_body))
            saved = dict(self.store)
            self.exec_body(body, [], depth + 1)
            st1 = dict(self.store)
            self.store = dict(saved)
            if else_body:
                self.exec_body(else_body, [], depth + 1)
            st2 = dict(self.store)
            self.store = dict(saved)
            for k in st1:
                if k in st2 and repr(st1[k].val) == repr(st2[k].val):
                    self.store[k] = st1[k]
            return []
        if else_body:
            return self.exec_body(else_body, out, depth + 1)
        return []

    def scan_gotos(self, body):
        """Find (A,B)= pair writes with foldable keys; return [(c1,c2), ...]."""
        gotos = []
        for st in stmts_of_block(body):
            st = st.strip()
            m = re.match(r'^' + re.escape(self.A) + r'\s*,\s*' + re.escape(self.B) + r'\s*=\s*(.+?)\s*,\s*(.+?)\s*$', st, re.S)
            if m:
                c1 = self.key_of(m.group(1))
                c2 = self.key_of(m.group(2))
                if c1 is not None and c2 is not None:
                    gotos.append((c1, c2))
        return gotos

    def key_of(self, expr):
        v0 = fold_expr(expr, self.store, {self.base: sym_const(0)})
        v1 = fold_expr(expr, self.store, {self.base: sym_const(1)})
        if v0.kind == 'int' and v1.kind == 'int' and v1.val - v0.val == 1:
            return v0.val
        return None

    def exec_plain(self, st, out):
        """One plain statement: plumbing vs real."""
        # multi-target assignment (register shuffles / phi merges): plumbing
        if re.match(r'^[A-Za-z_]\w*(?:\[\d+\])*\s*(?:,\s*[A-Za-z_]\w*(?:\[\d+\])*\s*)+=', st):
            lhs, rhs = st.split('=', 1)
            names = [x.strip() for x in lhs.split(',')]
            exprs = split_top_commas(rhs)
            if len(names) == len(exprs) and len(names) > 1 and self.A not in names and self.B not in names:
                vals = [fold_inv(e, self.store, self.base) for e in exprs]
                for nm, v in zip(names, vals):
                    self.store[canon_name(nm) or nm] = v
                return []
        # pair write?
        m = re.match(r'^' + re.escape(self.A) + r'\s*,\s*' + re.escape(self.B) + r'\s*(?:,\s*[A-Za-z_]\w*\s*)?=\s*(.+?)\s*,\s*(.+?)(?:\s*,\s*.+?)?$', st, re.S)
        if m:
            c1, c2 = self.key_of(m.group(1)), self.key_of(m.group(2))
            if c1 is not None and c2 is not None:
                return [('goto', c1, c2)]
            return []
        # single dispatch/base/flag/shadow writes
        m = re.match(r'^([A-Za-z_]\w*(?:\[\d+\])*)\s*=\s*(.+)$', st, re.S)
        if m:
            lhs, rhs = m.group(1), m.group(2).strip()
            key = canon_name(lhs) or lhs
            if lhs in (self.A, self.B, self.base, self.flag, self.shadow):
                try:
                    fv = fold_inv(rhs, self.store, self.base)
                except Exception:
                    fv = Sym('opaque', None, rhs)
                if lhs in (self.A, self.B):
                    k = self.key_of(rhs)
                    if k is not None:
                        self._pairpend[lhs] = k
                        self.store[key] = fv
                        if self.A in self._pairpend and self.B in self._pairpend:
                            g = [('goto', self._pairpend[self.A], self._pairpend[self.B])]
                            self._pairpend = {}
                            return g
                        return []
                self.store[key] = fv
                return []
            # guard `if X==nil` pattern handled in exec_if; here plain assign
            try:
                v = fold_inv(rhs, self.store, self.base)
            except Exception:
                v = Sym('opaque', None, rhs)
            self.store[key] = v
            if self.is_plumbing(lhs, v, rhs):
                return []
            out.append(('assign', lhs, rhs, v))
            return []
        out.append(('call', st))
        return []

    def is_plumbing(self, lhs, v, rhs):
        # register-style lhs with foldable value that is a shuffle temp = plumbing
        return False

    # ---- driver
    def run(self, chain_src, init1, init2, max_steps=3000):
        self._leafcache = {}
        queue = [(init1, init2)]
        out = []
        visited = set()
        while queue and self.steps < max_steps:
            self.steps += 1
            key = queue.pop(0)
            if key in visited:
                continue
            visited.add(key)
            regvals = getattr(self, 'regvals', None)
            if regvals is None:
                regvals = {self.base: 0}
                self.regvals = regvals
            regvals[self.A] = key[0]
            regvals[self.B] = key[1]
            sh = getattr(self, 'shadow_map', {})
            for shv, tgt in sh.items():
                if tgt in regvals:
                    regvals[shv] = regvals[tgt]
            ck = (key[0], key[1])
            leaf = self._leafcache.get(ck)
            if leaf is None:
                leaf = find_leaf(chain_src, key[0], key[1], self.A, self.B, self.base, regvals)
                self._leafcache[ck] = leaf
            if not leaf.strip():
                self.warnings.append('no leaf for key %r' % (key,))
                continue
            gotos = self.exec_body(leaf, out)
            for g in gotos:
                if isinstance(g, tuple) and len(g) == 2 and isinstance(g[0], int):
                    queue.append((g[0], g[1]))
                elif g[0] == 'goto':
                    queue.append((g[1], g[2]))
                elif g[0] == 'branch':
                    for (a, b) in (g[2] + g[3]):
                        queue.append((a, b))
        # sweep: execute every leaf the CFG walk did not reach (tree order)
        tree = _TOKCACHE.get(('tree', id(chain_src)))
        all_leaves = []
        if tree is not None:
            def _collect(node, outl):
                if node[0] == 'leaf':
                    outl.append(node[1])
                    return
                for _c, b in node[1]:
                    _collect(b, outl)
                if node[2]:
                    _collect(node[2], outl)
            _collect(tree.root, all_leaves)
        done_spans = set()
        for k in self._leafcache:
            lf = self._leafcache[k]
            done_spans.add(hash(lf))
        for (a, b) in sorted(all_leaves):
            txt = chain_src[a:b]
            if not txt.strip() or hash(txt) in done_spans:
                continue
            try:
                self.exec_body(txt, out)
            except Exception as e:
                self.warnings.append('sweep exec error: %r' % e)
        out.append(('end', None))
        return out


# --------------------------------------------------------------- top driver
def fn_body_span_fast(seg):
    """Given text starting at 'function(...)', return (params, body_span).
    Stack-based (robust against giant bodies that break p.block)."""
    toks = tokenize(seg)
    if not toks or toks[0][1] != 'function':
        raise ValueError('not a function')
    i = 1
    if toks[i][1] != '(':
        raise ValueError('no (')
    i += 1
    params = []
    while i < len(toks) and toks[i][1] != ')':
        if toks[i][1] != ',':
            params.append(toks[i][1])
        i += 1
    i += 1
    if i >= len(toks):
        raise ValueError('truncated')
    body_start = toks[i][2]
    prev = None
    stack = ['block']   # the function itself
    while i < len(toks):
        tt = toks[i]
        w = tt[1]
        if tt[0] == 'string':
            prev = w
            i += 1
            continue
        if w == 'if':
            expr_ctx = prev in ('=', '(', ',', '[', '~', 'and', 'or', 'not', 'return',
                                '+', '-', '*', '/', '..', '<', '>', '<=', '>=', '==', '~=', '%', '#')
            stack.append('expr-if' if expr_ctx else 'stmt-if')
        elif w in ('function', 'do'):
            stack.append('block')
        elif w == 'repeat':
            stack.append('loop')
        elif w in ('end', 'until'):
            stack.pop()
            if not stack:
                return params, (body_start, tt[2] + len(w))
        elif w == 'else' and stack and stack[-1] == 'expr-if':
            stack.pop()
        prev = w
        i += 1
    raise ValueError('unbalanced function body')


def fn_body_span_raw(seg):
    return fn_body_span_fast(seg)



    """Given text starting at 'function(...)', return (params, body_span)."""
    toks = tokenize(seg)
    p = P(toks)
    p.expect('kw', 'function')
    p.expect('op', '(')
    params = []
    while not p.at('op', ')'):
        if p.at('op', '...'):
            params.append('...')
            p.next()
        else:
            params.append(p.next()[1])
        if p.at('op', ','):
            p.next()
    p.expect('op', ')')
    body_start = p.peek()[2]
    p.block('end')
    body_end = p.t[p.i - 1][2] + len(p.t[p.i - 1][1])
    return params, (body_start, body_end)


def toplevel_stmts(src):
    toks = tokenize(src)
    p = P(toks)
    out = []
    while True:
        t = p.peek()
        if t[0] == 'eof':
            break
        if p.at('op', ';'):
            p.next(); continue
        if t[0] == 'kw' and t[1] in ('end', 'else', 'elseif', 'until', 'then', 'do', 'in'):
            break  # orphan structural token from a mid-statement cut: clean stop
        s0 = p.peek()[2]
        try:
            p.stmt()
        except Exception as e:
            msg = str(e)
            if msg.startswith('bad primary') and any(("'%s'" % k) in msg for k in
                    ('end', 'else', 'elseif', 'until', 'then', 'do', 'in')):
                break  # same as orphan token: clean stop
            out.append((s0, len(src), 'PARSE_ERROR: %s' % e))
            break
        e = p.t[p.i - 1]
        out.append((s0, e[2] + len(e[1]), None))
    return out


def run_init_loop(stmt, store, defs):
    """Run `for XX=A,B,K do <tree> end` in the store; collect function defs."""
    toks = tokenize(stmt)
    p = P(toks)
    p.expect('kw', 'for')
    var = p.next()[1]
    p.expect('op', '=')
    a0 = p.peek()[2]; p.expr()
    a = T.literal(stmt[a0:p.t[p.i-1][2] + len(p.t[p.i-1][1])])
    p.expect('op', ',')
    b0 = p.peek()[2]; p.expr()
    b = T.literal(stmt[b0:p.t[p.i-1][2] + len(p.t[p.i-1][1])])
    step = 1
    if p.at('op', ','):
        p.next()
        s0 = p.peek()[2]; p.expr()
        step = T.literal(stmt[s0:p.t[p.i-1][2] + len(p.t[p.i-1][1])])
    p.expect('kw', 'do')
    body_start = p.peek()[2]
    p.block('end')
    body_end = p.t[p.i-1][2] + len(p.t[p.i-1][1])
    body = stmt[body_start:body_end]
    vals = list(range(a, b + (1 if step > 0 else -1), step))
    for v in vals:
        _init_exec(body, v, var, store, defs)
    return store, defs


def _init_exec(body, v, var, store, defs):
    toks = tokenize(body)
    p = P(toks)
    _init_block(p, body, v, var, store, defs)


def _init_block(p, src, v, var, store, defs):
    from tool import bool_cond
    while True:
        t = p.peek()
        if t[0] == 'eof' or (t[0] == 'kw' and t[1] in ('end', 'else', 'elseif', 'until')):
            return
        if p.at('op', ';'):
            p.next(); continue
        if t[0] == 'kw' and t[1] == 'if':
            save = p.i
            p.next()
            c0 = p.peek()[2]
            p.expr()
            cond = src[c0:p.t[p.i-1][2] + len(p.t[p.i-1][1])]
            p.i = save
            try:
                val = bool_cond(cond, v)
            except Exception:
                val = None
            if val is True:
                p.expect('kw', 'if'); p.expr(); p.expect('kw', 'then')
                _init_block(p, src, v, var, store, defs)
                while True:
                    while p.at('op', ';'):
                        p.next()
                    if p.at_kw('elseif'):
                        p.next(); p.expr(); p.expect('kw', 'then')
                        p.block('elseif', 'else', 'end')
                        continue
                    break
                while p.at('op', ';'):
                    p.next()
                if p.at_kw('else'):
                    p.next(); p.block('end')
                while p.at('op', ';'):
                    p.next()
                p.expect('kw', 'end')
                continue
            elif val is False:
                p.expect('kw', 'if'); p.expr(); p.expect('kw', 'then')
                p.block('elseif', 'else', 'end')
                taken = False
                while True:
                    while p.at('op', ';'):
                        p.next()
                    if not p.at_kw('elseif'):
                        break
                    p.next()
                    c0 = p.peek()[2]
                    p.expr()
                    cond = src[c0:p.t[p.i-1][2] + len(p.t[p.i-1][1])]
                    p.expect('kw', 'then')
                    if taken:
                        p.block('elseif', 'else', 'end')
                        continue
                    try:
                        val = bool_cond(cond, v)
                    except Exception:
                        val = None
                    if val is True:
                        _init_block(p, src, v, var, store, defs)
                        taken = True
                    else:
                        p.block('elseif', 'else', 'end')
                while p.at('op', ';'):
                    p.next()
                if p.at_kw('else'):
                    p.next()
                    if not taken:
                        _init_block(p, src, v, var, store, defs)
                    else:
                        p.block('end')
                while p.at('op', ';'):
                    p.next()
                p.expect('kw', 'end')
                continue
            else:
                s0 = p.peek()[2]
                p.stmt()
                e = p.t[p.i-1]
                text = src[s0:e[2] + len(e[1])]
                _init_take(text, v, var, store, defs)
                continue
        s0 = p.peek()[2]
        p.stmt()
        e = p.t[p.i-1]
        text = src[s0:e[2] + len(e[1])]
        _init_take(text, v, var, store, defs)
    return


def _init_take(text, v, var, store, defs):
    m = re.match(r'\s*([A-Za-z_][A-Za-z_0-9]*(?:\[[^\]]+\])*)\s*=\s*(.+?)\s*$', text, re.S)
    if m and not m.group(2).startswith('function'):
        key = canon_name(m.group(1), v)
        val = literal_eval_ba(m.group(2), v)
        if val is not None and key:
            store[key] = sym_const(val)
            return
    if re.match(r'\s*\w+\s*=\s*function\b', text) or re.match(r'\s*function\b', text):
        defs.append(text)
        return
    # table inits and other junk: fold tables into the store, drop the rest
    m2 = re.match(r'\s*([A-Za-z_][A-Za-z_0-9]*(?:\[[^\]]+\])*)\s*=\s*\{', text)
    if m2:
        key = canon_name(m2.group(1), v) or m2.group(1)
        store[key] = Sym('opaque', None, 'table')
        return
    return


def fn_body_span(ay):
    """Given 'NAME=function(...)...end', return (params, body_span)."""
    toks = tokenize(ay)
    p = P(toks)
    p.expect('name')
    while p.at('op', '.') or p.at('op', ':'):
        p.next(); p.expect('name')
    if p.at('op', '='):
        p.next()
    p.expect('kw', 'function')
    p.expect('op', '(')
    params = []
    while not p.at('op', ')'):
        if p.at('op', '...'):
            params.append('...'); p.next()
        else:
            params.append(p.next()[1])
        if p.at('op', ','):
            p.next()
    p.expect('op', ')')
    body_start = p.peek()[2]
    p.block('end')
    body_end = p.t[p.i-1][2] + len(p.t[p.i-1][1])
    return params, (body_start, body_end)


def decompile_for_dispatch(vname, start, stop, step, body, store, out_lines, depth=0):
    """Execute a for-loop dispatch tree (if-tree over the loop var) concretely,
    one loop value at a time; emit the taken leaf statements in order."""
    w = Walker(store, vname, vname, vname, '', '')
    out_lines.append('-- for-dispatch over %s=%d..%d step %d' % (vname, start, stop, step))
    for val in range(start, stop + 1, step if step else 1):
        store[vname] = sym_const(val)
        w.store[vname] = sym_const(val)
        events = []
        try:
            w.exec_body(body, events)
        except Exception as e:
            out_lines.append('-- for-dispatch exec error: %r' % e)
            continue
        _vv = str(val)
        def _sub(txt):
            return _sub_protected(vname, _vv, txt)
        for ev in events:
            if ev[0] == 'assign':
                lhs, rhs = _sub(ev[1]), _sub(ev[2])
                if 'function' in rhs and len(rhs) > 1200:
                    out_lines.extend(splice_fns(lhs + ' = ' + rhs, w.store, depth + 1))
                else:
                    out_lines.append(emit_assign(lhs, rhs, w.store, ev[3]))
            elif ev[0] == 'call':
                st2 = _sub(ev[1])
                if 'function' in st2 and len(st2) > 1200:
                    out_lines.extend(splice_fns(st2, w.store, depth + 1))
                elif depth < 4 and re.match(r'^(while\s+true\s+do|repeat\b|if\b)', st2.strip()) and decompile_subregion(st2, w.store, out_lines, depth + 1):
                    pass
                else:
                    out_lines.append(emit_line(st2, w.store))
            elif ev[0] == 'if':
                out_lines.append('if %s then' % rewrite_stmt(_sub(ev[1]), w.store))
                for s2 in stmts_of_block(_sub(ev[2])):
                    out_lines.append('\t' + emit_line(s2, w.store))
                if ev[3]:
                    out_lines.append('else')
                    for s2 in stmts_of_block(_sub(ev[3])):
                        out_lines.append('\t' + emit_line(s2, w.store))
                out_lines.append('end')
            elif ev[0] == 'if':
                out_lines.append('if %s then' % rewrite_stmt(ev[1], w.store))
                for s2 in stmts_of_block(ev[2]):
                    out_lines.append('\t' + emit_line(s2, w.store))
                if ev[3]:
                    out_lines.append('else')
                    for s2 in stmts_of_block(ev[3]):
                        out_lines.append('\t' + emit_line(s2, w.store))
                out_lines.append('end')
    return True


def decompile_region(chain_src, store, params, out_lines, depth):
    """Walk one flattened dispatch region; append decompiled lines."""
    base, A, B, flag, shadow = region_vars(chain_src)
    if not base or not A:
        out_lines.append('-- UNPARSED REGION')
        return
    # init pair: look in store for A / B (set by `local A,B,...=...` handled by caller)
    init1 = store.get('__init_' + A)
    init2 = store.get('__init_' + B)
    if init1 is None or init2 is None:
        out_lines.append('-- REGION missing init pair (%s,%s)' % (A, B))
        return
    w = Walker(store, base, A, B, flag, shadow)
    # regvals: every dispatch var with an init key; shadow_map: same-init aliases
    inits = {}
    for k, v in store.items():
        if k.startswith('__init_') and isinstance(v, Sym) and v.kind == 'int':
            inits[k[7:]] = v.val
    regvals = {}
    for nm, kv in inits.items():
        regvals[nm] = kv
    regvals[base] = 0   # base is 0 in key-space; must win over any __init_base
    shadow_map = {}
    by_val = {}
    for nm, kv in sorted(inits.items()):
        if kv in by_val:
            shadow_map[nm] = by_val[kv]
        else:
            by_val[kv] = nm
    w.regvals = regvals
    w.shadow_map = shadow_map
    chain = chain_src.strip()
    try:
        events = w.run(chain, init1.val, init2.val)
    except Exception as e:
        out_lines.append('-- REGION WALK ERROR: %r' % e)
        return store
    for ev in events:
        if ev[0] == 'block':
            pass
        elif ev[0] == 'return':
            out_lines.append(emit_line(ev[1], w.store))
        elif ev[0] == 'if':
            out_lines.append('if %s then' % emit_expr(ev[1], w.store))
            for s in stmts_of_block(ev[2]):
                out_lines.append('\t' + emit_line(s, w.store))
            if ev[3]:
                out_lines.append('else')
                for s in stmts_of_block(ev[3]):
                    out_lines.append('\t' + emit_line(s, w.store))
            out_lines.append('end')
        elif ev[0] == 'assign':
            if 'function' in ev[2] and len(ev[2]) > 1200:
                out_lines.extend(splice_fns(ev[1] + ' = ' + ev[2], w.store, depth + 1))
            else:
                out_lines.append(emit_assign(ev[1], ev[2], w.store, ev[3]))
        elif ev[0] == 'call':
            if 'function' in ev[1] and len(ev[1]) > 1200:
                out_lines.extend(splice_fns(ev[1], w.store, depth + 1))
            elif depth < 4 and decompile_subregion(ev[1], w.store, out_lines, depth + 1):
                pass
            else:
                out_lines.append(emit_line(ev[1], w.store))
        elif ev[0] == 'fork':
            out_lines.append('-- branch: ' + repr(ev[1]))
        elif ev[0] == 'loopback':
            out_lines.append('-- loop back to %r' % (ev[1],))
        elif ev[0] == 'end':
            out_lines.append('-- region end')
    out_lines.extend('-- warn: ' + x for x in w.warnings)
    return w.store


_FN_NAMES = {}


def decompile_subregion(text, store, out_lines, depth=0):
    """Recurse into an inline dispatch region (while/repeat wrapper or bare chain)."""
    st = text.strip()
    m = re.match(r'^while\s+true\s+do\b(.*)\bend\s*;?$', st, re.S)
    if not m:
        m = re.match(r'^repeat\b(.*)\buntil\s+.+?\s*$', st, re.S)
    if m:
        inner = m.group(1)
    elif st.startswith('if') and re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', st):
        inner = st
    else:
        return False
    base, A, B, flag, shadow = region_vars(inner)
    if not base or not A or not B:
        return False
    bv = fold_expr(base, store)
    av = fold_expr(A, store)
    cv = fold_expr(B, store)
    if bv.kind == 'int' and av.kind == 'int' and cv.kind == 'int':
        init1 = av.val - bv.val
        init2 = cv.val - bv.val
    else:
        # derive the initial keys from the first (A,B)=pair write:
        #   A,B = c1 + base, c2 + base   (or any affine form in base)
        init1 = init2 = None

        def _affine_key(expr):
            k = fold_expr(expr, store, {base: sym_const(0)})
            kb = fold_expr(expr, store, {base: sym_const(1)})
            if k.kind == 'int' and kb.kind == 'int' and kb.val - k.val == 1:
                return k.val
            return None

        for stx in re.findall(r'[^;\n]+', inner):
            stx = stx.strip()
            m = re.match(r'^\s*' + re.escape(A) + r'\s*,\s*' + re.escape(B) +
                         r'\s*=\s*(.+?)\s*,\s*(.+?)\s*$', stx, re.S)
            if m:
                k1 = _affine_key(m.group(1))
                k2 = _affine_key(m.group(2))
                if k1 is not None and k2 is not None:
                    init1, init2 = k1, k2
                    break
            m1 = re.match(r'^\s*' + re.escape(A) + r'\s*=\s*(.+?)\s*$', stx, re.S)
            m2 = re.match(r'^\s*' + re.escape(B) + r'\s*=\s*(.+?)\s*$', stx, re.S)
            if m1 and init1 is None:
                k1 = _affine_key(m1.group(1))
                if k1 is not None:
                    init1 = k1
            if m2 and init2 is None:
                k2 = _affine_key(m2.group(1))
                if k2 is not None:
                    init2 = k2
            if init1 is not None and init2 is not None:
                break
        if init1 is None or init2 is None:
            return False
    regvals = {base: 0}
    for a, b in re.findall(r'\((\w+)-(\w+)\)', inner):
        for nm in (a, b):
            if nm not in regvals:
                v = fold_expr(nm, store, {base: sym_const(0)})
                if v.kind == 'int':
                    regvals[nm] = v.val
    w = Walker(store, base, A, B, flag, shadow)
    w.regvals = regvals
    shadow_map = {}
    by_val = {}
    for nm, kv in sorted(regvals.items()):
        if nm == base:
            continue
        if kv in by_val:
            shadow_map[nm] = by_val[kv]
        else:
            by_val[kv] = nm
    w.shadow_map = shadow_map
    out_lines.append('-- sub-region (%s,%s) base %s:' % (A, B, base))
    try:
        events = w.run(inner, init1, init2)
    except Exception as e:
        out_lines.append('-- sub-region walk error: %r' % e)
        return True
    for ev in events:
        if ev[0] == 'assign':
            if 'function' in ev[2] and len(ev[2]) > 1200:
                out_lines.extend(splice_fns(ev[1] + ' = ' + ev[2], w.store, depth + 1))
            else:
                out_lines.append(emit_assign(ev[1], ev[2], w.store, ev[3]))
        elif ev[0] == 'call':
            if 'function' in ev[1] and len(ev[1]) > 1200:
                out_lines.extend(splice_fns(ev[1], w.store, depth + 1))
            elif depth < 4 and decompile_subregion(ev[1], w.store, out_lines, depth + 1):
                pass
            else:
                out_lines.append(emit_line(ev[1], w.store))
        elif ev[0] == 'if':
            out_lines.append('if %s then' % rewrite_stmt(ev[1], w.store))
            for s2 in stmts_of_block(ev[2]):
                out_lines.append('\t' + emit_line(s2, w.store))
            if ev[3]:
                out_lines.append('else')
                for s2 in stmts_of_block(ev[3]):
                    out_lines.append('\t' + emit_line(s2, w.store))
            out_lines.append('end')
    return True


_SPLICE_CACHE = {}


def splice_fns(text, store, depth=0, name='anon'):
    """Decompile 'program bodies' (functions with literal-bound init loops) inside
    a raw statement. Returns a list of output lines."""
    if depth > 6 or 'function' not in text:
        return [rewrite_stmt(text, store)]
    ck = (hash(text), depth)
    if ck in _SPLICE_CACHE:
        return list(_SPLICE_CACHE[ck])
    prog_re = re.compile(r'\bfor\s+[A-Za-z_]\w*\s*=\s*-?\d+\s*,\s*-?\d+')
    spans = []
    for m in re.finditer(r'\bfunction\s*\(', text):
        pos = m.start()
        try:
            params, (b0, b1) = fn_body_span_fast(text[pos:])
        except Exception:
            continue
        b0 += pos
        b1 += pos
        body = text[b0:b1]
        # the init loop must be at the body's TOP LEVEL (before any nested function)
        first_fn = body.find('function(')
        if first_fn < 0:
            first_fn = len(body)
        if not prog_re.search(body[:first_fn]):
            continue
        spans.append((b0, b1, body, params))
    if not spans:
        # fallback: transitive loops (wrapper factory functions) -> deepest worker body
        for m in re.finditer(r'\bfunction\s*\(', text):
            pos = m.start()
            try:
                params, (b0, b1) = fn_body_span_fast(text[pos:])
            except Exception:
                continue
            b0 += pos
            b1 += pos
            body = text[b0:b1]
            if not prog_re.search(body):
                continue
            spans.append((b0, b1, body, params))
        spans.sort(key=lambda t: t[1] - t[0])
        keep = []
        for b0, b1, body, params in spans:
            if any(p0 >= b0 and p1 <= b1 for p0, p1 in [(k[0], k[1]) for k in keep]):
                continue
            keep.append((b0, b1, body, params))
        spans = keep
        if spans:
            # deepest only
            spans = spans[:1]
    if not spans:
        return [rewrite_stmt(text, store)]
    # outermost program bodies only (inner closures surface via their region walk)
    spans.sort(key=lambda t: t[1] - t[0], reverse=True)
    edits = []
    processed = []
    for b0, b1, body, params in spans:
        if any(b0 >= p0 and b1 <= p1 for p0, p1 in processed):
            continue
        processed.append((b0, b1))
        try:
            lines = decompile_fn(body, dict(store), params, name + '_fn%d' % len(edits))
        except Exception as e:
            lines = ['-- nested decompile error: %r' % e]
        edits.append((b0, b1, lines))
    edits.sort(key=lambda t: t[0])
    result = []
    cursor = 0
    for b0, b1, lines in edits:
        head = text[cursor:b0]
        if head.strip():
            emit_chunk(head, store, depth + 1, result)
        result.extend(lines)
        cursor = b1
    tail = text[cursor:]
    if tail.strip():
        emit_chunk(tail, store, depth + 1, result)
    _SPLICE_CACHE[ck] = list(result)
    return result


def emit_chunk(text, store, depth, out):
    """Emit a raw text chunk statement-by-statement with recursion."""
    if depth > 6:
        out.append(rewrite_stmt(text, store))
        return
    for st in stmts_of_block(text):
        if 'function' in st and len(st) > 1200:
            out.extend(splice_fns(st, store, depth + 1))
        elif re.match(r'^(while\s+true\s+do|repeat\b|if\b)', st) and re.search(r'\(\s*\w+\s*-\s*\w+\s*\)', st):
            if not decompile_subregion(st, store, out, depth + 1):
                out.append(emit_line(st, store))
        else:
            out.append(emit_line(st, store))


def _sub_protected(name, val, txt):
    """Substitute name -> val in expression text, NEVER in declaration name
    positions (`local a,b`, `for a =`, `function a`), and never on the LHS
    name of `name = ...` if it shadows... (LHS single-name kept raw)."""
    masks = []
    def _mask(m):
        masks.append(m.group(0))
        return '\x01%d\x01' % (len(masks) - 1)
    txt = re.sub(r'\blocal\s+[A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*', _mask, txt)
    txt = re.sub(r'\bfor\s+[A-Za-z_]\w*(?=\s*=)', _mask, txt)
    txt = re.sub(r'\bfunction\s+[A-Za-z_]\w*', _mask, txt)
    txt = re.sub(r'\b%s\b' % re.escape(name), val, txt)
    for i, m in enumerate(masks):
        txt = txt.replace('\x01%d\x01' % i, m)
    return txt


def _is_name_list(text):
    return all(x.strip() == '...' or re.match(r'^[A-Za-z_]\w*$', x.strip())
               for x in text.split(','))


def emit_assign(lhs, rhs, store, v=None):
    if v is None:
        v = fold_expr(rhs, store)
    canon = canon_name(lhs) or lhs
    return '%s = %s' % (canon, emit_sym(v, rhs, store))


def emit_line(st, store):
    return emit_expr(st, store) if False else rewrite_stmt(st, store)


def rewrite_stmt(st, store):
    """Rewrite a statement: inline folded subexpressions, resolve fn names."""
    # NEVER substitute into `local` declaration name lists (names, not values!)
    m = re.match(r'^(\s*local\s+)([^=]+?)(\s*=\s*)(.+)$', st, re.S)
    if m and _is_name_list(m.group(2)):
        rhs = m.group(4)
        return m.group(1) + m.group(2) + m.group(3) + emit_sym(fold_expr(rhs, store), rhs, store)
    m = re.match(r'^\s*local\s+[^=]*$', st)
    if m:
        return st
    # decrypt/known calls inside: handle `lhs = call(args)` shape
    m = re.match(r'\s*([A-Za-z_]\w*(?:\[\d+\])*)\s*=(?!=)\s*(.+)$', st, re.S)
    if m:
        return emit_assign(m.group(1), m.group(2), store)
    # return exprs
    m = re.match(r'\s*return\b\s*(.*)$', st, re.S)
    if m and m.group(1).strip():
        parts = [p.strip() for p in split_top_commas(m.group(1))]
        return 'return ' + ', '.join(emit_sym(fold_expr(p, store), p, store) for p in parts)
    return emit_sym(fold_expr(st, store), st, store)


def split_top_commas(text):
    out, depth, cur, instr = [], 0, '', None
    for ch in text:
        if instr:
            cur += ch
            if ch == instr: instr = None
        elif ch in '"\'':
            instr = ch; cur += ch
        elif ch in '({[':
            depth += 1; cur += ch
        elif ch in '})]':
            depth -= 1; cur += ch
        elif ch == ',' and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out


# --------------------------------------------------------------- function decompile
def decompile_fn(src, store, params=(), name='fn'):
    """Decompile one function BODY (src = body text). Returns output lines."""
    try:
        return _decompile_fn(src, store, params, name)
    except Exception as e:
        import traceback
        return ['-- DECOMPILE FN ERROR: %r' % e, '-- ' + traceback.format_exc().replace('\n', '\n-- ')]


def _decompile_fn(src, store, params=(), name='fn'):
    out = []
    store = dict(store)
    for pname in params:
        store[pname] = Sym('opaque', None, pname)
    stmts = toplevel_stmts(src)
    i = 0
    pending_locals = []
    while i < len(stmts):
        s0, s1, err = stmts[i]
        st = src[s0:s1]
        if err:
            out.append('-- PARSE ERROR: %s' % err)
            break
        stt = st.strip()
        import os
        if os.environ.get('UDEBUG'):
            print('STMT:', repr(stt[:70]), file=sys.stderr)
        # init loop (scratch) vs dispatch loop (if-tree over the loop var)
        m = re.match(r'^for\s+(\w+)\s*=\s*(-?\d+)\s*,\s*(-?\d+)\s*(?:,\s*(-?\d+))?\s+do\b(.*)\bend\s*$', stt, re.S)
        if m and len(m.group(5)) > 500:
            vname = m.group(1)
            start, stop = int(m.group(2)), int(m.group(3))
            step = int(m.group(4)) if m.group(4) else 1
            decompile_for_dispatch(vname, start, stop, step, m.group(5), store, out, 1)
            i += 1
            continue
        m = re.match(r'^for\s+(\w+)\s*=\s*-?\d+\s*,\s*-?\d+\s*(?:,\s*-?\d+)?\s*do\b', stt)
        if m:
            defs = []
            run_init_loop(st, store, defs)
            for d in defs:
                out.extend(handle_def(d, store))
            i += 1
            continue
        # scratch init `aN[..]={}` or `for cz=1,N do aN[..][cz]={}end`
        if re.match(r'^[\w\[\].]+\s*=\s*\{', stt) or re.match(r'^for\s+cz=', stt):
            # fold into store as opaque tables
            for mm in re.finditer(r'([A-Za-z_]\w*(?:\[\d+\])*)\s*=\s*\{', stt):
                key = canon_name(mm.group(1))
                if key:
                    store[key] = Sym('opaque', None, 'table')
            i += 1
            continue
        # local decls
        if stt.startswith('local '):
            m = re.match(r'^local\s+([\w,\s]+?)\s*=\s*(.+)$', stt, re.S)
            if os.environ.get('UDEBUG') and stt.startswith('local cC'):
                print('DECL MATCH:', bool(m), file=sys.stderr)
            if m:
                names = [x.strip() for x in m.group(1).split(',')]
                rhs = m.group(2)
                parts = split_top_commas(rhs)
                if len(parts) == len(names):
                    for nm, ex in zip(names, parts):
                        k1 = key_of_expr(ex, store)
                        if nm and k1 is not None:
                            store['__init_' + nm] = sym_const(k1)
                        v = fold_expr(ex, store)
                        store[nm] = v
                else:
                    v = fold_expr(rhs, store)
                    if len(names) == 1:
                        store[names[0]] = v
                    else:
                        for nm in names:
                            store[nm] = Sym('opaque', None, nm)
            else:
                for nm in re.findall(r'[A-Za-z_]\w*', stt[6:]):
                    if nm not in store:
                        store[nm] = Sym('nil', None)
            i += 1
            continue
        # dispatch region: `while X do` / `repeat ... until false`
        if re.match(r'^(while|repeat)\b', stt):
            chain = stt
            m2 = re.match(r'^while\s+.+?\s+do\b(.*)\bend\s*$', stt, re.S)
            if m2:
                chain = m2.group(1)
            else:
                m3 = re.match(r'^repeat\b(.*)\buntil\s+.+?\s*$', stt, re.S)
                if m3:
                    chain = m3.group(1)
            st2 = decompile_region(chain, store, params, out, 0)
            if st2:
                store = st2
            i += 1
            continue
        # function def
        if re.match(r'^\w+\s*=\s*function\b', stt) or stt.startswith('function'):
            out.extend(handle_def(st, store))
            i += 1
            continue
        # return
        if stt.startswith('return'):
            out.append(rewrite_stmt(stt, store))
            i += 1
            continue
        out.append(rewrite_stmt(stt, store))
        i += 1
    return out


def eval_key_expr_init(expr, store):
    v0 = fold_expr(expr, store)
    if v0.kind == 'int':
        return v0.val, 0
    return None, None


def key_of_expr(expr, store):
    """Fold `base+K` style exprs to K (base coefficient 1)."""
    # find base name candidates: names appearing in expr
    names = set(re.findall(r'[A-Za-z_]\w*', expr))
    for nm in names:
        if nm in FN_SYMS or nm in ('if', 'then', 'else', 'not', 'and', 'or', 'true', 'false', 'nil'):
            continue
        v0 = fold_expr(expr, store, {nm: sym_const(0)})
        v1 = fold_expr(expr, store, {nm: sym_const(1)})
        if v0.kind == 'int' and v1.kind == 'int' and v1.val - v0.val == 1:
            return v0.val
    v = fold_expr(expr, store)
    return v.val if v.kind == 'int' else None


def handle_def(d, store):
    """Handle `X=function(...)...end` — recursively decompile."""
    out = []
    m = re.match(r'\s*([A-Za-z_]\w*)\s*=\s*function\b', d)
    name = m.group(1) if m else None
    try:
        params, (b0, b1) = fn_body_span(d)
    except Exception as e:
        out.append('-- DEF PARSE ERROR %r' % e)
        out.append(d[:200])
        return out
    body = d[b0:b1]
    try:
        lines = decompile_fn(body, store, params, name or 'fn')
    except Exception as e:
        lines = ['-- DECOMPILE ERROR: %r' % e]
    head = ('local function %s(%s)' % (name or 'anon', ', '.join(params))) if name else ('local %s = function(%s)' % ('anon', ', '.join(params)))
    out.append(head)
    out.extend('\t' + l if l else l for l in lines)
    out.append('end')
    return out


def _find_vm_entry(src):
    """Locate the VM entry function for a Fulcrum-obfuscated file.

    Supports the known sample build (aY marker) and, generically, any build
    whose program is one giant `NAME=function(...)local ...` wrapper invoked
    through an alias at the end. Returns (name, offset) or (None, None)."""
    try:
        return 'aY', src.index('aY=function(...)local bb')
    except ValueError:
        pass
    # generic: the wrapper is invoked through an alias near the end (aJ = FN; return aJ(...))
    tail = src[-4000:]
    rm = re.search(r'return\s+([A-Za-z_]\w*)\(', tail)
    if rm:
        alias = rm.group(1)
        for am in re.finditer(r'(?<![\w.])%s\s*=\s*([A-Za-z_]\w*)\s*(?:$|\bend\b)' % alias, src):
            target = am.group(1)
            fm = re.search(r'(?<![\w.])%s=function\(...\)local\s+[A-Za-z_]\w*' % target, src)
            if not fm:
                continue
            try:
                params, (b0, b1) = fn_body_span(src[fm.start():])
            except Exception:
                continue
            if b1 - b0 > 2000:
                return target, fm.start()
    # fallback: the largest wrapper; skip nested defs inside an already-found span
    best = None
    for m in re.finditer(r'([A-Za-z_]\w*)=function\(...\)local\s+([A-Za-z_]\w*)', src):
        if best and m.start() < best[3]:
            continue
        try:
            params, (b0, b1) = fn_body_span(src[m.start():])
        except Exception:
            continue
        size = b1 - b0
        if best is None or size > best[0]:
            best = (size, m.group(1), m.start(), b1)
    if best and best[0] > 2000:
        return best[1], best[2]
    return None, None


def main_deobf(path, outpath, storepath='init_store.json'):
    """Staged deobfuscation: load the init store from JSON (low memory)."""
    src = open(path, encoding='utf-8', errors='replace').read()
    store = {}
    for k, (kind, val) in json.load(open(storepath)).items():
        store[k] = sym_const(val)
    vm_name, i = _find_vm_entry(src)
    if vm_name is None:
        raise RuntimeError('unsupported Fulcrum build: no VM entry function found (engine is derived from one known build)')
    seg = src[i:i + 708100]
    params, (b0, b1) = fn_body_span(seg)
    body = seg[b0:b1]
    out = ['-- deobfuscated by fulcrum_tool (using the fulcrum deobfuscation package:',
           '-- O/Q/U/V LCG string ciphers + affine constant folding)',
           '-- Fulcrum [polsec.net] loader (Polsec runtime)', '']
    out.append('local function %s(...)' % vm_name)
    lines = decompile_fn(body, store, params, vm_name)
    junk = sum(1 for l in lines if 'ERROR' in l or l.startswith('--'))
    if not lines or len(lines) < 30 or junk > max(2, len(lines) // 2):
        raise RuntimeError('unsupported Fulcrum build: this engine only covers the known Fulcrum build and this file uses a different variant')
    for l in lines:
        if l.startswith('\t'):
            out.append(l)
        else:
            out.append('\t' + l if l else l)
    out.append('end')
    out.append('')
    out.append('local aX = %s' % vm_name)
    out.append('return aX(...)')
    open(outpath, 'w').write('\n'.join(out) + '\n')
    print('lines:', len(out))
    print('output:', outpath)


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'deobf':
    main_deobf(sys.argv[2], sys.argv[3])
