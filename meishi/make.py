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
lw=46*mm; c.drawImage('meishi/logo.png',8*mm,H-17*mm,width=lw,height=lw/6,mask='auto')
c.setFillColorRGB(0.1,0.1,0.1)
c.setFont('G',9); c.drawString(8*mm,H-25*mm,'梅光園教室')
c.setFont('G',18); c.drawString(8*mm,H-35.5*mm,'黒岩 真吾')
c.setFont('G',7); c.drawString(8*mm,H-39.5*mm,'KUROIWA SHINGO')
c.setFont('G',8.5); c.drawString(8*mm,H-44.5*mm,'TEL  092-714-0070（教室）')
c.drawString(8*mm,H-48.5*mm,'MOBILE  090-4517-7401')
c.setFont('G',7); c.drawString(8*mm,H-52*mm,'福岡市中央区梅光園2-14-3')
c.save()
