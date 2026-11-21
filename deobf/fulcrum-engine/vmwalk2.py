#!/usr/bin/env python3
"""vmwalk2.py — un-flattener for the PolSec Fulcrum variant (XOR-keyed dispatcher).

Streaming scanner (constant memory): strings with escapes, long-bracket
strings/comments, Luau if-expressions disambiguated from real previous token.
"""
import re

WORD = re.compile(r'[A-Za-z_]\w*')
LONG_OPEN = re.compile(r'\[(=*)\[')
OPENERS = ('while', 'for', 'function', 'if', 'repeat')

EXPR_OPS = {'=', '==', '~=', '<', '<=', '>', '>=', '+', '-', '*', '/', '%',
            '^', '..', ',', '(', '[', '{', '#'}
EXPR_WORDS = {'and', 'or', 'not', 'return'}

def _prev_is_expr(prev):
    """True when the token before 'if' puts it in expression position.

    Rule: an if-expression can only continue an UNFINISHED expression, and
    the only tokens that leave an expression unfinished are these operators
    and the expression keywords. Closers (')', ']', '}', end of a string)
    complete an expression, so a following 'if' starts a statement. A
    paren-depth approach fails here: `return(function(...) ... end)()` keeps
    depth > 0 across an entire function body of real if-statements.
    """
    if not prev:
        return False
    if prev in EXPR_WORDS:
        return True
    if prev[0].isalpha() or prev[0] == '_' or prev[0] == '"':
        return False
    return prev in EXPR_OPS


class Tok:
    __slots__ = ('kind', 's', 'e', 'w')
    def __init__(self, kind, s, e, w=None):
        self.kind = kind; self.s = s; self.e = e; self.w = w
    def __repr__(self):
        return 'Tok(%r,%d,%d,%r)' % (self.kind, self.s, self.e, self.w)

def tokens(text, lo=0, hi=None):
    """Yield Tok for meaningful tokens. Strings/comments skipped (opaque).
    Keyword 'if' tokens carry w='if-stmt' or 'if-expr' decided from context."""
    if hi is None: hi = len(text)
    i = lo
    prev = None
    EXPR_PREV = set('=(,[~and or not return +-*/ .. < > <= >= == ~= % # ^')
    while i < hi:
        c = text[i]
        if c in ' \t\r\n':
            i += 1; continue
        if c == '-' and i + 1 < hi and text[i+1] == '-':
            m = LONG_OPEN.match(text, i + 2)
            if m:
                close = ']' + m.group(1) + ']'
                j = text.find(close, m.end())
                i = (j + len(close)) if j >= 0 else hi
            else:
                j = text.find('\n', i)
                i = j + 1 if j >= 0 else hi
            continue
        if c == '"' or c == "'":
            q = c; j = i + 1
            while j < hi:
                d = text[j]
                if d == '\\': j += 2; continue
                if d == q or d == '\n': break
                j += 1
            i = min(j + 1, hi); prev = '"str"'; continue
        m = LONG_OPEN.match(text, i)
        if m:
            close = ']' + m.group(1) + ']'
            j = text.find(close, m.end())
            i = (j + len(close)) if j >= 0 else hi
            prev = '"str"'; continue
        m = WORD.match(text, i)
        if m:
            w = m.group(0)
            if w == 'if':
                w = 'if-expr' if _prev_is_expr(prev) else 'if-stmt'
            yield Tok('word', i, m.end(), w)
            i = m.end(); prev = m.group(0); continue
        j = i
        while j < hi and text[j] not in ' \t\r\n"\'()[]{}-' and not WORD.match(text, j) and not LONG_OPEN.match(text, j):
            j += 1
        if j == i: j = i + 1
        op = text[i:j]
        yield Tok('op', i, j, op)
        i = j
        prev = op

def scan_tree(text, lo, hi):
    """Walk statements in [lo,hi). Returns (events, leaves).
    events: list of ('if-cond', s, e) / ('branch', kind, s, e) nest pairs.
    Actually returns a flat list of leaf dicts:
      {'s','e','path':[(cond_s,cond_e)], 'depth':d} for branch bodies that
      contain no nested if-stmt/loop/function blocks at their own top level.
    Loops/for/function blocks are treated as opaque leaves too (kind recorded)."""
    leaves = []
    stack = []   # frames: ('stmt-if', cond_spans, branch_bodies) etc.
    path = []    # list of (cond_s, cond_e)
    prev_tok = None
    # We implement with explicit manual token iteration to keep spans.
    toks = tokens(text, lo, hi)
    cur = None
    def nxt():
        try:
            return next(toks)
        except StopIteration:
            return Tok('eof', hi, hi, '')
    t = nxt()
    while t.kind != 'eof':
        w = t.w
        if w == 'if-stmt':
            # collect condition: tokens until matching 'then' at this if's level
            depth_expr = 0
            cs, ce = None, None
            tt = nxt()
            while tt.kind != 'eof':
                if tt.w == 'if-stmt':
                    depth_expr += 1
                elif tt.w in ('then',):
                    if depth_expr == 0:
                        cs, ce = t.e, tt.s
                        break
                    depth_expr -= 1
                elif tt.w == 'do' and depth_expr == 0 and False:
                    pass
                tt = nxt()
            if cs is None:
                break
            stack.append(('if', (cs, ce), []))
            path.append((cs, ce))
            t = nxt()
            continue
        elif w in ('for', 'while', 'function', 'do'):
            stack.append((w, None, []))
            t = nxt()
            continue
        elif w == 'repeat':
            stack.append((w, None, []))
            t = nxt()
            continue
        elif w == 'elseif' or w == 'else':
            if stack and stack[-1][0] == 'if':
                # close current branch as leaf; path keeps the if-cond only
                f = stack[-1]
                if cur is not None:
                    leaves.append({'s': cur[0], 'e': cur[1], 'path': list(path), 'depth': len(stack)})
                cur = None
            t = nxt()
            continue
        elif w in ('end', 'until'):
            if stack:
                f = stack.pop()
                if f[0] == 'if':
                    if cur is not None:
                        leaves.append({'s': cur[0], 'e': cur[1], 'path': list(path), 'depth': len(stack)})
                        cur = None
                    path.pop()
            t = nxt()
            continue
        else:
            if cur is None:
                cur = [t.s, None]
            cur[1] = t.e
            t = nxt()
            continue
    if cur is not None and not stack:
        leaves.append({'s': cur[0], 'e': cur[1], 'path': list(path), 'depth': 0})
    return leaves
