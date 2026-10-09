"""FreeType outline preflight. Native MuseScore proofs remain the acceptance render."""
import json
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from source.piano_palette import specs
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist/outline-preflight'
OUT.mkdir(exist_ok=True)
glyphs={'noteheadBlack':dict(codepoint='E0A4'),'noteheadHalf':dict(codepoint='E0A3'),'noteheadWhole':dict(codepoint='E0A2'),**specs()}
label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for key,path in [('leland',ROOT/'vendor/leland/Leland.otf'),('piano',ROOT/'dist/piano/Kumo Piano/Kumo Piano.otf')]:
    font=ImageFont.truetype(str(path),200)
    image=Image.new('RGB',(2000,math.ceil(len(glyphs)/5)*480),'white');d=ImageDraw.Draw(image)
    for i,(name,spec) in enumerate(glyphs.items()):
        x=i%5*400+20;y=i//5*480+300
        d.text((x,y-265),name,font=label,fill='black')
        for k in range(-2,3):d.line((x,y+k*50,x+365,y+k*50),fill='#bbbbbb',width=2)
        d.text((x+100,y),chr(int(spec['codepoint'],16)),font=font,fill='black',anchor='ls')
    image.save(OUT/(key+'-palette.png'))
print('Saved independent outline preflight boards.')
