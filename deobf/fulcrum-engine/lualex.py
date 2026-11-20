"""lualex.py - small Lua/Luau tokenizer + tolerant parser used by the
Fulcrum deobfuscation engine.

tokenize(src) -> list of tokens [kind, text, start, end]
    kind in {'kw','name','num','str','op','eof'}; start/end are character
    offsets into src; comments and whitespace produce no tokens.

P(toks) - parser helper with:
    .t tokens, .i index
    .at(kind, val) / .at_kw(word) / .next() / .peek(k) / .expect(kind, val)
    .expr()       parse (skip) one expression
    .stmt()       parse (skip) one statement
    .block(*kw)   parse statements until one of the terminator keywords

It understands standard Lua plus the Luau extensions the engine emits:
if-expressions (`if c then a else b`), compound assignments, `//`, and
bitwise operators.
"""
import re

KEYWORDS = {
    'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for', 'function',
    'goto', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat', 'return',
    'then', 'true', 'until', 'while',
}

_NUM_RE = re.compile(
    r'0[xX][0-9a-fA-F]+'
    r'|\d+\.\d*(?:[eE][+-]?\d+)?'
    r'|\.\d+(?:[eE][+-]?\d+)?'
    r'|\d+(?:[eE][+-]?\d+)?')
_NAME_RE = re.compile(r'[A-Za-z_]\w*')
_OPS3 = ('...', )
_OPS2 = ('..', '//', '<<', '>>', '==', '~=', '<=', '>=', '::',
         '+=', '-=', '*=', '/=', '%=', '^=', '..=')
_OPS1 = set('+-*/%^#=<>(){}[];:,.&|~')
_ESC = {'n': '\n', 't': '\t', 'r': '\r', 'a': '\a', 'b': '\b',
        'f': '\f', 'v': '\v', '\\': '\\', '"': '"', "'": "'"}


def _long_bracket(src, i):
    """If a long bracket starts at i, return (close_index_exclusive, level)."""
    m = re.match(r'\[(=*)\[', src[i:])
    if not m:
        return None
    level = m.group(1)
    close = ']' + level + ']'
    j = src.find(close, i + m.end())
    if j < 0:
        return len(src), level
    return j + len(close), level


def tokenize(src):
    toks = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in ' \t\r\n\f\v':
            i += 1
            continue
        if src.startswith('--', i):
            j = i + 2
            lb = _long_bracket(src, j) if j < n and src[j] == '[' else None
            if lb:
                i = lb[0]
            else:
                k = src.find('\n', j)
                i = n if k < 0 else k + 1
            continue
        if c == '[':
            lb = _long_bracket(src, i)
            if lb:
                toks.append(['str', src[i:lb[0]], i, lb[0]])
                i = lb[0]
                continue
        if c in '"\'':
            j = i + 1
            buf = []
            while j < n:
                ch = src[j]
                if ch == '\\':
                    if j + 1 >= n:
                        break
                    e = src[j + 1]
                    if e in _ESC:
                        buf.append(_ESC[e])
                        j += 2
                    elif e == 'x' and j + 3 < n + 1:
                        m = re.match(r'[0-9a-fA-F]{1,2}', src[j + 2:j + 4])
                        if m:
                            buf.append(chr(int(m.group(0), 16)))
                            j += 2 + len(m.group(0))
                        else:
                            buf.append(e)
                            j += 2
                    elif e.isdigit():
                        m = re.match(r'\d{1,3}', src[j + 1:])
                        buf.append(chr(int(m.group(0)) % 256))
                        j += 1 + len(m.group(0))
                    elif e == 'z':
                        k = j + 2
                        while k < n and src[k] in ' \t\r\n':
                            k += 1
                        j = k
                    elif e == '\n':
                        buf.append('\n')
                        j += 2
                    else:
                        buf.append(e)
                        j += 2
                elif ch == c:
                    j += 1
                    break
                elif ch == '\n':
                    break
                else:
                    buf.append(ch)
                    j += 1
            toks.append(['str', src[i:j], i, j])
            i = j
            continue
        m = _NUM_RE.match(src, i)
        if m and (c.isdigit() or (c == '.' and i + 1 < n and src[i + 1].isdigit())):
            toks.append(['num', m.group(0), i, m.end()])
            i = m.end()
            continue
        m = _NAME_RE.match(src, i)
        if m:
            w = m.group(0)
            toks.append(['kw' if w in KEYWORDS else 'name', w, i, m.end()])
            i = m.end()
            continue
        if src[i:i + 3] in _OPS3:
            toks.append(['op', src[i:i + 3], i, i + 3])
            i += 3
            continue
        if src[i:i + 2] in _OPS2:
            toks.append(['op', src[i:i + 2], i, i + 2])
            i += 2
            continue
        if c in _OPS1:
            toks.append(['op', c, i, i + 1])
            i += 1
            continue
        toks.append(['op', c, i, i + 1])
        i += 1
    toks.append(['eof', '', n, n])
    return toks


