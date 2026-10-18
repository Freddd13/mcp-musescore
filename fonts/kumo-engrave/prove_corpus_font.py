"""Isolated native proofs of the local corpus font: notes, Text, and all glyphs."""
import argparse,hashlib,json,os,re,shutil,subprocess,textwrap,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
from render_proofs import set_font,no_style_xml

ROOT=Path(__file__).resolve().parent


def run(args):
    args.output.mkdir(parents=True,exist_ok=False);out=args.output.resolve();fonts=out/'ScoreFonts'
    build=json.loads((args.fonts/'build-report.json').read_text(encoding='utf-8'))
    for name in build['fonts']:shutil.copytree(args.fonts/name,fonts/name)
    config=out/'config';(config/'MuseScore').mkdir(parents=True)
    (config/'MuseScore/MuseScore3Evo.ini').write_text('[application]\npaths\\myScoreFonts='+fonts.as_posix()+'\n',encoding='utf-8')
    env=os.environ.copy();env.update(QT_QPA_PLATFORM='windows',QT_QUICK_BACKEND='software',QML_DISABLE_DISK_CACHE='1')
    prefix=[str(args.musescore),'-s','-m','-c',str(config)]
    report=dict(host=str(args.musescore),host_sha256=hashlib.sha256(args.musescore.read_bytes()).hexdigest(),proofs={})
    def convert(label,options,source):
        try:
            result=subprocess.run(prefix+options+[str(source)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        except subprocess.TimeoutExpired as error:
            (out/(label+'.log')).write_bytes(error.output or b'')
            raise
        (out/(label+'.log')).write_bytes(result.stdout)
        if result.returncode:raise RuntimeError(label+' native conversion failed: '+str(result.returncode))
        print(label,'OK',flush=True)
    fixture=out/'palette.mscx'
    convert('import',['-o',str(fixture)],ROOT/'fixtures/piano-palette.musicxml')
    data=fixture.read_bytes()
    def proof(label,source,family,archive=None):
        score=out/(label+'.mscx');set_font(source,score,family,family+' Text')
        if archive:
            updated=score.read_bytes();score=out/(label+'.mscz')
            with zipfile.ZipFile(archive) as old,zipfile.ZipFile(score,'x') as new:
                main=[n for n in old.namelist() if n.endswith('.mscx')];assert len(main)==1
                for info in old.infolist():new.writestr(info,updated if info.filename==main[0] else old.read(info.filename))
        probe=out/(label+'.qml');state=out/(label+'.json')
        probe.write_text('''import QtQuick 2.0
import MuseScore 3.0
import FileIO 3.0
MuseScore {
 menuPath: "Plugins.Local corpus font proof"
 requiresScore: true
 FileIO { id: report }
 onRun: {
  var symbol=curScore.style.value("musicalSymbolFont");
  var text=curScore.style.value("musicalTextFont");
  report.source=REPORT;
  report.write(JSON.stringify({symbol:symbol,text:text,pages:curScore.npages,
   symbolRegistered:Qt.fontFamilies().indexOf(symbol)>=0,textRegistered:Qt.fontFamilies().indexOf(text)>=0},null,2));
 }
}
'''.replace('REPORT',json.dumps(str(state))),encoding='utf-8')
        convert(label+'-svg',['-p',str(probe),'-o',str(out/(label+'.svg'))],score)
        convert(label+'-png',['-r','200','-o',str(out/(label+'.png'))],score)
        status=json.loads(state.read_text(encoding='utf-8'));assert status['symbolRegistered'] and status['textRegistered']
        assert status['symbol']==family and status['text']==family+' Text'
        report['proofs'][label]=status
    if not args.text_only and not args.waves_only and not args.observed_only:
        for variant in ('Control','Study'):proof('palette-'+variant.lower(),data,'Kumo Score '+variant)
        from source.extension_fixture import integration_score
        extra=integration_score(data)
        for variant in ('Control','Study'):
            source=extra.replace(b'Kumo Score Study Text',('Kumo Score '+variant+' Text').encode())
            proof('integration-'+variant.lower(),source,'Kumo Score '+variant)
    if not args.text_only and not args.waves_only and 'noteheadCircleX' in build['fonts']['Kumo Score Study']['changed']:
        from source.observed_fixture import observed_score,brace_score
        for variant in ('Control','Study'):
            proof('observed-'+variant.lower(),observed_score(data),'Kumo Score '+variant)
        if not args.observed_only:
            for count in (1,2,3,4,6):
                proof('brace-%d'%count,brace_score(data,count),'Kumo Score Study')
    if args.observed_only:
        assert not args.score,'The observed-only fixture does not render user scores'
        assert hashlib.sha256(args.musescore.read_bytes()).hexdigest()==report['host_sha256']
        (out/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        return
    if not args.text_only:
        from source.wave_fixture import wave_score
        for variant in ('Control','Study'):proof('waves-'+variant.lower(),wave_score(data),'Kumo Score '+variant)
    if args.score:
        original=hashlib.sha256(args.score.read_bytes()).hexdigest();archive=None
        if args.score.suffix.lower()=='.mscz':
            with zipfile.ZipFile(args.score) as z:
                main=[n for n in z.namelist() if n.endswith('.mscx')];assert len(main)==1
                user=z.read(main[0])
            archive=args.score
        else:user=args.score.read_bytes()
        for variant in ('Control','Study'):proof('user-'+variant.lower(),user,'Kumo Score '+variant,archive)
        assert hashlib.sha256(args.score.read_bytes()).hexdigest()==original
        report['original_score']=dict(path=str(args.score),sha256=original,unchanged=True)
    if args.waves_only:
        assert hashlib.sha256(args.musescore.read_bytes()).hexdigest()==report['host_sha256'],'Proof host changed during rendering'
        (out/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        return
    def text_score():
        tree=ET.fromstring(data);score=tree.find('Score')
        for staff in score.findall('Staff'):
            measure=staff.find('Measure')
            for v in list(staff):
                if v is not measure:staff.remove(v)
        return tree,score
    # A separate authored score exercises the real <sym> Text path for every
    # changed symbol. These are not screenshots from Pillow font rendering.
    names=list(build['fonts']['Kumo Score Study']['changed'])
    for block in range(0,len(names),25):
        tree,score=text_score();style=score.find('Style')
        for key,value in [('pageWidth',11.6929),('pageHeight',16.5354)]:
            e=style.find(key)
            if e is None:e=ET.SubElement(style,key)
            e.text=str(value)
        staff=score.find('Staff');frame=ET.Element('VBox');staff.insert(0,frame);ET.SubElement(frame,'height').text='130'
        ET.SubElement(frame,'boxAutoSize').text='0'
        for i,name in enumerate(names[block:block+25]):
            text=ET.SubElement(frame,'Text');ET.SubElement(text,'style').text='Frame'
            ET.SubElement(text,'offset',x=str(i%5*52),y=str(i//5*40))
            item=build['fonts']['Kumo Score Study']['changed'][name]
            body=('<sym>'+name+'</sym>') if item.get('smufl',True) else '<font face="Kumo Score Study Text"/>'+chr(item['codepoint'])
            label=name if len(name)<=24 else '\n'.join(textwrap.wrap(re.sub(r'([a-z])([A-Z])',r'\1 \2',name),24))
            text.append(ET.fromstring('<text><font size="8"/>'+label+'</text>'))
            glyph=ET.SubElement(frame,'Text');ET.SubElement(glyph,'style').text='Frame'
            ET.SubElement(glyph,'offset',x=str(i%5*52),y=str(i//5*40+14))
            glyph.append(ET.fromstring('<text><font size="28"/>'+body+'</text>'))
        proof('atlas-%02d'%(block//25+1),ET.tostring(tree),'Kumo Score Study')
    # Native GSUB comparison rows; left uses ordinary composed dynamics,
    # right the observed single-glyph equivalent. Same type size and family.
    tree,score=text_score()
    frame=ET.Element('VBox');score.find('Staff').insert(0,frame);ET.SubElement(frame,'height').text='120'
    ET.SubElement(frame,'boxAutoSize').text='0'
    from source.pdf_symbol_map import LIGATURES
    for i,(target,parts) in enumerate(LIGATURES):
        for j,body in enumerate([''.join('<sym>'+n+'</sym>' for n in parts),'<sym>'+target+'</sym>']):
            text=ET.SubElement(frame,'Text');ET.SubElement(text,'style').text='Frame'
            ET.SubElement(text,'offset',x=str(j*80),y=str(i*18))
            text.append(ET.fromstring('<text><font size="22"/>'+body+'</text>'))
    proof('dynamics-shaping',ET.tostring(tree),'Kumo Score Study')
    assert hashlib.sha256(args.musescore.read_bytes()).hexdigest()==report['host_sha256'],'Proof host changed during rendering'
    (out/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Native registration and authored fixture conversions verified; inspect images separately.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fonts',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--musescore',type=Path,required=True)
    section=p.add_mutually_exclusive_group()
    section.add_argument('--text-only',action='store_true')
    section.add_argument('--waves-only',action='store_true')
    section.add_argument('--observed-only',action='store_true')
    p.add_argument('--score',type=Path,help='Optional read-only original; render isolated copies with archive assets preserved')
    run(p.parse_args())
