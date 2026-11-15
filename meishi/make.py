from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import glob
p=[f for f in glob.glob('/usr/share/fonts/**/ipag.ttf',recursive=True)][0]
pdfmetrics.registerFont(TTFont('G',p))
W,H=91*mm,55*mm
c=canvas.Canvas('meishi/meishi.pdf',pagesize=(W,H))
c.setFillColorRGB(0.8,0.1,0.1); c.rect(0,H-3*mm,W,3*mm,stroke=0,fill=1)
lw=42*mm; c.drawImage('meishi/logo.png',8*mm,H-14.5*mm,width=lw,height=lw/6,mask='auto')
c.setFillColorRGB(0.1,0.1,0.1)
def t(y,s,size): c.setFont('G',size); c.drawString(8*mm,H-y*mm,s)
t(20,'梅光園教室',8.5)
t(27.5,'黒岩 真吾',16)
t(30.8,'KUROIWA SHINGO',6)
t(35.3,'TEL  092-714-0070',7.5)
t(38.8,'MOBILE  090-4517-7401',7.5)
t(42.3,'MAIL  bgp2223@gmail.com',7.5)
t(45.8,'福岡市中央区梅光園2-14-3',6.5)
c.setStrokeColorRGB(0.75,0.75,0.75); c.setLineWidth(0.3)
c.line(8*mm,H-47.8*mm,W-8*mm,H-47.8*mm)
c.setFillColorRGB(0.35,0.35,0.35)
t(50.3,'六本松校舎 福岡市中央区六本松4-5-36　高宮校舎 福岡市南区玉川町8-8',4.6)
t(52.6,'西新校舎 福岡市早良区高取1-1-48',4.6)
c.save()
