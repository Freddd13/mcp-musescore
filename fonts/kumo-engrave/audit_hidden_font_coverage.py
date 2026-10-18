"""Verify the full hidden-font object ledger and reviewed representative scope."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from source.reviewed_catalog_roles import (PENDING_HASH,HIDDEN_MUSIC,HIDDEN_NONMUSIC_EXCEPTIONS,
    HIDDEN_OBJECTS_HASH,HIDDEN_LAYOUT_HASH,HIDDEN_VISIBILITY_HASH,H112_TEXT_ALPHABET)

ROOT=Path(__file__).resolve().parent
OBJECTS_SHA=HIDDEN_OBJECTS_HASH
LAYOUT_SHA=HIDDEN_LAYOUT_HASH
VISIBILITY_SHA=HIDDEN_VISIBILITY_HASH


def pinned(path, sha):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==sha,path
    return json.loads(path.read_text(encoding='utf-8'))


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    data=pinned(args.objects,OBJECTS_SHA)
    layout=pinned(args.layout,LAYOUT_SHA)
    visibility=pinned(args.visibility,VISIBILITY_SHA)
    pending=pinned(args.catalog,PENDING_HASH)
    assert data['all_objects_accounted'] and data['source_unchanged']
    assert layout['input_sha256']==visibility['input_sha256']==OBJECTS_SHA
    assert layout['representatives']==len(data['representatives'])==2232 and layout['groups']==269 and layout['boards']==8
    indices=[i for placement in layout['placements'] for i in placement['indices']]
    assert sorted(indices)==list(range(2232)),'A representative is absent from the reviewed compact boards'
    key=lambda r:(r['score'],r['page'],r['text_object_index'])
    assert len({key(r) for r in data['objects']})==len(data['objects'])==4273
    invisible={key(r) for r in data['objects'] if r['status']!='rendered'}
    assert {key(r) for r in visibility['rows']}==invisible and len(invisible)==500
    assert visibility['statuses']=={'isolated-page-no-ink':50,'wholly-outside-visible-page':450}
    assert visibility['source_hashes_unchanged'] and visibility['no_source_pdf_saved']
    assert len(visibility['visible_controls'])==36 and all(r['whole_page_2x_luma'][0]<255 for r in visibility['visible_controls'])
    for row in visibility['rows']:
        assert row['level']==0
        if row['status']=='isolated-page-no-ink':
            assert row['whole_page_2x_luma']==row['local_32x_luma']==[255,255]
    keys={tuple(k) for k in data['source_keys']}
    rep_keys={(r['group'],r['font_slot'],c['codepoint']) for r in data['representatives']
              for c in r['source_characters'] if not c['generated']}
    assert keys==rep_keys and len(keys)==4111
    by_group=collections.defaultdict(list)
    for row in data['objects']:
        by_group[row['group']].append(row)
    old_keys={(g['id'],int(k[2:],16)) for g in pending['groups'] for k in g['keys']}
    actual_keys={(g,cp) for g,slot,cp in keys}
    assert old_keys<=actual_keys and len(old_keys)==3737 and len(actual_keys)==3866
    additions=actual_keys-old_keys
    assert collections.Counter(cp for g,cp in additions)=={32:118,0:6,9:1,10:1,11:1,12:1,13:1}
    decoded=collections.Counter(''.join(H112_TEXT_ALPHABET[c['codepoint']] for c in r['source_characters']
        if not c['generated']) for r in data['objects'] if r['group']=='H112')
    assert set(decoded)=={'l.h.','r.h.','cresc.','rit.','dim.','a tempo','molto dim.','molto rit.','poco a poco cresc.','poco rit.'}
    capture=json.loads(args.capture.read_text(encoding='utf-8'))
    fonts={name:TTFont(args.fonts/name/(name+'.otf')) for name in ('Kumo Score Study','Kumo Score Study Text')}
    decisions=[]
    for group in pending['groups']:
        gid=group['id']
        objects=by_group[gid]
        assert len(objects)==group['objects']
        visible=sum(r['status']=='rendered' for r in objects)
        targets=[]
        for name in sorted(HIDDEN_MUSIC.get(gid,[])):
            cp=capture['glyphs'][name]['codepoint']
            assert all(cp in font.getBestCmap() for font in fonts.values()),name
            targets.append(dict(symbol=name,codepoint=cp,music_and_text_present=True))
        category='music-roles-reviewed' if targets else ('no-visible-source-objects' if not visible else 'ordinary-type-reviewed')
        decisions.append(dict(id=gid,score=group['score'],font=group['font'],category=category,
                              source_objects=len(objects),rendered_objects=visible,
                              targets=targets,note=HIDDEN_NONMUSIC_EXCEPTIONS.get(gid),
                              all_occurrence_semantics_individually_certified=False))
    for score,sha in data['source_hashes'].items():
        inv=json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        assert hashlib.sha256(Path(inv['source_path']).read_bytes()).hexdigest()==sha==inv['sha256']
    report=dict(source_hashes=data['source_hashes'],source_hashes_unchanged=True,
                source_objects=4273,rendered_objects=3773,nonvisible_objects=500,
                reviewed_representatives=2232,all_source_keys_represented=4111,
                group_code_keys=3866,old_inventory_keys=3737,added_keys=sorted(additions),
                group_categories=dict(collections.Counter(r['category'] for r in decisions)),groups=decisions,
                H112_reviewed_ordinary_words=dict(decoded),
                font_hashes={name:hashlib.sha256((args.fonts/name/(name+'.otf')).read_bytes()).hexdigest() for name in fonts},
                whole_goal_complete=False,same_text_other_sizes_individually_certified=False)
    for font in fonts.values():font.close()
    (args.output/'hidden-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('All 4273 objects accounted; 2232 representative strings/orientations reviewed; all 4111 source keys represented')
    print('269 groups',report['group_categories'],'129 keys recovered from old whitespace/empty-string omission')
    print('All music targets present in final Music/Text; no font files or source scores changed')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name,default in [('objects','hidden-all-objects-169/objects.json'),('layout','hidden-compact-171/layout.json'),
                         ('visibility','hidden-visibility-172/visibility.json'),('catalog','pending-fonts-01/catalog.json'),
                         ('inventory','corpus-v2')]:p.add_argument('--'+name,type=Path,default=ROOT/'dist'/default)
    for name in ('capture','fonts','output'):p.add_argument('--'+name,type=Path,required=True)
    run(p.parse_args())
