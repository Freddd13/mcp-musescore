"""Verify source protection, corpus coverage records and private render availability."""
import hashlib
import json
from pathlib import Path
import re
import sys
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
BASE = REPO/'docs/engraving'
PRIVATE = REPO/'tmp/engraving'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    inventory = json.loads((BASE/'corpus/inventory.json').read_text(encoding='utf-8'))
    review = json.loads((BASE/'corpus/reviews.json').read_text(encoding='utf-8'))
    rows = inventory['scores']
    assert len(rows) == inventory['score_count']
    assert sum(r['pages'] for r in rows) == inventory['total_pages']
    current_sources = sorted(str(p) for p in Path(inventory['source_root']).rglob('*.pdf'))
    assert current_sources == sorted(r['source_path'] for r in rows), 'Source directory changed; update inventory.'
    source_results = []
    page_count = 0
    for row in rows:
        assert row['inventory_status'] == 'readable'
        assert sha(row['source_path']) == row['sha256'], row['id']+' source modified'
        source_results.append({'id': row['id'], 'unchanged': True})
        directory = PRIVATE/'corpus'/row['id']
        rendered = sorted(directory.glob('page-*.jpg'), key=lambda p: int(p.stem.split('-')[-1]))
        assert len(rendered) == row['pages'], row['id']+' missing renders'
        assert [int(p.stem.split('-')[-1]) for p in rendered] == list(range(1,row['pages']+1))
        log = json.loads((directory/'render.json').read_text(encoding='utf-8'))
        assert log['source_sha256'] == row['sha256'] and log['returncode'] == 0
        for image in rendered:
            with Image.open(image) as im:
                assert im.width == log['width'] and im.height > 0
                im.verify()
        assert len(list(directory.glob('board-*.jpg'))) == (row['pages']+5)//6
        page_count += len(rendered)
    assert review['reviewed_score_count'] == len(review['scores'])
    for row in review['scores']:
        source = next(s for s in rows if s['id'] == row['id'])
        assert row['source_sha256'] == source['sha256']
        assert row['all_pages_screened'] == list(range(1,source['pages']+1))
        assert set(row['full_page_detail_viewed']) <= set(row['all_pages_screened'])
        assert sorted(set(row['overview_only_pages'])|set(row['full_page_detail_viewed'])) == row['all_pages_screened']
        assert (BASE/'corpus'/row['note']).is_file()
        assert row['id'] in (BASE/'corpus'/row['note']).read_text(encoding='utf-8')
    assert review['screened_pages'] == sum(len(r['all_pages_screened']) for r in review['scores'])
    assert review['detail_pages'] == sum(len(r['full_page_detail_viewed']) for r in review['scores'])
    assert review['all_scores_complete'] == (len(review['scores']) == inventory['score_count'])
    for row in review.get('partial_scores', []):
        source = next(s for s in rows if s['id'] == row['id'])
        assert row['source_sha256'] == source['sha256']
        assert set(row['screened_pages']).isdisjoint(row['remaining_pages'])
        assert sorted(row['screened_pages']+row['remaining_pages']) == list(range(1,source['pages']+1))
        assert set(row['full_page_detail_viewed']) <= set(row['screened_pages'])
        assert (BASE/'corpus'/row['note']).is_file()
    migration = json.loads((PRIVATE/'cache-migration.json').read_text(encoding='utf-8'))
    assert migration['verified'] and not Path(migration['source']).exists()
    migrated = Path(migration['destination'])
    for row in migration['files']:
        assert sha(migrated/row['relative']) == row['sha256'], 'Legacy evidence changed.'
    old_protection = json.loads((BASE/'spacing_evidence.json').read_text(encoding='utf-8'))['protected_sources']
    prior_results = [{'path': r['path'], 'matches_prior_baseline': sha(r['path']) == r['before_sha256']} for r in old_protection]
    docs = ['CONTINUOUS_STUDY.md','CACHE_LOCATIONS.md','NOTATION_DETAILS.md','RESOURCE_RESEARCH.md','README.md',
            'BEAM_STEM_STUDY.md','RESOURCE_PLAN_MAPPING.md','INPUT_HISTORY.md','EXTERNAL_PRACTICE.md']
    docs += [str(p.relative_to(BASE)) for p in (BASE/'corpus').glob('*.md')]
    for name in docs:
        path = BASE/name
        text = path.read_text(encoding='utf-8')
        assert all(line == line.rstrip() for line in text.splitlines()), name+' trailing whitespace'
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('https://','http://','#')):
                continue
            assert (path.parent/target.split('#')[0]).exists(), name+' broken link '+target
    compile((REPO/'tools/engraving/corpus.py').read_text(encoding='utf-8'), 'corpus.py', 'exec')
    report = {
        'date': '2026-10-18', 'result': 'passed', 'sources_unchanged': len(source_results),
        'source_directory_matches_inventory': True, 'rendered_pages': page_count,
        'reviewed_scores_documented': len(review['scores']), 'screened_pages_recorded': review['screened_pages'],
        'detail_pages_recorded': review['detail_pages'],
        'partial_scores_documented': len(review.get('partial_scores', [])),
        'partial_screened_pages_recorded': sum(len(r['screened_pages']) for r in review.get('partial_scores', [])),
        'review_limit': 'Visual reading is recorded by the analyst. This verifier checks indices, files and consistency; it cannot establish depth of understanding or aesthetic quality.',
        'migration_files_verified': migration['file_count'], 'migration_bytes': migration['bytes'],
        'legacy_c_directory_absent': True, 'prior_protected_sources': prior_results,
        'entire_objective_complete': False, 'planning_body_obtained': True,
        'planning_body_source': 'User pasted the planning text on 2026-10-18; see RESOURCE_PLAN_MAPPING.md. Source research remains incomplete.',
        'historical_input_differences': [r['path'] for r in prior_results if not r['matches_prior_baseline']],
        'sources': source_results,
    }
    target = BASE/'corpus/verification.json'
    target.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print(json.dumps({k:v for k,v in report.items() if k not in ['sources','prior_protected_sources','review_limit']},ensure_ascii=False))


if __name__ == '__main__':
    main()
