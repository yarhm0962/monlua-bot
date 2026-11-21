#!/usr/bin/env python3
"""vmtree.py — dispatch-tree builder for the PolSec Fulcrum variant."""
import re, json, sys
from vmwalk2 import tokens

DISP_CHARS = re.compile(r'^[Lue][0-9=!<>~() ]*[!]=?[0-9]+.*$')  # unused
IDENT = re.compile(r'\b(?!L\b|u\b|e\b)[A-Za-z_]\w*\b')

OK_WORDS = {'and', 'or', 'not', 'nil', 'true', 'false'}

def is_disp(cond):
    """Dispatch condition iff only L/u/e identifiers, digits, comparisons, and/or/not."""
    if not re.search(r'\b[Lue]\b', cond):
        return False
    for m in re.finditer(r'[A-Za-z_]\w*', cond):
        w = m.group(0)
        if w in ('L', 'u', 'e') or w in OK_WORDS:
            continue
        return False
    return True

def build_tree(src, lo, hi):
    """Single pass; returns root children list.
    Nodes: ('if', node) dispatch ifs with node={'cond','branches':[(cond,children)],'else',...}
           ('run', s, e) statement run (belongs to the innermost dispatch branch)
           ('opaque', w, s, e) opaque construct recorded in place."""
    IT = tokens(src, lo, hi)
    def nxt():
        try: return next(IT)
        except StopIteration: return None
    def read_cond(after):
        sub = []
        cs = after
        while True:
            t = nxt()
            if t is None: return None, None
            if t.w == 'if-expr': sub.append('e')
            elif t.w == 'if-stmt': sub.append('i')
            elif t.w in ('function', 'do', 'repeat', 'for', 'while'): sub.append('b')
            elif t.w == 'else':
                if sub and sub[-1] == 'e': sub.pop()
                elif not sub: return None, None
            elif t.w in ('end', 'until'):
                if sub: sub.pop()
                else: return None, None
            elif t.w == 'then':
                if not sub: return cs, t.s
    root = []
    stack = []        # ['if', node, branch_start] / ['opaque', w]
    cur_target = root  # list receiving runs (innermost dispatch branch or root)
    branch_of = {}     # id(node) -> current branch children list
    skip_do = False
    cur = None
    def close_run(endpos):
        nonlocal cur
        if cur is not None:
            cur_target.append(('run', cur[0], endpos))
            cur = None
    def skip_exprif_gen(first):
        """Consume an if-expression's tokens; return the FIRST token after it,
        UNCONSUMED, so the caller (main loop or an enclosing skip) processes it.

        pd counts parens opened within this if-expression; the expression ends
        at the first closer/separator seen at pd == 0 after the else branch.
        bd tracks nested function expressions (their 'end' must not terminate).
        Nested if-expressions recurse and hand their terminator back the same way.
        """
        seen_then = seen_else = False
        pd = 0
        bd = 0
        t2 = first
        last_e = t2.e
        t2 = nxt()
        if t2 is None:
            cur_extend(last_e)
            return None
        while True:
            w2 = t2.w
            if w2 == 'if-expr':
                t2 = skip_exprif_gen(t2)
                if t2 is None:
                    cur_extend(last_e)
                    return None
                w2 = t2.w
            term = False
            if pd == 0 and bd == 0:
                if not seen_then:
                    if w2 == 'then':
                        seen_then = True
                    elif w2 in ('end', ';', 'until', 'do', 'elseif'):
                        term = True
                elif not seen_else:
                    if w2 == 'else':
                        seen_else = True
                    elif w2 in ('end', ';', 'until', 'do', 'elseif'):
                        term = True
                else:
                    if w2 in (';', ',', ')', ']', '}', 'end', 'elseif', 'else', 'do', 'until', 'then'):
                        term = True
            if term:
                cur_extend(last_e)
                return t2
            if w2 in ('(', '[', '{'):
                pd += 1
            elif w2 in (')', ']', '}'):
                pd = max(0, pd - 1)
            elif w2 == 'function':
                bd += 1
            elif w2 == 'end' and bd > 0:
                bd -= 1
            last_e = t2.e
            t2 = nxt()
            if t2 is None:
                cur_extend(last_e)
                return None

    def cur_extend(pos):
        """Extend the current run to include pos (expr-if tail belongs to body)."""
        nonlocal cur
        if cur is not None:
            cur[1] = pos

    t = nxt()
    while t is not None:
        w = t.w
        if w == 'if-expr':
            if cur is None: cur = [t.s, None]
            t = skip_exprif_gen(t)
            if t is None: break
            continue
        if w == 'if-stmt':
            cs, ce = read_cond(t.e)
            if ce is None: break
            cond = re.sub(r'\s+', ' ', src[cs:ce]).strip()
            disp = is_disp(cond)
            if disp:
                close_run(t.s)
                node = {'cond': cond, 'branches': [], 'else': None, 'pos': t.s, 'cpos': (cs, ce)}
                cur_target.append(('if', node))
                stack.append(['if', node, cur_target])
                cur_target = []
                node['branches'].append([cond, cur_target])
                cur = [ce + 4, None]
            else:
                stack.append(['opaque', 'if'])
            t = nxt(); continue
        if w == 'elseif':
            if stack and stack[-1][0] == 'if':
                close_run(t.s)
                f = stack[-1]
                cs, ce = read_cond(t.e)
                if ce is None: break
                cond = re.sub(r'\s+', ' ', src[cs:ce]).strip()
                cur_target = []
                f[1]['branches'].append([cond, cur_target])
                cur = [ce + 4, None]
            t = nxt(); continue
        if w == 'else':
            if stack and stack[-1][0] == 'if':
                close_run(t.s)
                f = stack[-1]
                cur_target = []
                f[1]['else'] = cur_target
                cur = [t.e, None]
            t = nxt(); continue
        if w in ('end', 'until'):
            close_run(t.s)
            if stack:
                f = stack.pop()
                if f[0] == 'if':
                    cur_target = f[2]
                else:
                    cur = [t.s, t.e]   # inner end/until belongs to the body
            skip_do = False
            t = nxt(); continue
        if w in ('for', 'while', 'function', 'repeat'):
            stack.append(['opaque', w])
            skip_do = (w in ('for', 'while'))
            t = nxt(); continue
        if w == 'do':
            if skip_do:
                skip_do = False
            else:
                stack.append(['opaque', 'do'])
            t = nxt(); continue
        if cur is None: cur = [t.s, None]
        cur[1] = t.e
        t = nxt()
    close_run(hi)
    return root

