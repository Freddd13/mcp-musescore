"""Account for A064 paths and verify reviewed representative target availability.

No matcher labels are used and no font outlines are changed. Source PDF files
are read only. Member accounting is exhaustive; semantic review is explicitly
limited to representatives and the listed page contexts.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from source.reviewed_path_roles import (PATHS_SHA, GROUPS_SHA, CONTEXT_HASHES,
                                       CANCELLATION_HASH, reviewed_roles)

ROOT = Path(__file__).resolve().parent


def read_pinned(path, expected):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path
    return json.loads(path.read_text(encoding='utf-8'))


def run(args):
    args.output.mkdir(parents=True, exist_ok=False)
    data = read_pinned(args.study/'A064-paths-03/paths.json', PATHS_SHA)
    groups = read_pinned(args.study/'path-groups-089/groups.json', GROUPS_SHA)
    cancelled = read_pinned(args.study/'path-cancellation-153/cancellation.json', CANCELLATION_HASH)
    source = Path(data['source'])
    assert hashlib.sha256(source.read_bytes()).hexdigest() == data['sha256']
    assert cancelled['sha256'] == data['sha256'] and cancelled['source_unchanged']
    assert cancelled['exact_stored_coordinates'] and not cancelled['coordinate_comparison_rounding_pt']
    contexts = {}
    for name, sha in CONTEXT_HASHES.items():
        for row in read_pinned(args.study/name, sha):
            contexts.setdefault(row['role_candidate'], []).append(row)
    decisions = reviewed_roles()
    assert {int(g['id'][1:]) for g in groups['groups']} == set(decisions)
    capture = json.loads(args.capture.read_text(encoding='utf-8'))
    fonts = {name: TTFont(args.fonts/name/(name+'.otf'))
             for name in ('Kumo Score Study', 'Kumo Score Study Text')}
    members = collections.Counter()
    rows = []
    for group in groups['groups']:
        decision = decisions[int(group['id'][1:])]
        targets = []
        for name in decision['targets']:
            cp = capture['glyphs'][name]['codepoint']
            assert all(cp in font.getBestCmap() for font in fonts.values()), name
            targets.append(dict(symbol=name, codepoint=cp, music_and_text_present=True))
        for m in group['members']:
            members[(m['page'], m['object_index'])] += 1
        first = group['members'][0]
        for c in contexts.get(group['id'], []):
            assert (c['page'], c['object_index']) == (first['page'], first['object_index'])
        rows.append(dict(id=group['id'], category=decision['category'], targets=targets,
                         note=decision['note'], representative=dict(page=first['page'], object_index=first['object_index']),
                         grouped_members=len(group['members']), page_contexts=contexts.get(group['id'], []),
                         all_member_semantics_certified=False))
    assert all(n == 1 for n in members.values()), 'Duplicate path membership'
    blank = {(r['page'], r['object_index']) for r in cancelled['matching_cancelled_paths']}
    assert len(blank) == 10 and set(members).isdisjoint(blank)
    source_keys = {(r['page'], r['object_index']) for r in data['paths']}
    assert len(source_keys) == len(data['paths']) == 7299
    assert set(members) | blank == source_keys and len(members) == 7289
    report = dict(source=str(source), sha256=data['sha256'], source_unchanged=True,
                  input_paths=7299, visible_grouped_members=7289, reverse_cancelled_paths=10,
                  reviewed_representatives=len(rows), all_member_accounting=True,
                  all_member_semantics_certified=False, whole_goal_complete=False,
                  category_counts=dict(collections.Counter(r['category'] for r in rows)),
                  page_context_instances=sum(len(r['page_contexts']) for r in rows),
                  distinct_context_representatives=sum(bool(r['page_contexts']) for r in rows),
                  font_hashes={name:hashlib.sha256((args.fonts/name/(name+'.otf')).read_bytes()).hexdigest() for name in fonts},
                  rows=rows, remaining=['Cross-PDF font/code shape variants and unshown members',
                                       'Unrendered music-catalogue samples: all-occurrence check',
                                       'Unverified native routes, scale/print review'])
    for font in fonts.values():
        font.close()
    (args.output/'path-role-coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Paths 7299 = 7289 grouped + 10 reverse-cancelled; representatives', len(rows))
    print('Categories', report['category_counts'])
    print('Context instances', report['page_context_instances'], 'distinct representatives', report['distinct_context_representatives'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study', type=Path, default=ROOT/'dist')
    p.add_argument('--capture', type=Path, required=True)
    p.add_argument('--fonts', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    run(p.parse_args())
