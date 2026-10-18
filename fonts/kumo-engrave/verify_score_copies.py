"""Verify user proof copies differ only in the two font fields; preserve assets."""
import argparse,hashlib,json,xml.etree.ElementTree as ET,zipfile
from pathlib import Path


def without_font_fields(data):
    tree=ET.fromstring(data)
    for style in tree.findall('Score/Style'):
        for child in list(style):
            if child.tag in ('musicalSymbolFont','musicalTextFont'):style.remove(child)
    return ET.tostring(tree)


def run(args):
    report=json.loads((args.proofs/'native-report.json').read_text(encoding='utf-8'))
    source=Path(report['original_score']['path']);sha=hashlib.sha256(source.read_bytes()).hexdigest()
    assert sha==report['original_score']['sha256']
    host=Path(report['host']);assert hashlib.sha256(host.read_bytes()).hexdigest()==report['host_sha256']
    results={}
    if source.suffix.lower()=='.mscz':
        with zipfile.ZipFile(source) as original:
            names=original.namelist();assert len(names)==len(set(names))
            main=[n for n in names if n.endswith('.mscx')];assert len(main)==1
            for variant in ('control','study'):
                path=args.proofs/('user-'+variant+'.mscz')
                with zipfile.ZipFile(path) as result:
                    assert result.namelist()==names
                    for name in names:
                        if name==main[0]:assert without_font_fields(original.read(name))==without_font_fields(result.read(name))
                        else:assert original.read(name)==result.read(name),name
                    results[variant]=dict(only_font_fields_changed=True,all_archive_assets_preserved=True,entries=len(names))
    else:
        for variant in ('control','study'):
            assert without_font_fields(source.read_bytes())==without_font_fields((args.proofs/('user-'+variant+'.mscx')).read_bytes())
            results[variant]=dict(only_font_fields_changed=True)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
    (args.proofs/'score-protection.json').write_text(json.dumps(dict(source_sha256=sha,source_unchanged=True,host_unchanged=True,copies=results),indent=2)+'\n',encoding='utf-8')
    print('Original unchanged; both copies alter only font fields; archive assets retained; host hash stable.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--proofs',type=Path,required=True);run(p.parse_args())
