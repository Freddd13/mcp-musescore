"""Check explicit alternate-encoding shape decisions against the final fonts."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from source.reviewed_encoding_variants import VARIANTS_SHA, CONTEXT_SHA, SCORES, selected_encoding_roles

ROOT = Path(__file__).resolve().parent


def run(args):
    args.output.mkdir(parents=True, exist_ok=False)
    assert hashlib.sha256(args.variants.read_bytes()).hexdigest() == VARIANTS_SHA
    assert hashlib.sha256(args.contexts.read_bytes()).hexdigest() == CONTEXT_SHA
    data = json.loads(args.variants.read_text(encoding='utf-8'))
    contexts = json.loads(args.contexts.read_text(encoding='utf-8'))
    assert set(data['source_hashes']) == SCORES
    decisions = selected_encoding_roles()
    capture = json.loads(args.capture.read_text(encoding='utf-8'))
    fonts = {name: TTFont(args.fonts/name/(name+'.otf')) for name in ('Kumo Score Study', 'Kumo Score Study Text')}
    used = set()
    rows = []
    for group in data['groups']:
        cp = group['unicode'][2:]
        names = decisions[cp]
        targets = []
        for name in names:
            code = capture['glyphs'][name]['codepoint']
            assert all(code in font.getBestCmap() for font in fonts.values()), name
            targets.append(dict(symbol=name, codepoint=code, music_and_text_present=True))
        member_keys = {(m['score'], m['font'], m['unicode']) for m in group['members']}
        assert len(member_keys) == len(group['members']) and not used & member_keys
        used.update(member_keys)
        context = contexts.get(group['id'])
        representative = group['representative']
        if context:
            assert context['sample']['score'] == representative['score']
            assert context['sample']['page'] == representative['sample']['page']
            assert context['bounds_pt'] == representative['bounds_pt']
        rows.append(dict(id=group['id'], unicode=group['unicode'], targets=targets,
                         representative=representative, grouped_key_samples=len(group['members']),
                         page_context=context, all_occurrence_semantics_certified=False))
    assert used == {(r['score'], r['font'], r['unicode']) for r in data['rows'] if r['status'] == 'rendered'}
    assert {r['unicode'][2:] for r in data['rows'] if r['status'] == 'rendered'} == set(decisions)
    unrendered = [r for r in data['rows'] if r['status'] != 'rendered']
    assert len(unrendered) == 6 and all(r['unicode'] == 'U+0003' for r in unrendered)
    for score in SCORES:
        inv = json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        assert hashlib.sha256(Path(inv['source_path']).read_bytes()).hexdigest() == data['source_hashes'][score]
    result = dict(source_hashes=data['source_hashes'], source_unchanged=True,
                  per_pdf_key_samples=len(data['rows']), visible_key_samples=len(used),
                  reviewed_shape_groups=len(rows), distinct_visible_codes=len(decisions),
                  page_contexts=len(contexts), rows=rows, unrendered=unrendered,
                  all_occurrence_semantics_certified=False, whole_goal_complete=False,
                  font_hashes={name:hashlib.sha256((args.fonts/name/(name+'.otf')).read_bytes()).hexdigest() for name in fonts})
    for font in fonts.values():
        font.close()
    (args.output/'encoding-coverage.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Eight PDFs:', len(data['rows']), 'key samples;', len(used), 'visible;', len(rows), 'reviewed shape groups;', len(contexts), 'page contexts')
    print('All assigned targets present in final Music/Text; grouped membership is not independent all-occurrence semantics')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--variants', type=Path, default=ROOT/'dist/encoding-variants-161/variants.json')
    p.add_argument('--contexts', type=Path, default=ROOT/'dist/encoding-context-162/catalog.json')
    p.add_argument('--inventory', type=Path, default=ROOT/'dist/corpus-v2')
    for name in ('capture', 'fonts', 'output'):
        p.add_argument('--'+name, type=Path, required=True)
    run(p.parse_args())
