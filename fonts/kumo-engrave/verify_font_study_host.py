"""Verify the separate local host with its real preconfigured Study-only profile."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image,ImageChops

ROOT=Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args):
    host=args.host.resolve();exe=host/'bin/MuseScore3Evo.exe'
    manifest=json.loads((host/'FONT_STUDY_HOST.json').read_text(encoding='utf-8'))
    assert digest(exe)==manifest['host_sha256']
    for name,sha in manifest['native_source_files'].items():assert digest(host/name)==sha,name
    for family,sha in manifest['study_font_hashes'].items():assert digest(host/'ScoreFonts'/family/(family+'.otf'))==sha
    args.output.mkdir(parents=True,exist_ok=False);out=args.output.resolve()
    score=out/'gliss-study.mscx';shutil.copyfile(args.source_score,score)
    state=out/'registration.json';plugin=out/'registration.qml'
    plugin.write_bytes(('''import QtQuick 2.0
import MuseScore 3.0
import FileIO 3.0
MuseScore {
 menuPath: "Plugins.Font study host verification"
 requiresScore: true
 FileIO { id: report }
 onRun: {
  report.source=REPORT;
  report.write(JSON.stringify({symbol:curScore.style.value("musicalSymbolFont"),
   text:curScore.style.value("musicalTextFont"),pages:curScore.npages,
   symbolRegistered:Qt.fontFamilies().indexOf("Kumo Score Study")>=0,
   textRegistered:Qt.fontFamilies().indexOf("Kumo Score Study Text")>=0},null,2));
 }
}
'''.replace('REPORT',json.dumps(str(state)))).encode('utf-8'))
    env=os.environ.copy();env.update(QT_QPA_PLATFORM='windows',QT_QUICK_BACKEND='software',QML_DISABLE_DISK_CACHE='1')
    prefix=[str(exe),'-s','-m','-c',str(host/'profile')]
    for mode,options in [('svg',['-p',str(plugin),'-o',str(out/'gliss-study.svg')]),
                         ('png',['-r','200','-o',str(out/'gliss-study.png')])]:
        result=subprocess.run(prefix+options+[str(score)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        (out/(mode+'.log')).write_bytes(result.stdout)
        assert result.returncode==0,(mode,result.returncode)
        print('Separate preconfigured host',mode,'OK',flush=True)
    registered=json.loads(state.read_text(encoding='utf-8'))
    assert registered==dict(symbol='Kumo Score Study',text='Kumo Score Study Text',pages=1,symbolRegistered=True,textRegistered=True)
    svg=ET.parse(out/'gliss-study-1.svg').getroot();reference=ET.parse(args.reference/'gliss-study-1.svg').getroot()
    for cls in ('GlissandoSegment','TrillSegment'):
        ours=[ET.tostring(e,encoding='unicode') for e in svg if e.get('class')==cls]
        expected=[ET.tostring(e,encoding='unicode') for e in reference if e.get('class')==cls]
        assert ours==expected,(cls,'Dedicated output differs from verified 0.71')
    rgba=Image.open(out/'gliss-study-1.png').convert('RGBA');paper=Image.new('RGBA',rgba.size,'white');paper.alpha_composite(rgba)
    ours=paper.convert('RGB');ours.save(out/'gliss-study-1-white.png')
    expected=Image.open(args.reference/'gliss-study-1-white.png').convert('RGB')
    assert ours.size==expected.size and ImageChops.difference(ours,expected).getbbox() is None
    assert digest(exe)==manifest['host_sha256']
    report=dict(host=str(exe),host_sha256=manifest['host_sha256'],all_1610_native_files_verified=True,
                actual_preconfigured_profile_used=True,study_font_hashes=manifest['study_font_hashes'],registration=registered,
                dedicated_gliss_and_trill_match_verified_071=True,whole_page_pixels_identical=True,
                installed_application_modified=False,launcher_executed=False,authored_fixture_only=True)
    (out/'host-verification.json').write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print('Study-only preconfigured host verified; dedicated gliss/trill and full-page pixels match 0.71')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--host',type=Path,default=ROOT/'dist/Evolution-0.71-font-study')
    p.add_argument('--source-score',type=Path,default=ROOT/'dist/current-native-gliss-201/gliss-study.mscx')
    p.add_argument('--reference',type=Path,default=ROOT/'dist/native-gliss-133')
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
