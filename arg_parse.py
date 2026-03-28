#!/usr/bin/env python3
"""Lightweight argument parser — no argparse dependency style."""
import sys
class Args:
    def __init__(self): self._args={}; self._pos=[]; self._flags=set()
    def flag(self,*names,help=""): self._flags.update(names); return self
    def opt(self,name,default=None,help=""): self._args[name]=default; return self
    def parse(self,argv=None):
        argv=argv or sys.argv[1:]; result={"_pos":[]}; i=0
        for f in self._flags: result[f.lstrip("-").replace("-","_")]=False
        for k,v in self._args.items(): result[k.lstrip("-").replace("-","_")]=v
        while i<len(argv):
            a=argv[i]
            if a.startswith("-"):
                key=a.lstrip("-").replace("-","_")
                if a in self._flags: result[key]=True
                elif i+1<len(argv): result[key]=argv[i+1]; i+=1
            else: result["_pos"].append(a)
            i+=1
        return type("NS",(),result)()
def cli():
    p=Args().flag("-v","--verbose").opt("--name","world").opt("--count","1")
    args=p.parse()
    for _ in range(int(args.count)): print(f"Hello, {args.name}!" + (" (verbose)" if args.verbose else ""))
if __name__=="__main__": cli()
