"""tool.py - shared Fulcrum helpers for the deobfuscation engine.

- fulcrum_decrypt(alg, data, key, seed): the four O/Q/U/V LCG ciphers
- DEC: decryptor-function-name -> algorithm, learned from the known samples
- literal(text): evaluate a constant Lua numeric expression
- lua2py(text): translate a Lua expression to Python syntax for ast parsing
- parse_int_table / parse_arglist: small Lua-text parsers
"""
import ast
import re
import warnings
warnings.simplefilter("ignore", SyntaxWarning)

MOD = 1 << 24

# Decryptor function names seen in known samples, mapped to the cipher the
# function body implements (seed update + byte formula shapes).
DEC = {
    'bZ': 'O', 'cb': 'Q', 'cc': 'U', 'ce': 'V',
    'bO': 'O', 'bQ': 'Q', 'bU': 'U', 'bV': 'V',
    'f1': 'O', 'f2': 'Q', 'f3': 'U', 'f4': 'V',
}


class NonConstant(ValueError):
    """Raised when an expression is not a constant."""


def fulcrum_decrypt(algorithm, data, key, seed):
    """Decode one Fulcrum cipher run. algorithm in O/Q/U/V, key = 5 ints."""
    if algorithm not in 'OQUV' or len(algorithm) != 1:
        raise ValueError('algorithm must be one of O, Q, U, V')
    if len(key) != 5 or not all(isinstance(x, int) and not isinstance(x, bool) for x in key):
        raise ValueError('key must contain exactly five integers')
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError('seed must be an integer')
    if not all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x <= 255 for x in data):
        raise ValueError('data must contain byte values')
    a, b, c, d, e = key
    out = bytearray()
    for value in data:
        if algorithm == 'O':
            seed = (seed * a + b) % MOD
        elif algorithm == 'Q':
            seed = (seed * a + b * a) % MOD
        elif algorithm == 'U':
            seed = (seed * a - b) % MOD
        else:
            seed = (seed * a - b * a) % MOD
        f = seed + (seed // 256) * d + (seed // 65536) * e
        if algorithm == 'O':
            value = (value - f) * c
        elif algorithm == 'Q':
            value = value * c - f
        elif algorithm == 'U':
            value = (value + f) * c
        else:
            value = value * c + f
        out.append(value % 256)
    return bytes(out)


# ---------------------------------------------------------------- lua2py
def _mask_strings(text):
    """Replace string literals with placeholders; return (masked, table)."""
    table = []
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '"' or c == "'":
            j = i + 1
            while j < n:
                if text[j] == '\\':
                    j += 2
                    continue
                if text[j] == c:
                    j += 1
                    break
                j += 1
            table.append(text[i:j])
            out.append('\x00%d\x00' % (len(table) - 1))
            i = j
            continue
        m = re.match(r'\[(=*)\[', text[i:])
        if m:
            close = ']' + m.group(1) + ']'
            j = text.find(close, i + m.end())
            j = n if j < 0 else j + len(close)
            inner = text[i + m.end():j - len(close)] if j < n else text[i + m.end():]
            table.append('"' + inner.replace('\\', '\\\\').replace('"', '\\"') + '"')
            out.append('\x00%d\x00' % (len(table) - 1))
            i = j
            continue
        out.append(c)
        i += 1
    return ''.join(out), table


def _split_top(text, words):
    """Split masked text at top-level occurrences of the words in `words`,
    respecting (), {}, [] depth."""
    parts = []
    depth = 0
    start = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in '({[':
            depth += 1
        elif c in ')}]':
            depth -= 1
        elif depth == 0:
            for w in words:
                if text.startswith(w, i) \
                        and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == '_')) \
                        and (i + len(w) >= n or not (text[i + len(w)].isalnum() or text[i + len(w)] == '_')):
                    parts.append(text[start:i])
                    parts.append(w)
                    start = i + len(w)
                    i += len(w)
                    break
            else:
                i += 1
                continue
        i += 1
    parts.append(text[start:])
    return parts


def _ifexpr_to_ternary(seg):
    """Convert a Luau if-expression segment into a Python conditional."""
    parts = _split_top(seg, ('then', 'elseif', 'else'))
    head = re.sub(r'^\s*if\b', '', parts[0])
    toks = [head] + parts[1:]

    def parse(i):
        cond = toks[i].strip()
        if i + 1 >= len(toks) or toks[i + 1] != 'then':
            raise SyntaxError('malformed if-expression')
        body = toks[i + 2].strip() or 'None'
        j = i + 3
        if j < len(toks) and toks[j] == 'elseif':
            return '(%s if (%s) else %s)' % (body, cond, parse(j + 1))
        if j < len(toks) and toks[j] == 'else':
            alt = toks[j + 1].strip() or 'None'
            return '(%s if (%s) else %s)' % (body, cond, alt)
        return '(%s if (%s) else None)' % (body, cond)

    return parse(0)


def _ifexpr_extent(text, start):
    """End offset of the if-expression starting at `start`."""
    base = text.count('(', 0, start) + text.count('{', 0, start) + text.count('[', 0, start)
    base -= text.count(')', 0, start) + text.count('}', 0, start) + text.count(']', 0, start)
    depth = base
    seen_else = False
    i = start
    n = len(text)
    while i < n:
        c = text[i]
        if c in '({[':
            depth += 1
        elif c in ')}]':
            if depth == base:
                return i
            depth -= 1
        elif c in ',;' and depth == base and seen_else:
            return i
        elif depth == base:
            if text.startswith('else', i) and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == '_')):
                seen_else = True
        i += 1
    return n


