"""Recognize direct nearby literal assignments; outputs are unverified candidates."""
import ast
import re
from fulcrum_deobf import decrypt

CALL = re.compile(r'\b(b[OQUV])\s*\(\s*([A-Za-z_]\w*(?:\[\d+\])?)\s*,\s*([A-Za-z_]\w*(?:\[\d+\])?)\s*,\s*([A-Za-z_]\w*(?:\[\d+\])?)\s*\)')

def affine(text):
    def walk(n):
        if isinstance(n,ast.Constant) and type(n.value) is int:return n.value,{}
        if isinstance(n,ast.Name):return 0,{n.id:1}
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            c,d=walk(n.operand);f=-1 if isinstance(n.op,ast.USub) else 1
            return c*f,{k:v*f for k,v in d.items()}
        if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub)):
            a,x=walk(n.left);b,y=walk(n.right);f=-1 if isinstance(n.op,ast.Sub) else 1
            return a+f*b,{k:x.get(k,0)+f*y.get(k,0) for k in x.keys()|y.keys()}
        raise ValueError('not affine integer arithmetic')
    try:
        v,terms=walk(ast.parse(text.strip(),mode='eval').body)
        if any(terms.values()):raise ValueError('symbolic expression')
        return v
    except (SyntaxError,RecursionError) as e:raise ValueError('invalid expression') from e

def find_assignment(region,var):
    token=re.escape(var)
    pat=re.compile(r'(?<![\w\]])'+token+r'\s*=\s*(\{[^{}]*\}|[^;,\n]+)')
    matches=list(pat.finditer(region))
    if not matches:return None
    m=matches[-1]
    # Do not follow through register shuffles or other subsequent uses.
    if re.search(r'(?<![\w\]])'+token+r'(?![\w\[])',region[m.end():]):return None
    raw=m.group(1).strip()
    if raw.startswith('{') and raw.endswith('}'):
        return [affine(x) for x in raw[1:-1].split(',')]
    return affine(raw)

def recover(source,window=4000):
    result=[]
    for call in CALL.finditer(source):
        region=source[max(0,call.start()-window):call.start()]
        try:
            data,key,seed=(find_assignment(region,var) for var in call.groups()[1:])
            if not isinstance(data,list) or not isinstance(key,list) or not isinstance(seed,int):continue
            if len(data)<1 or len(data)>4096:continue
            result_bytes=decrypt(call.group(1)[1],data,key,seed)
        except (ValueError,TypeError):continue
        result.append({'character_offset':call.start(),'algorithm':call.group(1),'hex':result_bytes.hex(),
                       'utf8':result_bytes.decode('utf-8',errors='replace'),
                       'data':data,'key':key,'seed':seed})
    return result