def collect_leaves(children, out, path):
    """Flatten: leaves = branch bodies whose children contain no nested dispatch if.
    leaf = {'path': [cond...], 'runs': [(s,e)...], 'opqs': [(w,s,e)...]}"""
    has_if = any(x[0] == 'if' for x in children)
    for x in children:
        if x[0] == 'if':
            node = x[1]
            for cond, ch in node['branches']:
                collect_leaves(ch, out, path + [cond])
            if node['else'] is not None:
                collect_leaves(node['else'], out, path + ['(else)'])
        elif x[0] == 'run':
            out.append({'path': list(path), 'runs': [(x[1], x[2])], 'opqs': [], 'kind': 'run'})
        else:
            out.append({'path': list(path), 'runs': [], 'opqs': [(x[1], x[2], x[3])], 'kind': x[1]})
    return has_if

if __name__ == '__main__':
    src = open('/tmp/vm_while_inner.lua', encoding='utf-8', errors='replace').read()
    root = build_tree(src, 0, len(src))
    leaves = []
    collect_leaves(root, leaves, [])
    disp = sum(1 for x in leaves if x['kind'] == 'run' and False)
    print('leaf items:', len(leaves))
    import collections
    print(collections.Counter(x['kind'] for x in leaves))
    print('non-disp conds found in tree: checking sample')
    # count nodes
    def cnt(ch):
        n = 0
        for x in ch:
            if x[0] == 'if':
                n += 1
                for _, c in x[1]['branches']: n += cnt(c)
                if x[1]['else'] is not None: n += cnt(x[1]['else'])
        return n
    print('dispatch nodes:', cnt(root))
    json.dump({'root': _ser(root) if False else None}, open('/dev/null', 'w'))
