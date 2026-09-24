import math
S = 220                      # 立方体の1辺（px）
import os
K, TH = float(os.environ.get('K', 0.35)), math.radians(float(os.environ.get('TH', 45)))  # 奥行きの縮み・角度（キャビネット図）
DX, DY = K * math.cos(TH) * S, K * math.sin(TH) * S

# 3D座標（x:右, y:上, z:奥）
V = {
    'G': (0, 0, 0), 'H': (1, 0, 0), 'D': (1, 1, 0), 'C': (0, 1, 0),
    'F': (0, 0, 1), 'E': (1, 0, 1), 'A': (1, 1, 1), 'B': (0, 1, 1),
}
OX, OY = 50, 60 + DY + S     # 前面左下(G)の画面位置

def P(p):
    x, y, z = p
    return (OX + x * S + z * DX, OY - y * S - z * DY)

W = S + DX + 100
H = S + DY + 120

def line(a, b, dashed=False, w=2.2):
    (x1, y1), (x2, y2) = P(a), P(b)
    d = ' stroke-dasharray="8 6"' if dashed else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#000" stroke-width="{w}"{d} stroke-linecap="round"/>'

# 頂点名の位置（原図に合わせる）
LAB = {'A': (12, -8, 'start'), 'B': (-4, -14, 'middle'), 'C': (-12, 8, 'end'), 'D': (8, 26, 'start'),
       'E': (12, 8, 'start'), 'F': (-10, -6, 'end'), 'G': (-10, 26, 'end'), 'H': (8, 28, 'start')}

def cube():
    out = []
    solid = [('C','D'),('D','H'),('H','G'),('G','C'),('B','A'),('A','E'),('C','B'),('D','A'),('H','E')]
    hidden = [('B','F'),('F','E'),('F','G')]
    out += [line(V[a], V[b], True, 1.8) for a, b in hidden]
    out += [line(V[a], V[b]) for a, b in solid]
    for n, (dx, dy, anc) in LAB.items():
        x, y = P(V[n])
        out.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anc}" font-size="26">{n}</text>')
    return out

def poly(pts, fill='#9a9a9a', op=0.45):
    s = ' '.join(f'{P(p)[0]:.1f},{P(p)[1]:.1f}' for p in pts)
    return f'<polygon points="{s}" fill="{fill}" fill-opacity="{op}" stroke="none"/>'

def dot(p):
    x, y = P(p)
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="#000"/>'

mid = lambda a, b: tuple((V[a][i] + V[b][i]) / 2 for i in range(3))

def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
            f'font-family="Arial, Helvetica, \'Liberation Sans\', sans-serif">'
            f'<rect width="100%" height="100%" fill="#fff"/>' + ''.join(body) + '</svg>')

figs = {}

# ① 正八面体（各面の中心を結ぶ）
c = {'top': (.5, 1, .5), 'bot': (.5, 0, .5), 'L': (0, .5, .5), 'R': (1, .5, .5), 'fr': (.5, .5, 0), 'bk': (.5, .5, 1)}
oct_edges = [(a, b) for a in ['top', 'bot'] for b in ['L', 'R', 'fr', 'bk']] + [('L','fr'),('fr','R'),('R','bk'),('bk','L')]
body = cube()
body += [line(c[a], c[b], True, 1.8) for a, b in oct_edges if 'bk' in (a, b)]
body += [line(c[a], c[b]) for a, b in oct_edges if 'bk' not in (a, b)]
figs['1_正八面体'] = svg(body)

# ② 立方体のみ
figs['2_立方体'] = svg(cube())

# ③ 正三角形 BDE で切る（AGに垂直。三角すい A-BDE は全体の 1/6）
body = [poly([V['B'], V['D'], V['E']])] + cube()
body += [line(V['B'], V['D'], w=2.6), line(V['D'], V['E'], w=2.6), line(V['B'], V['E'], True, 2.2)]
figs['3_正三角形の切り口'] = svg(body)

# ④ 正六角形で切る（AGに垂直で、6本の辺の中点を通る）
hexp = [mid('B','C'), mid('C','D'), mid('D','H'), mid('H','E'), mid('E','F'), mid('F','B')]
vis = [True, True, True, False, False, False]   # 上面・前面・右面は見える、底面・奥面・左面は見えない
body = [poly(hexp)] + cube()
for i in range(6):
    body.append(line(hexp[i], hexp[(i + 1) % 6], not vis[i], 2.6 if vis[i] else 2.2))
body += [dot(p) for p in hexp]
figs['4_正六角形の切り口'] = svg(body)

for k, s in figs.items():
    open(f'{k}.svg', 'w').write(s)

cells = ''.join(f'<div class="cell"><span class="no">{"①②③④"[i]}</span>{s}</div>' for i, s in enumerate(figs.values()))
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page {{ size: A4 landscape; margin: 0; }}
html, body {{ margin: 0; }}
.page {{ width: 297mm; height: 210mm; box-sizing: border-box; padding: 8mm 12mm;
  display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 4mm 10mm; }}
.cell {{ position: relative; min-height: 0; }}
.cell svg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.no {{ position: absolute; left: 0; top: 0; font: 22px 'IPAPGothic', sans-serif; z-index: 1; }}
</style></head><body><div class="page">{cells}</div></body></html>'''
open('sheet.html', 'w').write(html)
