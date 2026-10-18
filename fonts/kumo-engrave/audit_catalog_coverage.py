"""Reconcile all selected music catalogues and reviewed hidden-font samples.

No matcher label is promoted to a semantic decision. This checks the exact
reviewed instances; font-name/code collisions in other PDF objects stay outside
its claim. It never changes source scores or copies source font programs.
"""
import argparse,collections,hashlib,json
from pathlib import Path
from fontTools.ttLib import TTFont
from source.reviewed_catalog_roles import (CATALOG_HASHES,PENDING_HASH,EMPTY_AUDIT_HASH,
    EMPTY_CATALOG_AUDIT_HASH,EMPTY_CATALOG_CONTROLS_HASH,
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
    no_ink_proof=None
    empty_keys=set()
    assert bool(args.empty_audit)==bool(args.empty_controls),'Provide both no-ink audit and visible controls'
    if args.empty_audit:
        proof=read_pinned(args.empty_audit,EMPTY_CATALOG_AUDIT_HASH)
        controls=read_pinned(args.empty_controls,EMPTY_CATALOG_CONTROLS_HASH)
        assert proof['all_inventory_occurrences_accounted'] and proof['all_occurrences_no_ink'] and proof['source_unchanged']
        assert len(proof['rows'])==755 and proof['actual_source_character_count']==457 and proof['generated_spacing_count']==298
        assert all(r['dark_pixels']==0 and (r['minimum_luma'] in (None,255)) for r in proof['rows'])
        assert len(controls['rows'])==3 and controls['source_unchanged'] and all(r['dark_pixels']>0 for r in controls['rows'])
        isolated=controls['isolated_null_bitmap_objects']
        assert {(r['score'],r['page'],r['text_object_index']) for r in isolated}=={('A130',3,649),('A130',3,651)}
        assert all(len(r['renders'])==2 and all(v['luma']==[255,255] for v in r['renders']) for r in isolated)
        for score,sha in proof['source_hashes'].items():
            inv=json.loads((args.study/'corpus-v2'/(score+'.json')).read_text(encoding='utf-8'))
            assert inv['sha256']==sha
            check_source(inv['source_path'],sha)
        counts=collections.Counter((r['font'],'%04X'%r['codepoint']) for r in proof['rows'] if not r['generated_by_pdfium'])
        assert counts=={('Chaconne','0003'):86,('Chaconne','0020'):241,('CIDFont+F1','F020'):130}
        empty_keys={('chaconne-catalog-v2','0003'),('chaconne-catalog-v2','0020'),('cid1-catalog-v2','F020')}
        no_ink_proof=dict(actual_source_character_positions=457,generated_spacing_positions=298,
            original_inventory_characters=235,source_count=len(proof['source_hashes']),visible_controls=3,
            exact_white_rendered_positions=455,whole_objects_without_bitmap=2,
            null_bitmap_objects_independently_isolated_at_32x_64x=2,
            all_source_hashes_unchanged=True)
    catalogues={}
    for directory,sha in CATALOG_HASHES.items():
        data=read_pinned(args.study/directory/'catalog.json',sha);decisions=selected_roles(directory);rows=[]
        for key,row in data.items():
            code=row['unicode'][2:];assert code in decisions,(directory,code)
            names=decisions[code];assert bool(names)==(row['status']=='rendered'),key
            all_empty=(directory,code) in empty_keys
            sample=row.get('sample')
            if sample:check_source(sample['source'],sample['sha256'])
            rows.append(dict(key=key,source_sample=sample,status='reviewed-selected-instance' if names else
                ('all-target-code-source-positions-no-rendered-ink' if all_empty else 'unrendered-selected-instance'),
                symbols=check_targets(names),whole_corpus_occurrences_certified=all_empty))
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
        no_ink_catalogue_audit=no_ink_proof,
        font_hashes={name:hashlib.sha256((args.fonts/name/(name+'.otf')).read_bytes()).hexdigest() for name in families},
        whole_goal_complete=False,remaining=['Other per-PDF encoding collisions and unshown member semantics',
            'A064 per-member semantics beyond reviewed representatives',
            'Other unresolved per-PDF keys outside the three verified catalogue keys',
            'Actual print and unverified native symbol routes'])
    (args.output/'catalog-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for font in fonts.values():font.close()
    print('Selected music keys',report['selected_music_keys'],'visible',report['visible_selected_music_keys'])
    print('Hidden font groups',len(hidden),report['hidden_categories'])
    print('Assigned targets present in both final fonts; selected instances are not whole-corpus certification')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study',type=Path,default=ROOT/'dist')
    p.add_argument('--empty-audit',type=Path);p.add_argument('--empty-controls',type=Path)
    for name in ('capture','fonts','output'):p.add_argument('--'+name,type=Path,required=True)
    run(p.parse_args())
