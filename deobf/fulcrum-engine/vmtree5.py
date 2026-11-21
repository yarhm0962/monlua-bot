#!/usr/bin/env python3
"""Parser-backed dispatch-tree builder (lualex.P) with env-based leaf evaluation."""
import re,sys
sys.path.insert(0,'/workspace/monlua-bot/deobf/fulcrum-engine')
from lualex import tokenize, P

def eval_cond(cond, env):
    c=cond.strip().replace('~=','!=')
    try: return bool(eval(c,{'__builtins__':{}},env))
    except Exception: return None

def build_tree(src,lo,hi):
    body=src[lo:hi]
    p=P(tokenize(body))
    def parse_branch(cur):
        kids=[]
        while True:
            t=p.peek()
            if t[0]=='eof' or (t[0]=='kw' and t[1] in ('end','else','elseif','until')):
                return kids
            if p.at('op',';'):
                t2=p.peek()
                p.next()
                cur=max(cur,p.peek()[2] if p.peek()[0]!='eof' else len(body))
                continue
            if t[0]=='kw' and t[1]=='if':
                save=p.i
                p.next(); c0=p.peek()[2]; p.expr()
                cond_txt=body[c0:p.t[p.i-1][2]+len(p.t[p.i-1][1])]
                p.i=save
                p.next(); p.expr(); p.expect('kw','then')
                cur_then=p.t[p.i-1][2]+len(p.t[p.i-1][1])
                kids_then=parse_branch(cur_then)
                branches=[]
                while p.at_kw('elseif'):
                    p.next()
                    c1=p.peek()[2]; p.expr()
                    bc=body[c1:p.t[p.i-1][2]+len(p.t[p.i-1][1])]
                    p.expect('kw','then')
                    cur_b=p.t[p.i-1][2]+len(p.t[p.i-1][1])
                    bkids=parse_branch(cur_b)
                    branches.append([re.sub(r'\s+',' ',bc).strip(),bkids])
                ekids=None
                if p.at_kw('else'):
                    p.next()
                    cur_e=p.t[p.i-1][2]+len(p.t[p.i-1][1])
                    ekids=parse_branch(cur_e)
                p.expect('kw','end')
                cur=p.t[p.i-1][2]+len(p.t[p.i-1][1])
                kids.append(('if',re.sub(r'\s+',' ',cond_txt).strip(),kids_then,branches,ekids))
                continue
            s0=p.peek()[2]
            p.stmt()
            e=p.t[p.i-1]
            nend=e[2]+len(e[1])
            if p.peek()[0]=='op' and p.peek()[1]==';':
                p.next()
                nt=p.peek()
                nend=nt[2] if nt[0]!='eof' else len(body)
            else:
                nt=p.peek()
                nend=nt[2] if nt[0]!='eof' else len(body)
            kids.append(('raw',cur,nend))
            cur=nend
    kids=parse_branch(lo)
    def shift(nodes,off):
        out=[]
        for x in nodes:
            if x[0]=='raw': out.append(('raw',x[1]+off,x[2]+off))
            else:
                _,c,kt,br,ek=x
                out.append(('if',c,shift(kt,off),[[bc,shift(bk,off)] for bc,bk in br],shift(ek,off) if ek is not None else None))
        return out
    return shift(kids,lo)

def leaf_for(nodes,env,src):
    out=[]
    def ev(cond):
        c=cond.replace('~=','!=')
        try: return bool(eval(c,{'__builtins__':{}},env))
        except Exception: return None
    def walk(ch):
        for x in ch:
            if x[0]=='if':
                _,c,kids_then,branches,ekids=x
                if ev(c) is True: walk(kids_then)
                else:
                    hit=False
                    for bc,bk in branches:
                        if ev(bc) is True: walk(bk);hit=True;break
                    if not hit and ekids is not None: walk(ekids)
            elif x[0]=='raw':
                out.append(src[x[1]:x[2]])
    walk(nodes)
    return ''.join(out)

def count_ifs(nodes):
    n=0
    for x in nodes:
        if x[0]=='if':
            n+=1+count_ifs(x[2])+sum(count_ifs(b) for _,b in x[3])
            if x[4] is not None: n+=count_ifs(x[4])
    return n
