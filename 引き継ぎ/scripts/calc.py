import openpyxl, re, sys, collections
F='/tmp/claude-0/work/src6.xlsx'
wb=openpyxl.load_workbook(F)
def parse(ws, r0, r1):
    """r0..r1: section 3 rows. returns dict[(teacher,subject)] -> list of (cell,n)"""
    res=collections.defaultdict(list); unk=[]
    # subject per column determined by nearest header row above (rows whose C == '担任')
    hdr={}
    for r in range(r0,r1+1):
        for base in (2,10):  # B..H and J..P
            if ws.cell(r,base+1).value=='担任':
                hdr[base]={c:ws.cell(r,c).value for c in range(base+2,base+7)}
        for base in (2,10):
            if base not in hdr or ws.cell(r,base+1).value=='担任': continue
            lab=ws.cell(r,base).value or ''
            special=None
            if lab.startswith('5年特別講座'): special='sp'
            elif lab.startswith('高校'): special='hs'
            if special=='sp':
                for c,sj in ((base+3,'社'),(base+5,'理')):
                    v=ws.cell(r,c).value
                    m=re.fullmatch(r'[★●]*\s*([^\d]+?)\s*(\d+)\??',str(v).strip()) if v else None
                    if m: res[(m.group(1).lstrip('★●'),sj)].append((ws.cell(r,c).coordinate,int(m.group(2)),v))
                continue
            if special=='hs':
                for c in range(base+2,base+7):
                    v=ws.cell(r,c).value
                    if v: print('HS',ws.cell(r,c).coordinate,v)
                continue
            for c in range(base+2,base+7):
                v=ws.cell(r,c).value
                if not isinstance(v,str): continue
                m=re.fullmatch(r'[★●]*\s*([^\d]+?)\s*(\d+)\??',v.strip())
                if not m:
                    if re.search(r'\d',v): unk.append((ws.cell(r,c).coordinate,v))
                    continue
                name=m.group(1).lstrip('★●'); n=int(m.group(2))
                subj=hdr[base][c]
                subj={'数学':'数','算数':'数','算数講座':'数','国語':'国','社会':'社','理科':'理','英語':'英'}.get(subj,subj)
                res[(name.replace('高本','髙本'),subj)].append((ws.cell(r,c).coordinate,n,v))
    print('UNPARSED',unk)
    return res
if __name__=='__main__':
    ws=wb[sys.argv[1]]; r0,r1=int(sys.argv[2]),int(sys.argv[3])
    res=parse(ws,r0,r1)
    tot=collections.defaultdict(dict)
    for (t,s),l in res.items(): tot[t][s]=sum(n for _,n,_ in l)
    for t,d in sorted(tot.items()): print(t,d)