# binary operator precedence (Lua); .. and ^ are right-associative
_BINOP = {
    'or': 1, 'and': 2,
    '<': 3, '>': 3, '<=': 3, '>=': 3, '~=': 3, '==': 3,
    '|': 4, '~': 5, '&': 6, '<<': 7, '>>': 7,
    '..': 9,
    '+': 10, '-': 10,
    '*': 11, '/': 11, '//': 11, '%': 11,
    '^': 14,
}
_UNARY = ('not', '-', '#', '~')


class P:
    def __init__(self, toks):
        self.t = toks
        self.i = 0

    # ------------------------------------------------------------- helpers
    def tok(self, k=0):
        j = self.i + k
        if j >= len(self.t):
            j = len(self.t) - 1
        return self.t[j]

    def peek(self, k=0):
        return self.tok(k)

    def next(self):
        t = self.tok()
        if t[0] != 'eof':
            self.i += 1
        return t

    def at(self, kind, val=None):
        t = self.tok()
        if t[0] != kind:
            return False
        return val is None or t[1] == val

    def at_kw(self, word):
        t = self.tok()
        return t[0] == 'kw' and t[1] == word

    def expect(self, kind, val=None):
        t = self.tok()
        if t[0] != kind or (val is not None and t[1] != val):
            raise SyntaxError('expected %s %r, got %r' % (kind, val, t[:2]))
        self.i += 1
        return t

    # ---------------------------------------------------------- statements
    def block(self, *terms):
        while True:
            t = self.tok()
            if t[0] == 'eof':
                return
            if t[0] == 'kw' and t[1] in terms:
                return
            if t[0] == 'kw' and t[1] == ';':
                self.i += 1
                continue
            self.stmt()
            if t[0] == 'kw' and t[1] == 'return':
                return

    def stmt(self):
        t = self.tok()
        if t[0] == 'op' and t[1] == ';':
            self.next()
            return
        if t[0] == 'op' and t[1] == '::':
            self.next()
            self.expect('name')
            self.expect('op', '::')
            return
        if t[0] == 'kw':
            w = t[1]
            if w == 'if':
                self.if_stmt()
                return
            if w == 'while':
                self.next()
                self.expr()
                self.expect('kw', 'do')
                self.block('end')
                self.expect('kw', 'end')
                return
            if w == 'repeat':
                self.next()
                self.block('until')
                self.expect('kw', 'until')
                self.expr()
                return
            if w == 'for':
                self.for_stmt()
                return
            if w == 'do':
                self.next()
                self.block('end')
                self.expect('kw', 'end')
                return
            if w == 'function':
                self.next()
                self.expect('name')
                while self.at('op', '.') or self.at('op', ':'):
                    self.next()
                    self.expect('name')
                self.funcbody()
                return
            if w == 'local':
                self.next()
                if self.at_kw('function'):
                    self.next()
                    self.expect('name')
                    while self.at('op', '.') or self.at('op', ':'):
                        self.next()
                        self.expect('name')
                    self.funcbody()
                    return
                self.expect('name')
                while self.at('op', ','):
                    self.next()
                    self.expect('name')
                if self.at('op', '='):
                    self.next()
                    self.exprlist()
                return
            if w == 'return':
                self.next()
                t2 = self.tok()
                ends = ('end', 'else', 'elseif', 'until')
                if not (t2[0] == 'eof' or (t2[0] == 'kw' and t2[1] in ends)
                        or (t2[0] == 'op' and t2[1] == ';')):
                    self.exprlist()
                if self.at('op', ';'):
                    self.next()
                return
            if w == 'break':
                self.next()
                return
            if w == 'goto':
                self.next()
                self.expect('name')
                return
            raise SyntaxError('unexpected keyword %r in statement' % w)
        # expression statement: call or assignment
        self.suffixedexp()
        t2 = self.tok()
        if t2[0] == 'op' and t2[1] == ',':
            # multiple assignment targets: a, b, c = ...
            while t2[0] == 'op' and t2[1] == ',':
                self.next()
                self.suffixedexp()
                t2 = self.tok()
        if t2[0] == 'op' and (t2[1] == '=' or t2[1] in
                              ('+=', '-=', '*=', '/=', '%=', '^=', '..=')):
            self.next()
            self.exprlist()

    def if_stmt(self):
        self.expect('kw', 'if')
        self.expr()
        self.expect('kw', 'then')
        self.block('elseif', 'else', 'end')
        while self.at_kw('elseif'):
            self.next()
            self.expr()
            self.expect('kw', 'then')
            self.block('elseif', 'else', 'end')
        if self.at_kw('else'):
            self.next()
            self.block('end')
        self.expect('kw', 'end')

    def for_stmt(self):
        self.expect('kw', 'for')
        self.expect('name')
        if self.at('op', '='):
            self.next()
            self.expr()
            self.expect('op', ',')
            self.expr()
            if self.at('op', ','):
                self.next()
                self.expr()
            self.expect('kw', 'do')
            self.block('end')
            self.expect('kw', 'end')
            return
        while self.at('op', ','):
            self.next()
            self.expect('name')
        self.expect('kw', 'in')
        self.exprlist()
        self.expect('kw', 'do')
        self.block('end')
        self.expect('kw', 'end')

    # --------------------------------------------------------- expressions
    def exprlist(self):
        self.expr()
        while self.at('op', ','):
            self.next()
            self.expr()

    def expr(self):
        t = self.tok()
        if t[0] == 'kw' and t[1] == 'if':
            return self.if_expr()
        return self.subexpr(0)

    def subexpr(self, limit):
        t = self.tok()
        if t[0] == 'kw' and t[1] == 'not' or (t[0] == 'op' and t[1] in ('-', '#', '~')):
            self.next()
            self.subexpr(12)
        else:
            self.simpleexp()
        while True:
            t = self.tok()
            op = t[1] if t[0] in ('op', 'kw') else None
            if op is None or op not in _BINOP or _BINOP[op] <= limit:
                return
            self.next()
            if op in ('..', '^'):
                self.subexpr(_BINOP[op] - 1)
            else:
                self.subexpr(_BINOP[op])

    def simpleexp(self):
        t = self.tok()
        k = t[0]
        if k in ('num', 'str'):
            self.next()
            return
        if k == 'kw':
            if t[1] in ('nil', 'true', 'false'):
                self.next()
                return
            if t[1] == 'function':
                self.next()
                self.funcbody()
                return
            if t[1] == 'if':
                self.if_expr()
                return
            raise SyntaxError('unexpected %r in expression' % t[1])
        if k == 'op' and t[1] == '...':
            self.next()
            return
        if k == 'op' and t[1] == '{':
            self.tableconstructor()
            return
        self.suffixedexp()

    def primaryexp(self):
        t = self.tok()
        if t[0] == 'name':
            self.next()
            return
        if t[0] == 'op' and t[1] == '(':
            self.next()
            self.expr()
            self.expect('op', ')')
            return
        raise SyntaxError('unexpected %r in expression' % t[:2])

    def suffixedexp(self):
        self.primaryexp()
        while True:
            t = self.tok()
            if t[0] == 'op' and t[1] == '.':
                self.next()
                self.expect('name')
            elif t[0] == 'op' and t[1] == '[':
                self.next()
                self.expr()
                self.expect('op', ']')
            elif t[0] == 'op' and t[1] == ':':
                self.next()
                self.expect('name')
                self.callargs()
            elif t[0] == 'op' and t[1] in ('(', '{') or (t[0] == 'str'):
                self.callargs()
            else:
                return

    def callargs(self):
        t = self.tok()
        if t[0] == 'op' and t[1] == '(':
            self.next()
            if not self.at('op', ')'):
                self.exprlist()
            self.expect('op', ')')
            return
        if t[0] == 'op' and t[1] == '{':
            self.tableconstructor()
            return
        if t[0] == 'str':
            self.next()
            return
        raise SyntaxError('expected call arguments, got %r' % t[:2])

    def funcbody(self):
        self.expect('op', '(')
        if not self.at('op', ')'):
            if self.at('op', '...'):
                self.next()
            else:
                self.expect('name')
                while self.at('op', ','):
                    self.next()
                    if self.at('op', '...'):
                        self.next()
                    else:
                        self.expect('name')
        self.expect('op', ')')
        self.block('end')
        self.expect('kw', 'end')

    def tableconstructor(self):
        self.expect('op', '{')
        while not self.at('op', '}'):
            t = self.tok()
            if t[0] == 'op' and t[1] == '[':
                self.next()
                self.expr()
                self.expect('op', ']')
                self.expect('op', '=')
                self.expr()
            elif t[0] == 'name' and self.peek(1)[0] == 'op' and self.peek(1)[1] == '=':
                self.next()
                self.expect('op', '=')
                self.expr()
            else:
                self.expr()
            t = self.tok()
            if t[0] == 'op' and t[1] in (',', ';'):
                self.next()
            elif t[0] == 'op' and t[1] == '}':
                break
            else:
                raise SyntaxError('bad table separator %r' % t[:2])
        self.expect('op', '}')

    def if_expr(self):
        self.expect('kw', 'if')
        self.expr()
        self.expect('kw', 'then')
        self.expr()
        while self.at_kw('elseif'):
            self.next()
            self.expr()
            self.expect('kw', 'then')
            self.expr()
        if self.at_kw('else'):
            self.next()
            self.expr()
