"""Audit actual font-resource coverage and the current installable font payload.

Read-only: verifies source counters, reviewed representatives, blank positions,
actual final OTF geometry/coverage, native-proof font bytes, size evidence,
ZIP payload and protected originals. It does not equate font coverage with
every score occurrence's musical semantics or user aesthetic approval.
"""
import argparse
import collections
import hashlib
import json
import zipfile
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from source.reviewed_corpus_keys import CATALOG_SHA
from source.reviewed_font_resources import (RESOURCES_SHA,PROPOSALS_SHA,CONTEXT_SHA,WAVE_CONTEXT_SHA,
                                          APPROVED_BASELINE_GROUPS,CONTEXT_NOTES,roles)

ROOT=Path(__file__).resolve().parent
BLANK_SHA='35496a88ded70806c883490ef3d280bf232d8bda0cc98d25d343783d187d894d'
SOURCE_SCORE_SHA='4a62cc33723b1c19a207102f27425c983e9fd40d570a2ff65d7a818b82ac91ad'
SOURCE_PDF_SHA='58475eccac2a6e83f8da881ae2f44abeb3998ac7b8c236a33ab4c948f1f3faf5'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned(path,sha):
    assert digest(path)==sha,path
    return json.loads(path.read_text(encoding='utf-8'))


def outline(glyphset,name):
    pen=RecordingPen();glyphset[name].draw(pen);return pen.value