_IF_RE = re.compile(r'(?<![\w_.])if(?![\w_])')


def lua2py(text):
    """Translate a Lua/Luau expression to Python expression syntax."""
    text = text.strip()
    if not text:
        raise SyntaxError('empty expression')
    masked, table = _mask_strings(text)
    tlist = []

    def put(s):
        tlist.append(s)
        return '\x01%d\x01' % (len(tlist) - 1)

    # Luau if-expressions are left untranslated: the reference pipeline does
    # not fold them (verified against deobfuscated_a.lua)
    masked = re.sub(r'(?<![\w_.])nil(?![\w_])', 'None', masked)
    masked = re.sub(r'(?<![\w_.])true(?![\w_])', 'True', masked)
    masked = re.sub(r'(?<![\w_.])false(?![\w_])', 'False', masked)
    masked = masked.replace('~=', '!=')
    masked = re.sub(r':\s*([A-Za-z_]\w*)\s*\(', r'.\1(', masked)
    masked = re.sub(r'(?<!\.)\.\.(?!\.)', '+', masked)
    masked = masked.replace('^=', '**=')
    masked = masked.replace('^', '**')
    masked = re.sub(r'#\s*([A-Za-z_]\w*(?:\s*\[[^\[\]]*\])*)', r'len(\1)', masked)
    # expand converted if-expressions, then string literals
    masked = re.sub(r'\x01(\d+)\x01', lambda m: tlist[int(m.group(1))], masked)
    masked = re.sub(r'\x00(\d+)\x00', lambda m: table[int(m.group(1))], masked)
    return masked


# --------------------------------------------------------------- literal
def _const_walk(n):
    if isinstance(n, ast.Constant) and type(n.value) is int:
        return n.value
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
        return -_const_walk(n.operand)
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.UAdd):
        return _const_walk(n.operand)
    if isinstance(n, ast.BinOp):
        a = _const_walk(n.left)
        b = _const_walk(n.right)
        if isinstance(n.op, ast.Add):
            return a + b
        if isinstance(n.op, ast.Sub):
            return a - b
        if isinstance(n.op, ast.Mult):
            return a * b
        if isinstance(n.op, ast.FloorDiv):
            return a // b
        if isinstance(n.op, ast.Mod):
            return a % b
        if isinstance(n.op, ast.Pow):
            return a ** b
    if isinstance(n, ast.Name):
        raise NonConstant('symbolic name %r' % n.id)
    raise NonConstant('not constant')


def literal(text):
    """Evaluate a constant Lua numeric expression; int result or NonConstant."""
    s = text.strip().rstrip(';').strip()
    if not s:
        raise NonConstant('empty')
    try:
        node = ast.parse(lua2py(s), mode='eval').body
    except (SyntaxError, ValueError) as e:
        raise NonConstant('unparsable %r' % s) from e
    v = _const_walk(node)
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if not isinstance(v, int):
        raise NonConstant('not an int')
    return v


# --------------------------------------------------------- small parsers
def parse_int_table(text):
    """Parse `{1,2,3}` (constant arithmetic allowed) into a list of ints."""
    s = text.strip()
    if not (s.startswith('{') and s.endswith('}')):
        raise ValueError('not a table literal')
    inner = s[1:-1].strip()
    if not inner:
        return []
    return [literal(part) for part in split_top_commas(inner)]


def split_top_commas(text):
    parts = []
    depth = 0
    start = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in '({[':
            depth += 1
        elif c in ')}]':
            depth -= 1
        elif c == ',' and depth == 0:
            parts.append(text[start:i])
            start = i + 1
        elif c == '"' or c == "'":
            j = i + 1
            while j < n:
                if text[j] == '\\':
                    j += 2
                    continue
                if text[j] == c:
                    break
                j += 1
            i = j
        i += 1
    parts.append(text[start:])
    return parts


def parse_arglist(text):
    """Split a call argument list on top-level commas; returns raw texts."""
    return [p.strip() for p in split_top_commas(text) if p.strip()]


_KW = ('and', 'or', 'not', 'true', 'false', 'nil')
_IDENT_RE = __import__('re').compile(r'[A-Za-z_][A-Za-z_0-9]*')


def bool_cond(cond, ba):
    """Evaluate a Lua if-condition over a known numeric loop value.

    Returns True/False, or None when the condition cannot be decided
    (unknown names, tables, calls). `ba` is the loop value, or a mapping
    of name -> value."""
    cond = (cond or '').strip()
    if not cond:
        return None
    if '[' in cond or ']' in cond or '.' in cond or ':' in cond:
        return None
    names = {m for m in _IDENT_RE.findall(cond) if m not in _KW}
    if len(names) > 1:
        return None
    py = cond.replace('~=', '!=')
    py = __import__('re').sub(r'\btrue\b', 'True', py)
    py = __import__('re').sub(r'\bfalse\b', 'False', py)
    py = __import__('re').sub(r'\bnil\b', 'None', py)
    env = {}
    if isinstance(ba, dict):
        if len(names) == 1:
            name = next(iter(names))
            if name not in ba:
                return None
            env[name] = ba[name]
        elif names:
            return None
    elif names:
        name = next(iter(names))
        if not isinstance(ba, (int, float)):
            return None
        env[name] = ba
    try:
        return bool(eval(py, {'__builtins__': {}}, env))
    except Exception:
        return None
