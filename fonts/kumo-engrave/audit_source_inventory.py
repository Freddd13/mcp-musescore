"""Verify source inventory, delta decisions, independent visibility and fonts.

Reports the reviewed scope without claiming every member's musical semantics
or every same-code shape in the whole corpus has been individually certified.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from source.reviewed_inventory_delta import (DELTA_SHA,VISIBILITY_SHA,INVENTORY_SHA,
    MUSIC_KEYS,MUSIC_REPRESENTATIVES,ORDINARY_REPRESENTATIVES)

ROOT = Path(__file__).resolve().parent


def pinned(path, expected):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path
    return json.loads(path.read_text(encoding='utf-8'))


def run(args):
    data = pinned(args.delta, DELTA_SHA)
    visibility = pinned(args.visibility, VISIBILITY_SHA)
    inventory = pinned(args.inventory/'inventory.json', INVENTORY_SHA)
    assert inventory['schema'] == 3 and inventory['inventory_complete']
    assert inventory['completed_scores'] == 146 and inventory['completed_pages'] == 1135
    assert inventory['owned_source_characters'] == 925005
    assert inventory['generated_characters'] == 1435137 and inventory['unowned_source_characters'] == 0
    assert len(data['added']) == 595 and len(data['removed']) == 2 and len(data['rows']) == 6813
    assert data['all_new_key_occurrences_accounted'] and data['source_hashes_unchanged']
    expected = collections.Counter({(r['score'],r['font'],r['codepoint']):r['count'] for r in data['added']})
    assert expected == collections.Counter((r['score'],r['font'],r['codepoint']) for r in data['rows'])
    assert sorted(r['serial'] for r in data['reviews']) == list(range(1,504))
    assert MUSIC_REPRESENTATIVES.keys() | ORDINARY_REPRESENTATIVES == set(range(1,504))
    assert not (MUSIC_REPRESENTATIVES.keys() & ORDINARY_REPRESENTATIVES)
    assert visibility['delta_sha256'] == DELTA_SHA
    assert visibility['statuses'] == {'isolated-page-no-ink':72}
    assert len(visibility['controls']) == 57 and all(r['whole_page_2x_luma'][0] < 255 for r in visibility['controls'])
    key = lambda r:(r['score'],r['page'],r['text_object_index'])
    assert {key(r) for r in visibility['rows']} == {key(r) for r in data['unrendered_objects']}
    assert all(r['whole_page_2x_luma'] == r['local_32x_luma'] == [255,255] for r in visibility['rows'])
    zero_objects = {key(r) for r in data['rows'] if r['codepoint'] == 0 and r['status'] == 'ambiguous-visible-compound-review'}
    assert {key(r) for r in visibility['zero_code_visible_objects']} == zero_objects and len(zero_objects) == 17
    assert visibility['source_hashes_unchanged'] and not visibility['source_pdf_saved']
    assert len(visibility['removed_extraction_keys']) == 2
    assert all(r['actual_U0020_source_occurrences'] == 0 for r in visibility['removed_extraction_keys'])
    capture = json.loads(args.capture.read_text(encoding='utf-8'))
    previous = json.loads(args.previous_font_report.read_text(encoding='utf-8'))
    fonts = {n:TTFont(args.fonts/n/(n+'.otf')) for n in ('Kumo Score Study','Kumo Score Study Text')}
    hashes = {n:hashlib.sha256((args.fonts/n/(n+'.otf')).read_bytes()).hexdigest() for n in fonts}
    assert hashes == previous['font_hashes'], 'This audit must not change production fonts or sizes'
    targets = sorted({n for names in MUSIC_KEYS.values() for n in names})
    for name in targets:
        cp = capture['glyphs'][name]['codepoint']
        assert all(cp in f.getBestCmap() for f in fonts.values()), name
    for score, sha in data['source_hashes'].items():
        inv = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        assert hashlib.sha256(Path(inv['source_path']).read_bytes()).hexdigest() == sha == inv['sha256']
    report = dict(inventory_sha256=INVENTORY_SHA, delta_sha256=DELTA_SHA, visibility_sha256=VISIBILITY_SHA,
                  scores=146,pages=1135,owned_source_characters=925005,generated_characters_excluded=1435137,
                  unowned_source_characters=0,added_per_pdf_keys=595,added_source_positions=6813,
                  reviewed_representatives=503,reviewed_boards=21,additional_all_zero_objects_reviewed=17,
                  music_representatives=13,ordinary_representatives=490,music_targets=targets,
                  all_targets_already_present=True,font_hashes=hashes,fonts_unchanged=True,
                  blank_objects_independently_resolved=72,visible_page_controls=57,
                  source_hashes_unchanged=True,whole_goal_complete=False,
                  all_same_code_shapes_in_corpus_certified=False)
    for f in fonts.values():f.close()
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('146 PDFs / 1135 pages; 595 added keys / 6813 source positions accounted')
    print('503 representatives + all 17 visible U+0000 objects reviewed; 72 blank objects independently resolved')
    print('7 music keys / 13 representatives already covered; production fonts and sizes unchanged')


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name,default in [('delta','inventory-delta-review-179/delta.json'),('visibility','delta-visibility-181/visibility.json'),
                         ('inventory','corpus-v3-176'),('previous-font-report','hidden-coverage-174/hidden-coverage.json')]:
        p.add_argument('--'+name,type=Path,default=ROOT/'dist'/default)
    p.add_argument('--capture',type=Path,default=ROOT/'dist/alternate-integrated-141/capture.json')
    p.add_argument('--fonts',type=Path,default=ROOT/'dist/corpus-font-141')
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
