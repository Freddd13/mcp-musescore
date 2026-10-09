"""Verify final files against read-only native proofs, including Text isolation."""
import hashlib,json
import argparse
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parent
ART=Path(r'C:\Users\Fred\.codex\visualizations\2026\10\09\01a11ecb-ed01-7723-ae9b-12c5ea10a97d')
FIXED=ART/'font-native-017-piano02'
PAIRED=ART/'font-native-017-piano02-text'

def opaque(file):
    image=Image.open(file).convert('RGBA');paper=Image.new('RGBA',image.size,'white');paper.alpha_composite(image)
    return paper.convert('RGB')

def run(fixed=FIXED,paired=PAIRED):
    global FIXED,PAIRED
    FIXED,PAIRED=Path(fixed),Path(paired)
    a=json.loads((FIXED/'native-report.json').read_text());b=json.loads((PAIRED/'native-report.json').read_text())
    assert a['host_sha256']==b['host_sha256']
    checks={}
    for variant in ['leland-control','piano']:
        for sample in ['fixture','user']:
            key=sample+'-'+variant
            assert a['proofs'][key]['pages']==b['proofs'][key]['pages']
            for page in range(1,a['proofs'][key]['pages']+1):
                file=key+'-'+str(page)+'.png'
                before,after=opaque(FIXED/file),opaque(PAIRED/file)
                assert before.size==after.size
                diff=ImageChops.difference(before,after).getbbox()
                checks[file]=dict(fixed_vs_paired_pixel_identical=diff is None,difference_bbox=diff)
                # Renamed Text has no built-in Qt substitutions. Record full
                # score differences; only the common-symbol fixture is strict.
                if sample=='fixture':assert diff is None,file
        family='Kumo Piano Control' if variant=='leland-control' else 'Kumo Piano'
        for suffix in ['', ' Text']:
            name=family+suffix
            final=(ROOT/'dist'/variant/name/(name+'.otf')).read_bytes()
            for proof in [FIXED,PAIRED]:
                assert final==(proof/'ScoreFonts'/name/(name+'.otf')).read_bytes(),name
    originals=dict(a['originals'])
    originals[r'C:\Users\Fred\OneDrive - yunzd\arr\如果有来生\如果有来生_arr_by_kumo.pdf']='58475eccac2a6e83f8da881ae2f44abeb3998ac7b8c236a33ab4c948f1f3faf5'
    for path,expected in originals.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected
    report=dict(date='2026-10-10',fixed_report=str(FIXED/'native-report.json'),paired_report=str(PAIRED/'native-report.json'),text_comparison=checks,recommended_text='Leland Text',originals=originals,originals_unchanged=True,font_bytes_match_proofs=True,physical_print_test=False,aesthetic_approval=False)
    out=ROOT/'dist/review-0.2';out.mkdir(exist_ok=True)
    (out/'release-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    # A compact native side-by-side board, fixed physical scale and crop boxes.
    before=opaque(FIXED/'fixture-leland-control-1.png');after=opaque(FIXED/'fixture-piano-1.png')
    from PIL import ImageDraw,ImageFont
    label=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
    board=Image.new('RGB',(2720,1720),'white')
    for i,(image,name) in enumerate([(before,'Unmodified Leland (renamed control)'),(after,'Kumo Piano 0.2 - independent common palette')]):
        board.paste(image.crop((105,255,1430,1905)),(i*1360+10,55))
        ImageDraw.Draw(board).text((i*1360+10,15),name,font=label,fill='black')
    board.save(out/'native-palette-comparison.png')
    print('Verified %d pages; %d paired Text pages differ. Recommend built-in Leland Text. Final font bytes and both original hashes verified.' % (len(checks),sum(not row['fixed_vs_paired_pixel_identical'] for row in checks.values())))
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixed',type=Path,default=FIXED)
    parser.add_argument('--paired',type=Path,default=PAIRED)
    args=parser.parse_args();run(args.fixed,args.paired)
