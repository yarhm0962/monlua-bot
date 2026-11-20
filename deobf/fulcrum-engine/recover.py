"""Conservative local-literal candidate recovery for Fulcrum LCG strings.

Uses proximity only, never rewrites source; flattened VM register shuffles can
make nearby literals unrelated. Candidates must be independently verified.
"""
import ast
import re
from fulcrum_deobf import decrypt

TABLE = re.compile(r'\{([^{}]{1,16000})\}')
CALL = re.compile(r'\b(b[OQUV])\s*\([^()]{1,300}\)')
ASSIGN = re.compile(r'=\s*(\(*\s*(?:[A-Za-z_][A-Za-z_0-9]*\s*[+\-]\s*)?\d[\d\s()+\-*/]*\)*)\s*(?=;|,|\bend\b)')

class NonConstant(ValueError):pass

def literal(text):
    """Evaluate integer affine arithmetic; all variables must cancel."""
    def walk(n):
        if isinstance(n,ast.Constant) and type(n.value) is int:return n.value,{}
        if isinstance(n,ast.Name):return 0,{n.id:1}
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            c,v=walk(n.operand);s=-1 if isinstance(n.op,ast.USub) else 1
            return c*s,{k:s*x for k,x in v.items()}
        if not isinstance(n,ast.BinOp):raise NonConstant()
        a,x=walk(n.left);b,y=walk(n.right)
        if isinstance(n.op,(ast.Add,ast.Sub)):
            s=-1 if isinstance(n.op,ast.Sub) else 1
            keys=x.keys()|y.keys();return a+s*b,{k:x.get(k,0)+s*y.get(k,0) for k in keys}
        if isinstance(n.op,ast.Mult):
            if any(x.values()) and any(y.values()):raise NonConstant()
            if any(x.values()):return a*b,{k:v*b for k,v in x.items()}
            return a*b,{k:v*a for k,v in y.items()}
        raise NonConstant()
    try:
        n=ast.parse(text.strip(),mode='eval').body
        c,terms=walk(n)
        if any(terms.values()):raise NonConstant()
        return c
    except (SyntaxError,ValueError,RecursionError):raise NonConstant()

def recover(source,window=8000,max_calls=500):
    tables=[]
    for m in TABLE.finditer(source):
        parts=m.group(1).split(',')
        if not 2<=len(parts)<=512:continue
        try:v=[literal(p) for p in parts]
        except NonConstant:continue
        tables.append((m.start(),v))
    seeds=[]
    for m in ASSIGN.finditer(source):
        try:v=literal(m.group(1))
        except NonConstant:continue
        if 0<=v<2**32:seeds.append((m.start(),v))
    result=[]
    for call in list(CALL.finditer(source))[:max_calls]:
        p=call.start(); near=[(at,v) for at,v in tables if p-window<=at<p]
        keys=[v for _,v in near if len(v)==5][-5:]
        arrays=[v for _,v in near if 2<=len(v)<=512 and all(0<=x<=255 for x in v)][-8:]
        numbers=[v for at,v in seeds if p-window<=at<p][-10:]
        found={}
        for k in keys:
            for a in arrays:
                if a is k:continue
                for s in numbers:
                    data=decrypt(call.group(1)[1],a,k,s)
                    score=sum(32<=x<127 or x in (9,10,13) for x in data)/len(data)
                    if score>=.95 and len(data)>=3:
                        found.setdefault(data,(score,k,a,s))
        best=sorted(found.items(),key=lambda it:(-it[1][0],-len(it[0]),it[0]))[:5]
        if best:
            result.append({'character_offset':p,'algorithm':call.group(1),'candidates':[
                {'hex':data.hex(),'text':data.decode('ascii','replace'),'printable_ratio':r[0],
                 'key':r[1],'data':r[2],'seed':r[3]} for data,r in best]})
    return result