def run(args):
    data=pinned(args.resources,RESOURCES_SHA)
    baseline=pinned(args.baseline,CATALOG_SHA)
    proposals=pinned(args.matches,PROPOSALS_SHA)
    contexts=pinned(args.contexts,CONTEXT_SHA)
    wave_contexts=pinned(args.wave_contexts,WAVE_CONTEXT_SHA)
    blank=pinned(args.blank,BLANK_SHA)
    reviewed=roles();resource_by_id={r['id']:r for r in data['resources']}
    assert len(data['source_hashes'])==146 and len(resource_by_id)==len(data['resources'])==422
    assert len(data['rows'])==8502
    assert len({(r['resource'],r['codepoint']) for r in data['rows']})==8502
    expected={};source_font_objects=collections.Counter();source_chars=0
    family_scopes={(r['score'],r['font']) for r in baseline['rows']}
    for score,sha in data['source_hashes'].items():
        inv=json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        assert digest(Path(inv['source_path']))==sha==baseline['source_hashes'][score]==inv['sha256']
        for family,font in inv['fonts'].items():
            if (score,family) not in family_scopes:continue
            source_font_objects[score]+=font['objects']
            for cp,glyph in font['glyphs'].items():
                expected[score,family,int(cp[2:],16)]=glyph['count'];source_chars+=glyph['count']
        assert data['scan_counts'][score]['objects']==source_font_objects[score]
    actual=collections.Counter()
    resource_counts=collections.Counter()
    for r in data['rows']:
        parent=resource_by_id[r['resource']]
        assert (r['score'],r['font'],r['raw_name'])==(parent['score'],parent['font'],parent['raw_name'])
        actual[r['score'],r['font'],r['codepoint']]+=r['occurrences']
        resource_counts[r['resource']]+=r['occurrences']
    assert actual==expected and source_chars==854812
    assert sum(r['source_characters'] for r in resource_by_id.values())==854812
    assert all(resource_counts[r['id']]==r['source_characters'] for r in resource_by_id.values())
    assert data['pages_retained_until_document_capture_complete'] and data['resource_ids_are_run_local']
    assert not data['source_pdf_saved'] and data['source_hashes_unchanged']
    visible={r['id'] for r in data['rows'] if r['status']=='rendered'}
    members=[k for g in data['groups'] for k in g['members']]
    assert len(visible)==len(members)==8364 and set(members)==visible
    assert {g['id'] for g in data['groups']}==reviewed.keys() and len(reviewed)==347
    assert len(proposals['proposals'])==347 and len(APPROVED_BASELINE_GROUPS)==347
    # Explicitly reject the geometric notehead suggestion and check all page
    # evidence against the resource's actual chosen sample.
    assert next(r for r in proposals['proposals'] if r['group']=='F0223')['matches'][0]['symbols']==['noteheadBlack']
    assert reviewed['F0223']==['wiggleGlissando']
    by_id={r['id']:r for r in data['rows']};by_group={g['id']:g for g in data['groups']}
    assert set(contexts)|set(wave_contexts)==CONTEXT_NOTES.keys() and len(CONTEXT_NOTES)==13
    for gid,c in dict(contexts,**wave_contexts).items():
        rep=by_id[by_group[gid]['representative']]
        assert c['sample']['score']==rep['score'] and c['sample']['page']==rep['sample']['page']
        assert c['sample']['text_object_index']==rep['sample']['text_object_index']
        assert c['sample']['sha256']==data['source_hashes'][rep['score']]
    empty=[r for r in data['rows'] if r['status']!='rendered']
    assert len(empty)==138 and sum(r['occurrences'] for r in empty)==544
    assert all(r['family_code_status']=='needs-visibility-review' for r in empty)
    blank_counts=collections.Counter((r['score'],r['font'],r['codepoint']) for r in blank['rows'])
    resource_empty_counts=collections.Counter()
    for r in empty:resource_empty_counts[r['score'],r['font'],r['codepoint']]+=r['occurrences']
    assert blank_counts==resource_empty_counts and blank['all_pending_key_source_positions_accounted']
    build=json.loads((args.fonts/'build-report.json').read_text(encoding='utf-8'))
    capture=json.loads(args.capture.read_text(encoding='utf-8'))
    assert digest(args.capture)==build['capture_sha256'] and len(capture['glyphs'])==112
    geometry={};hashes={};live_fonts={}
    for family,item in build['fonts'].items():
        path=args.fonts/family/(family+'.otf')
        assert digest(path)==item['sha256'] and digest(Path(item['baseline']))==item['baseline_sha256']
        hashes[family]=item['sha256'];font=TTFont(path);base=TTFont(item['baseline'])
        live_fonts[family]=font;fg=font.getGlyphSet();bg=base.getGlyphSet()
        assert set(base.getBestCmap())<=set(font.getBestCmap())
        assert font.getGlyphOrder()[:len(base.getGlyphOrder())]==base.getGlyphOrder()
        allowed={r['glyph'] for r in item['changed'].values()}
        preserved=0
        for name in base.getGlyphOrder():
            if name not in allowed:
                assert outline(bg,name)==outline(fg,name), (family,name)
                assert base['hmtx'].metrics[name]==font['hmtx'].metrics[name],(family,name)
                preserved+=1
        meta=json.loads((args.fonts/family/(family+'.json')).read_text(encoding='utf-8'))
        assert meta['fontName']==family
        for name,change in item['changed'].items():
            pen=BoundsPen(fg);fg[change['glyph']].draw(pen)
            assert pen.bounds is not None
            assert all(abs(a/250-b)<1e-5 for a,b in zip(pen.bounds,change['bounds_sp'])),(family,name)
            assert font['hmtx'].metrics[change['glyph']][0]==change['advance']
            if change['smufl']:
                box=meta['glyphBBoxes'][name]
                assert box['bBoxSW']+box['bBoxNE']==change['bounds_sp'],(family,name,'metadata bounds')
                assert meta['glyphsWithAnchors'][name]==change['anchors'],(family,name,'metadata anchors')
            else:
                extra=meta['kumoUnicodeExtras'][name]
                assert extra['codepoint']==change['codepoint'] and extra['bounds_sp']==change['bounds_sp']
        geometry[family]=dict(base_glyphs=len(base.getGlyphOrder()),final_glyphs=len(font.getGlyphOrder()),
                              final_cmap=len(font.getBestCmap()),unprocessed_outlines_metrics_preserved=preserved,
                              processed_symbols=len(item['changed']))
        base.close()
    targets=sorted({s for names in reviewed.values() for s in names})
    assert len(targets)==105
    for name in targets:
        cp=capture['glyphs'][name]['codepoint']
        for family in ('Kumo Score Study','Kumo Score Study Text'):
            font=live_fonts[family];glyph=font.getBestCmap()[cp]
            pen=BoundsPen(font.getGlyphSet());font.getGlyphSet()[glyph].draw(pen)
            assert pen.bounds is not None,(family,name)
    for font in live_fonts.values():font.close()
    native=json.loads((args.native/'native-report.json').read_text(encoding='utf-8'))
    assert len(native['proofs'])==21 and digest(Path(native['host']))==native['host_sha256']
    for family,sha in hashes.items():assert digest(args.native/'ScoreFonts'/family/(family+'.otf'))==sha
    assert all(p['symbolRegistered'] and p['textRegistered'] and p['pages']>0 for p in native['proofs'].values())
    dynamics=json.loads((args.native/'dynamics-pixel-check.json').read_text(encoding='utf-8'))
    assert len(dynamics)==10 and all(r['shape_iou']==1 for r in dynamics)
    protection=json.loads((args.native/'score-protection.json').read_text(encoding='utf-8'))
    assert protection['source_unchanged'] and protection['source_sha256']==SOURCE_SCORE_SHA
    assert all(p['only_font_fields_changed'] and p['all_archive_assets_preserved'] for p in protection['copies'].values())
    sizes=json.loads(args.sizes.read_text(encoding='utf-8'))
    assert len(sizes['guards'])==5 and all(r['passed'] for r in sizes['guards'])
    calibration=json.loads((ROOT/'source/text_calibration.json').read_text(encoding='utf-8'))
    assert capture['text_calibration']['spec_sha256']==digest(ROOT/'source/text_calibration.json')
    assert calibration['groups']==capture['text_calibration']['groups']
    with zipfile.ZipFile(args.package) as archive:
        # Control families are native comparison fixtures. The user-facing
        # package has always installed only the two Study families.
        for family in ('Kumo Score Study','Kumo Score Study Text'):
            sha=hashes[family]
            found=[n for n in archive.namelist() if n.endswith('/'+family+'/'+family+'.otf') or n==family+'/'+family+'.otf']
            assert len(found)==1,(family,found)
            assert hashlib.sha256(archive.read(found[0])).hexdigest()==sha
            metadata=found[0][:-4]+'.json'
            assert archive.read(metadata)==(args.fonts/family/(family+'.json')).read_bytes()
    originals={str(args.score):digest(args.score),str(args.score_pdf):digest(args.score_pdf)}
    assert originals[str(args.score)]==SOURCE_SCORE_SHA and originals[str(args.score_pdf)]==SOURCE_PDF_SHA
    # Filesystem tree check keeps the corpus scope tied to the folder supplied
    # by the user, rather than to a stale list with fewer PDFs.
    inv0=json.loads((args.inventory/'A001.json').read_text(encoding='utf-8'))
    source_root=Path(inv0['source_path']).parent
    expected_paths={json.loads(p.read_text(encoding='utf-8'))['source_path'] for p in args.inventory.glob('A*.json')}
    assert {str(p.resolve()) for p in source_root.rglob('*.pdf')}==expected_paths and len(expected_paths)==146
    report=dict(resource_sha256=RESOURCES_SHA,resources=422,resource_keys=8502,visible_keys=8364,
                all_candidate_source_characters_accounted=854812,reviewed_representatives=347,
                source_contexts=13,music_targets=targets,target_count=105,blank_resource_keys=138,
                blank_source_positions=544,all_resource_keys_resolved=True,geometry=geometry,font_hashes=hashes,
                native_proof_cases=21,dynamics_cases=10,native_size_guards=sizes['guards'],
                native_host_sha256=native['host_sha256'],package_sha256=digest(args.package),
                original_hashes=originals,source_hashes_unchanged=True,production_fonts_unchanged=True,
                subset_resource_queue_closed=True,installable_payload_verified=True,
                every_occurrence_semantics_certified=False,original_font_program_recovered=False,
                user_aesthetic_approval_claimed=False)
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('422 live resources / 8502 resource-code keys / 854812 source characters reconciled')
    print('347 representatives / 105 existing roles; 138 blank keys / 544 source positions resolved')
    print('Current font geometry, Leland preservation, native proof font bytes, actual size evidence and ZIP verified')
    print('Protected PDF/MSCZ and all 146 corpus sources unchanged')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name,default in [('resources','font-resources-194/resources.json'),('baseline','all-candidate-keys-186/catalog.json'),
                         ('matches','resource-matches-195/matches.json'),('contexts','resource-context-196/catalog.json'),
                         ('wave-contexts','resource-wave-context-197/catalog.json'),('blank','candidate-blank-189/visibility.json'),
                         ('inventory','corpus-v3-176'),('fonts','corpus-font-141'),
                         ('capture','alternate-integrated-141/capture.json'),('native','corpus-native-142'),
                         ('sizes','native-size-audit-145/native-text-size-audit.json'),('package','kumo-score-study-0.500-local.zip')]:
        p.add_argument('--'+name,type=Path,default=ROOT/'dist'/default)
    p.add_argument('--score',type=Path,default=Path(r'C:\Users\Fred\OneDrive - yunzd\arr\如果有来生\如果有来生-release5.mscz'))
    p.add_argument('--score-pdf',type=Path,default=Path(r'C:\Users\Fred\OneDrive - yunzd\arr\如果有来生\如果有来生_arr_by_kumo.pdf'))
    p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
