from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('G','/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'))
W,H=91*mm,55*mm
L,R=8*mm,W-8*mm
B=3*mm
c=canvas.Canvas('meishi/meishi_print.pdf',pagesize=(W+2*B,H+2*B))
c.translate(B,B)
c.setFillColorRGB(0.8,0.1,0.1); c.rect(-B,H-2.5*mm,W+2*B,2.5*mm+B,stroke=0,fill=1)
INK=(0.1,0.1,0.1); GREY=(0.35,0.35,0.35)
def t(y,s,size,color=INK,right=False):
    c.setFillColorRGB(*color); c.setFont('G',size)
    (c.drawRightString if right else c.drawString)(R if right else L,H-y*mm,s)
# 上段左：ロゴ・会社名
lw=36*mm; c.drawImage('meishi/logo.png',L,H-12.5*mm,width=lw,height=lw/6,mask='auto')
# 中段右：所属・氏名
t(23,'梅光園教室',7.5,right=True)
t(30,'黒岩 真吾',17,right=True)
t(33.6,'Shingo Kuroiwa',6,GREY,right=True)
# 下段左：連絡先
t(35.3,'株式会社森田修学館',6.5)
t(38.6,'福岡市中央区梅光園2-14-3',6.5)
t(41.9,'TEL 092-714-0070　　MOBILE 090-4517-7401',6.5)
t(45.2,'E-mail bgp2223@gmail.com',6.5)
c.setStrokeColorRGB(0.75,0.75,0.75); c.setLineWidth(0.3)
c.line(L,H-47.4*mm,R,H-47.4*mm)
t(50.2,'六本松校舎 福岡市中央区六本松4-5-36　高宮校舎 福岡市南区玉川町8-8',4.6,GREY)
t(52.5,'西新校舎 福岡市早良区高取1-1-48',4.6,GREY)
c.save()
