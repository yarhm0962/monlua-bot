#!/usr/bin/env python3
"""Experimental offline Fulcrum decoder; this is not a VM devirtualizer."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

MOD = 1 << 24
KNOWN_SHA256 = '351e2801ddfcdfb34fb9aa4874cd2125593c1d11ccb1736005d65b9bd07dde48'

def decrypt(algorithm, data, key, seed):
    if algorithm not in 'OQUV' or len(algorithm) != 1:
        raise ValueError('algorithm must be one of O, Q, U, V')
    if len(key) != 5 or not all(isinstance(x, int) and not isinstance(x, bool) for x in key):
        raise ValueError('key must contain exactly five integers')
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError('seed must be an integer')
    if not all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x <= 255 for x in data):
        raise ValueError('data must contain byte values')
    a,b,c,d,e = key
    out = bytearray()
    for value in data:
        if algorithm == 'O': seed = (seed*a+b) % MOD
        elif algorithm == 'Q': seed = (seed*a+b*a) % MOD
        elif algorithm == 'U': seed = (seed*a-b) % MOD
        else: seed = (seed*a-b*a) % MOD
        f = seed + (seed//256)*d + (seed//65536)*e
        if algorithm == 'O': value = (value-f)*c
        elif algorithm == 'Q': value = value*c-f
        elif algorithm == 'U': value = (value+f)*c
        else: value = value*c+f
        out.append(value % 256)
    return bytes(out)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    scan = sub.add_parser('scan', help='identify Fulcrum indicators and known loader string candidates')
    scan.add_argument('input', type=Path)
    scan.add_argument('-o', '--output', type=Path, required=True, help='write report as JSON')
    scan.add_argument('--direct', action='store_true', help='recover direct nearby literals; results are unverified')
    dec = sub.add_parser('decrypt', help='decode a supplied byte array, key and seed')
    dec.add_argument('algorithm', choices=['O','Q','U','V'])
    dec.add_argument('--data', required=True, help='JSON array of encoded bytes')
    dec.add_argument('--key', required=True, help='JSON array of five integers')
    dec.add_argument('--seed', type=int, required=True)
    args = p.parse_args()
    if args.command == 'decrypt':
        out = decrypt(args.algorithm, json.loads(args.data), json.loads(args.key), args.seed)
        print(json.dumps({'hex':out.hex(), 'utf8':out.decode('utf-8', errors='replace')}, ensure_ascii=False))
        return
    data = args.input.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    header = re.search(rb'(?i)obfuscated\s+by\s+fulcrum',data[:4096]) is not None
    report = {'input':str(args.input), 'sha256':digest, 'fulcrum_header':header,
              'note':'This is a static analysis report, not devirtualized code. Known-sample strings are heuristic candidates, not verified substitutions.',
              'known_sample':digest == KNOWN_SHA256, 'string_candidates':[]}
    if report['known_sample']:
        records = json.loads((Path(__file__).parent/'known_sample_candidates.json').read_text(encoding='utf-8'))
        report['string_candidates']=[{'character_offset':int(k), **v} for k,v in records.items() if v['text'] is not None]
        report['unresolved_count']=sum(v['text'] is None for v in records.values())
    if args.direct:
        from direct import recover
        report['direct_literal_candidates'] = recover(data.decode('utf-8',errors='replace'))
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('Fulcrum header:', header, '| known exact sample:', report['known_sample'], '| candidates:',len(report['string_candidates']))
    print('Report:',args.output)

if __name__ == '__main__':
    try: main()
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print('error:',e,file=sys.stderr);sys.exit(1)
