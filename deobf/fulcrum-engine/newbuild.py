#!/usr/bin/env python3
"""Fulcrum new-build (no-HWID, local VM) deobfuscator.

Pipeline: locate the dispatch heads -> inject trace hooks -> run the file under
bin/luau with a stubbed Roblox prelude -> parse the VMCH trace -> rebuild each
layer's dispatch tree with the parser-backed extractor (vmtree5) -> linearize
the executed states into a readable script.
"""
import os,re,subprocess,sys,tempfile

ENGINE_DIR=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,ENGINE_DIR)
import vmtree5

LUAU=os.path.join(ENGINE_DIR,'bin','luau')

SITE_RE=re.compile(
    r"local (?P<u>\w+)=(?P<fn>\w+)\((?P<F>\w+),(?P<h>\w+)\);"
    r"local (?P<L>\w+)=(?P=u)//32;"
    r"local (?P<e>\w+)=\(if (?P<q>\w+)==(?P=F) then (?P=L) else\(\w+\((?P=q),(?P=h)\)//32\)\);"
    r"(?P=u)=(?P=u)%32")

def find_sites(src):
    out=[]
    for k,m in enumerate(SITE_RE.finditer(src)):
        out.append({'i':m.start(),'end':m.end(),'A':m.group('u'),'L':m.group('L'),
                    'e':m.group('e'),'F':m.group('F'),'h':m.group('h'),'q':m.group('q')})
    return out

def find_loopend(src,start):
    """Scan tokens from `start` until block depth goes negative; that token closes the enclosing loop."""
    from vmwalk2 import tokens
    depth=0
    for t in tokens(src,start,len(src)):
        w=t.w
        if w in ('function','do','repeat','if-stmt'): depth+=1
        elif w in ('end','until'):
            if depth==0: return t.s
            depth-=1
    return len(src)

def gate_ident(src,s):
    m=re.match(r"\s*;?\s*if (\w+) then",src[s['end']:s['end']+80])
    return m.group(1) if m else None

def patch_hooks(src,sites):
    out=[];last=0
    for k,s in enumerate(sites):
        out.append(src[last:s['end']])
        out.append(';__vtrace(%d,%s,%s,%s);print("VMCH\\t%d\\t"..tostring(%s).."\\t"..tostring(%s).."\\t"..tostring(%s))'
                   % (k,s['L'],s['e'],s['A'],k,s['F'],s['h'],s['q']))
        last=s['end']
    out.append(src[last:])
    return ''.join(out)

def h_formula(src,s):
    """Detect an optional `local H=(expr)%K;` right after the head (or a gate if)."""
    g=gate_ident(src,s)
    if g:
        m=re.match(r"\s*;?\s*if \w+ then local (\w+)=\(([^;{}]+?)\)%(?P<k>\d+);",src[s['end']:s['end']+200])
        if not m: return None
        return (m.group(1),m.group(2).strip(),int(m.group('k')))
    m=re.match(r"\s*;?\s*local (\w+)=\(([^;{}]+?)\)%(?P<k>\d+);",src[s['end']:s['end']+160])
    if not m: return None
    return (m.group(1),m.group(2).strip(),int(m.group('k')))

def bx(a,b): return (a^b)&0xFFFFFFFF

def run_trace(patched,prelude_path,timeout=180):
    prelude=open(prelude_path,encoding='utf-8').read()
    blob=prelude+'\nlocal __w = function(...)\n'+patched+'\nend; setfenv(__w, ENV)\nlocal ok,err = xpcall(__w, function(m) print("TB", debug.traceback(m,2)) return m end)\nprint("DONE\t"..tostring(ok).."\t"..tostring(err))\n'
    fd,fn=tempfile.mkstemp(suffix='.lua');os.close(fd)
    with open(fn,'w',encoding='utf-8') as f: f.write(blob)
    try:
        r=subprocess.run([LUAU,fn],capture_output=True,timeout=timeout)
        out=r.stdout.decode(errors='replace')
        err=r.stderr.decode(errors='replace')
    finally: os.remove(fn)
    if 'VMCH' not in out and not out.strip():
        raise RuntimeError('trace produced no states; stderr: '+err[:400])
    tr=[];b0={}
    mode=None
    for line in out.splitlines():
        if line.startswith('B0START'): mode='b0';continue
        if mode=='b0':
            if line.startswith('B0 '):
                _,k,v=line.split(' ',2);b0[int(k)]=v
            else: mode=None
            continue
        if line.startswith('VMCH\t'):
            _,sid,F,h,q=line.strip().split('\t')
            tr.append((int(sid),int(F),int(h),int(q)))
    return tr,b0

def deobfuscate(src,prelude_path=None,timeout=180):
    if prelude_path is None: prelude_path=os.path.join(ENGINE_DIR,'newbuild_prelude.lua')
    sites=find_sites(src)
    if not sites: raise RuntimeError('no dispatch sites matched; not a Fulcrum new-build file')
    tr,b0=run_trace(patch_hooks(src,sites),prelude_path,timeout)
    # per-site state lists + global order
    order=[];seen={}
    for sid,F,h,q in tr:
        u=bx(F,h);L=u//32;op=u%32
        e=L if q==F else bx(q,h)//32
        n=seen.get(sid,0);seen[sid]=n+1
        order.append((sid,n,L,op,e,F,h,q))
    layers=sorted(set(s for s,_,_,_,_,_,_,_ in order))
    res={}
    for sid in layers:
        s=sites[sid]
        s['loopend']=find_loopend(src,s['end'])
        states=[x for x in order if x[0]==sid]
        hf=h_formula(src,s)
        gate=gate_ident(src,s)
        nodes=vmtree5.build_tree(src,s['end'],s['loopend'])
        out=[];bad=[]
        for idx,(lsid,n,L,op,e,F,h,q) in enumerate(states):
            K=bx(states[idx+1][5],states[idx+1][6]) if idx+1<len(states) else None
            env={'N':op,'z':L,'U':e}
            if hf:
                expr='(%s)%%%d'%(hf[1],hf[2])
                try: env[hf[0]]=int(eval(expr.replace(s['e'],str(e)),{'__builtins__':{}}))
                except Exception: pass
            text=vmtree5.leaf_for(nodes,env,src)
            if gate is not None and gate not in env: env[gate]=True;text=vmtree5.leaf_for(nodes,env,src)
            ok = K is None or re.search(r'\b%d\b'%K,text)
            if not ok and gate is not None:
                env2=dict(env);env2[gate]=False
                t2=vmtree5.leaf_for(nodes,env2,src)
                if K is None or re.search(r'\b%d\b'%K,t2): text=t2;ok=True
            if not ok: bad.append(n);text=''
            out.append({'L':L,'op':op,'e':e,'K':K,'text':text})
        res[sid]={'states':out,'bad':bad}
    parts=[]
    for sid,n,L,op,e,F,h,q in order:
        t=res[sid]['states'][n]['text'].strip()
        if not t: continue
        if parts and parts[-1]==t: continue
        parts.append(t)
    body='\n'.join('do\n'+p+'\nend' for p in parts)
    head=sites[0]['i'];loopend=sites[0]['loopend']
    pre=src[:head];post=src[loopend:]
    artifact=pre+'while true do\n'+body+'\nend '+post
    return artifact,res,b0
