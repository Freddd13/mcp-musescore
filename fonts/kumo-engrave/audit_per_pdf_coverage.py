"""Verify exhaustive per-PDF non-text key partition and reviewed role scope.

This closes the family/code key queue, not raw subset-font variants, every
occurrence's musical meaning, or user aesthetic approval of every glyph.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from source.reviewed_corpus_keys import CATALOG_SHA,CONTEXT_NOTES,roles
from source.reviewed_catalog_roles import HIDDEN_OBJECTS_HASH,PENDING_HASH
from source.reviewed_inventory_delta import INVENTORY_SHA

ROOT=Path(__file__).resolve().parent
BLANK_SHA='35496a88ded70806c883490ef3d280bf232d8bda0cc98d25d343783d187d894d'
CONTEXT_SHA='eadb8f36b1b885ce98d6f9c6b55aa8a0a5731370e8d9e51daf6548287b4428cc'


def pinned(path,expected):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,path
    return json.loads(path.read_text(encoding='utf-8'))


def run(args):
    inventory=pinned(args.inventory/'inventory.json',INVENTORY_SHA)
    catalog=pinned(args.catalog,CATALOG_SHA)
    blank=pinned(args.blank,BLANK_SHA)
    contexts=pinned(args.contexts,CONTEXT_SHA)
    hidden=pinned(args.hidden,HIDDEN_OBJECTS_HASH)
    hidden_groups=pinned(args.hidden_groups,PENDING_HASH)
    reviewed=roles()
    assert inventory['completed_scores']==len(catalog['source_hashes'])==146
    assert inventory['completed_pages']==1135
    actual={(r['score'],r['font'],r['codepoint']) for r in catalog['rows']}
    assert len(actual)==len(catalog['rows'])==5723
    candidate_families={(r['score'],r['font']) for r in catalog['rows']}
    keys=set();excluded=set();subsets=[]
    for score,sha in catalog['source_hashes'].items():
        inv=json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        assert hashlib.sha256(Path(inv['source_path']).read_bytes()).hexdigest()==sha==inv['sha256']
        for family,font in inv['fonts'].items():
            if font['category']!='text':
                keys.update((score,family,int(cp[2:],16)) for cp in font['glyphs'])
                if (score,family) in candidate_families and len(font['raw_names'])>1:
                    subsets.append(dict(score=score,font=family,raw_names=font['raw_names']))
    for row in catalog['skipped_font_groups']:
        if row['category']=='unclassified':
            inv=json.loads((args.inventory/(row['score']+'.json')).read_text(encoding='utf-8'))
            excluded.update((row['score'],row['font'],int(cp[2:],16)) for cp in inv['fonts'][row['font']]['glyphs'])
    assert len(keys)==9591 and len(excluded)==3868
    assert actual|excluded==keys and not actual&excluded
    by_group={r['id']:(r['score'],r['font']) for r in hidden_groups['groups']}
    known_hidden={by_group[g]+(cp,) for g,slot,cp in hidden['source_keys']}
    assert len(known_hidden)==3866 and known_hidden<=excluded
    assert excluded-known_hidden=={('A125','FEF3203D4E1',0),('A132','FEFC71BC52D',0)}
    rendered={r['id'] for r in catalog['rows'] if r['status']=='rendered'}
    members=[r for g in catalog['groups'] for r in g['members']]
    assert set(members)==rendered and len(members)==len(rendered)==5606
    assert {g['id'] for g in catalog['groups']}==reviewed.keys() and len(reviewed)==343
    assert all(g['minimum_similarity']>=.96 for g in catalog['groups'])
    assert set(contexts)==set(CONTEXT_NOTES) and len(contexts)==16
    by_id={r['id']:r for r in catalog['rows']}
    by_id_group={g['id']:g for g in catalog['groups']}
    for gid,row in contexts.items():
        rep=by_id[by_id_group[gid]['representative']]
        assert row['sample']['score']==rep['score'] and row['sample']['page']==rep['sample']['page']
        assert row['sample']['text_object_index']==rep['sample']['text_object_index']
        assert row['bounds_pt']==rep['bounds_pt']
        assert row['sample']['sha256']==catalog['source_hashes'][rep['score']]
    assert blank['catalog_sha256']==CATALOG_SHA and blank['all_pending_key_source_positions_accounted']
    pending={(r['score'],r['font'],r['codepoint']):r['occurrences'] for r in catalog['rows'] if r['status']!='rendered'}
    assert len(pending)==117 and sum(pending.values())==544
    assert collections.Counter((r['score'],r['font'],r['codepoint']) for r in blank['rows'])==pending
    previous=json.loads(args.previous_font_report.read_text(encoding='utf-8'))
    capture=json.loads(args.capture.read_text(encoding='utf-8'))
    fonts={n:TTFont(args.fonts/n/(n+'.otf')) for n in ('Kumo Score Study','Kumo Score Study Text')}
    hashes={n:hashlib.sha256((args.fonts/n/(n+'.otf')).read_bytes()).hexdigest() for n in fonts}
    assert hashes==previous['font_hashes']
    targets=sorted({name for names in reviewed.values() for name in names})
    for name in targets:
        cp=capture['glyphs'][name]['codepoint']
        assert all(cp in font.getBestCmap() for font in fonts.values()),name
    assert len(subsets)==18
    report=dict(catalog_sha256=CATALOG_SHA,blank_sha256=BLANK_SHA,context_sha256=CONTEXT_SHA,
                all_non_text_per_pdf_keys=9591,candidate_keys=5723,visible_keys=5606,
                reviewed_group_representatives=343,reviewed_boards=8,source_contexts=16,
                blank_keys=117,blank_actual_source_positions=544,
                previously_reviewed_hidden_keys=3866,previously_reviewed_zero_keys=2,
                all_non_text_keys_partitioned=True,targets=targets,target_count=len(targets),
                all_targets_present_in_music_and_text=True,font_hashes=hashes,fonts_unchanged=True,
                source_hashes_unchanged=True,raw_subset_families_remaining=subsets,
                every_group_member_semantics_certified=False,raw_subset_variants_certified=False,
                whole_goal_complete=False)
    for font in fonts.values():font.close()
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('9591 non-text keys partitioned: 5723 candidates + 3866 hidden + 2 U+0000')
    print('5606 visible keys / 343 reviewed representatives / 104 targets already present')
    print('117 blank keys / all 544 source positions accounted; fonts unchanged')
    print('Next: raw subset variants in 18 family/PDF pairs; no completion claim yet')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name,default in [('inventory','corpus-v3-176'),('catalog','all-candidate-keys-186/catalog.json'),
                         ('blank','candidate-blank-189/visibility.json'),('contexts','all-key-context-188/catalog.json'),
                         ('hidden','hidden-all-objects-169/objects.json'),('hidden-groups','pending-fonts-01/catalog.json'),
                         ('previous-font-report','source-inventory-coverage-182/coverage.json'),
                         ('capture','alternate-integrated-141/capture.json'),('fonts','corpus-font-141')]:
        p.add_argument('--'+name,type=Path,default=ROOT/'dist'/default)
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
