"""Counterfactual bracket-only copies; preserve six staves and all music."""
import copy,json,os,subprocess,xml.etree.ElementTree as E
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parent
PROOF=Path(r'C:\Users\Fred\.codex\visualizations\2026\10\09\01a11ecb-ed01-7723-ae9b-12c5ea10a97d\font-native-017-piano02')
EXE=Path(r'E:\programming\funcodes\muse3_dev\MuseScore\msvc.install_piano_0_17_x64\bin\MuseScore3Evo.exe')

def run():
    out=ROOT/'dist/bracket-cause-probe'
    if out.exists():raise ValueError('Probe exists; preserve prior results')
    (out/'config/MuseScore').mkdir(parents=True)
    (out/'config/MuseScore/MuseScore3Evo.ini').write_text('[application]\npaths\\myScoreFonts='+str(PROOF/'ScoreFonts').replace('\\','/')+'\n',encoding='utf-8')
    changed=[]
    env=os.environ.copy();env.update(QT_QPA_PLATFORM='windows',QT_QUICK_BACKEND='software',QML_DISABLE_DISK_CACHE='1')
    for variant in ['leland','leland-control']:
        source=E.parse(PROOF/('user-'+variant+'.mscx')).getroot()
        music=[E.tostring(staff) for staff in source.findall('./Score/Staff')]
        for bracket in source.findall('./Score/Part/Staff/bracket'):
            span=int(bracket.get('span','1'))
            if span>4:
                changed.append(dict(variant=variant,before=dict(bracket.attrib)))
                bracket.set('span','4')
        assert music==[E.tostring(staff) for staff in source.findall('./Score/Staff')]
        file=out/(variant+'.mscx');E.ElementTree(source).write(str(file),encoding='utf-8',xml_declaration=True)
        result=subprocess.run([str(EXE),'-s','-m','-c',str(out/'config'),'-r','180','-o',str(out/(variant+'.png')),str(file)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,timeout=90)
        (out/(variant+'.log')).write_bytes(result.stdout);assert result.returncode==0
        print(variant,'bracket-only copy rendered',flush=True)
    baseline=sorted(out.glob('leland-[0-9]*.png'));control=sorted(out.glob('leland-control-[0-9]*.png'))
    assert len(baseline)==len(control)
    results={}
    for a,b in zip(baseline,control):
        def paper(file):
            im=Image.open(file).convert('RGBA');p=Image.new('RGBA',im.size,'white');p.alpha_composite(im);return p.convert('RGB')
        diff=ImageChops.difference(paper(a),paper(b)).getbbox()
        results[a.name]=dict(pixel_identical=diff is None,difference_bbox=diff)
    report=dict(intervention='Only bracket span >4 becomes 4 in copies. Six Staff music subtrees unchanged. Fonts/Text/config otherwise the same as fixed proofs.',changes=changed,pages=len(baseline),comparisons=results)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Counterfactual:',len(baseline),'pages;',sum(row['pixel_identical'] for row in results.values()),'identical')
if __name__=='__main__':run()
