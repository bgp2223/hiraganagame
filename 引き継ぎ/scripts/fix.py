import openpyxl, collections, copy
from calc import parse, F
wb=openpyxl.load_workbook(F)
ws=wb['R8表紙']
res=parse(ws,74,101)
tot=collections.defaultdict(dict)
for (t,s),l in res.items(): tot[t][s]=sum(n for _,n,_ in l)
HS={'原':'高5?','古賀':'高5?','髙本':'高5?'}   # 高校行（R8 D85/D101/L101）
tot['原']  # exists
order={'国':['馬渡','日高','副島','佐藤','長本','右田'],
 '数':['髙本','小野','黒岩','伊地知','平井','古賀','平野'],
 '社':['藤田','岡野','右田','長本','山内','副島','佐藤','中嶋'],
 '理':['神田','田代','和久','大山','平野','倉光'],
 '英':['中村','中嶋','土井下','原','大山']}
# 全員が漏れなく入っているか確認
for s,l in order.items():
    got={t for t,d in tot.items() if s in d}
    assert got==set(l),(s,got^set(l))
cols={'国':2,'数':5,'社':8,'理':11,'英':14}
SN=dict(国='国',数='数',社='社',理='理',英='英')
for r in range(107,118):
    for c in range(2,17): ws.cell(r,c).value=None
for s,l in order.items():
    c0=cols[s]
    for i,t in enumerate(l):
        r=107+i
        ws.cell(r,c0).value='？(未定)' if t=='？' else t
        ws.cell(r,c0+1).value=tot[t][s]
        oth=''.join(f'{o}{tot[t][o]}' for o in '国数社理英' if o!=s and o in tot[t])
        oth+=HS.get(t,'')
        ws.cell(r,c0+2).value=oth or None
# 内訳シート
if '4番内訳' in wb.sheetnames: del wb['4番内訳']
bs=wb.create_sheet('4番内訳',index=1)
bs.append(['教員','教科','計','内訳（セル：コマ数）'])
n=0
for s in '国数社理英':
    for t in order[s]:
        l=res[(t,s)]
        bs.append([t,s,sum(x[1] for x in l),' + '.join(f'{a}:{b}' for a,b,_ in l)])
bs.append([]); bs.append(['※シート「R8表紙プランA」の「３．担当者」表を集計。担任列は含めない。'])
bs.append(['※高校：原5?(D85)、古賀5?(D101)、髙本・北原5?(L101) は「他教科」欄に高5?として記載（未確定）'])
for col,w in zip('ABCD',(12,6,6,120)): bs.column_dimensions[col].width=w
wb.save('/tmp/claude-0/work/out5.xlsx')
for s in '国数社理英':
    print(s,[(t,tot[t][s],''.join(f'{o}{tot[t][o]}' for o in '国数社理英' if o!=s and o in tot[t])+HS.get(t,'')) for t in order[s]])
