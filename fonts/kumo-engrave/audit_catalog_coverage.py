"""Reconcile all selected music catalogues and reviewed hidden-font samples.

No matcher label is promoted to a semantic decision. This checks the exact
reviewed instances; font-name/code collisions in other PDF objects stay outside
its claim. It never changes source scores or copies source font programs.
"""
import argparse,collections,hashlib,json
from pathlib import Path
from fontTools.ttLib import TTFont
from source.reviewed_catalog_roles import (CATALOG_HASHES,PENDING_HASH,EMPTY_AUDIT_HASH,
    selected_roles,HIDDEN_MUSIC,HIDDEN_NONMUSIC_EXCEPTIONS)

ROOT=Path(__file__).resolve().parent


def read_pinned(path,sha):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==sha,path
    return json.loads(path.read_text(encoding='utf-8'))


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    capture=json.loads(args.capture.read_text(encoding='utf-8'))
    families=['Kumo Score Study','Kumo Score Study Text']
    fonts={name:TTFont(args.fonts/name/(name+'.otf')) for name in families}
    source_hashes={};inventories={}
    def check_source(source,expected):
        if source not in source_hashes:
            source_hashes[source]=hashlib.sha256(Path(source).read_bytes()).hexdigest()
        assert source_hashes[source]==expected,source
    def check_targets(names):
        result=[]
        for name in sorted(set(names)):
            assert name in capture['glyphs'],name
            item=capture['glyphs'][name];cp=item['codepoint']
            assert all(cp in font.getBestCmap() for font in fonts.values()),name
            result.append(dict(symbol=name,codepoint=cp,music_and_text_present=True,
                capture_source_key=item.get('source_key'),capture_mode=item.get('mode')))
        return result
    catalogues={}
    for directory,sha in CATALOG_HASHES.items():
        data=read_pinned(args.study/directory/'catalog.json',sha);decisions=selected_roles(directory);rows=[]
        for key,row in data.items():
            code=row['unicode'][2:];assert code in decisions,(directory,code)
            names=decisions[code];assert bool(names)==(row['status']=='rendered'),key
            sample=row.get('sample')
            if sample:check_source(sample['source'],sample['sha256'])
            rows.append(dict(key=key,source_sample=sample,status='reviewed-selected-instance' if names else 'unrendered-selected-instance',
                symbols=check_targets(names),whole_corpus_occurrences_certified=False))
        catalogues[directory]=dict(rows=rows,selected_keys=len(rows),visible_selected_keys=sum(bool(r['symbols']) for r in rows))
    pending=read_pinned(args.study/'pending-fonts-01/catalog.json',PENDING_HASH)
    empty=read_pinned(args.study/'pending-empty-052/audit.json',EMPTY_AUDIT_HASH)
    empty_by_id={row['id']:row for row in empty['groups']};hidden=[]
    assert set(HIDDEN_MUSIC).isdisjoint(empty_by_id)
    for row in pending['groups']:
        key=row['id'];score=row['score']
        if score not in inventories:inventories[score]=json.loads((args.study/'corpus-v2'/(score+'.json')).read_text(encoding='utf-8'))
        inv=inventories[score];check_source(inv['source_path'],inv['sha256'])
        if key in empty_by_id:
            proof=empty_by_id[key]
            assert proof['visible_objects']==0 and len(proof['objects'])==row['objects']
            assert proof['sha256']==inv['sha256']
            category='all-font-objects-no-rendered-ink'
        elif key in HIDDEN_MUSIC:category='music-role-samples-reviewed'
        else:category='ordinary-type-samples-reviewed'
        hidden.append(dict(id=key,score=score,font=row['font'],category=category,
            symbols=check_targets(HIDDEN_MUSIC.get(key,[])),
            note=HIDDEN_NONMUSIC_EXCEPTIONS.get(key),samples=row['samples'],
            unshown_font_keys_individually_certified=key in empty_by_id))
    report=dict(selected_music_catalogues=catalogues,hidden_font_groups=hidden,
        selected_music_keys=sum(c['selected_keys'] for c in catalogues.values()),
        visible_selected_music_keys=sum(c['visible_selected_keys'] for c in catalogues.values()),
        hidden_categories=dict(collections.Counter(r['category'] for r in hidden)),source_hashes=source_hashes,
        font_hashes={name:hashlib.sha256((args.fonts/name/(name+'.otf')).read_bytes()).hexdigest() for name in families},
        whole_goal_complete=False,remaining=['Per-PDF encoding collisions and member semantics',
            'A064 full-page path-role audit','Unrendered music catalogue instances require independent no-ink review',
            'Actual print and unverified native symbol routes'])
    (args.output/'catalog-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for font in fonts.values():font.close()
    print('Selected music keys',report['selected_music_keys'],'visible',report['visible_selected_music_keys'])
    print('Hidden font groups',len(hidden),report['hidden_categories'])
    print('Assigned targets present in both final fonts; selected instances are not whole-corpus certification')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study',type=Path,default=ROOT/'dist')
    for name in ('capture','fonts','output'):p.add_argument('--'+name,type=Path,required=True)
    run(p.parse_args())
