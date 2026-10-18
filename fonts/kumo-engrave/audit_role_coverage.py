"""Reconcile manually reviewed representative roles with the actual local fonts.

Requires fontTools. No automatic matcher label is promoted to a decision. Source
hashes, representative locations, member counts and engine gaps stay explicit.
"""
import argparse,hashlib,json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from source.symbol_names import load_symbol_names

ROOT=Path(__file__).resolve().parent


def run(args):
    args.output.mkdir(parents=True,exist_ok=False)
    spec=json.loads(args.decisions.read_text(encoding='utf-8'))
    assert hashlib.sha256(args.groups.read_bytes()).hexdigest()==spec['groups_sha256']
    groups=json.loads(args.groups.read_text(encoding='utf-8'));capture=json.loads(args.capture.read_text(encoding='utf-8'))
    decisions={}
    for role in spec['roles']:
        for number in role['groups'].split():
            key='G'+number;assert key not in decisions,key;decisions[key]=role
    assert set(decisions)=={g['id'] for g in groups['groups']},'Every group needs an explicit reviewed decision'
    contexts={}
    for path in args.contexts:
        for key,value in json.loads(path.read_text(encoding='utf-8')).items():
            assert key not in contexts,key;contexts[key]=value
    assert set(contexts)=={'G'+number for number in spec['page_context_confirmations']}
    fonts=[TTFont(args.fonts/family/(family+'.otf')) for family in ('Kumo Score Study','Kumo Score Study Text')]
    baseline=TTFont(ROOT/'vendor/leland/Leland.otf');names=load_symbol_names(args.glyphnames)
    inventories={};source_hashes={};rows=[]
    for group in groups['groups']:
        key=group['id'];role=decisions[key];sample=group['members'][0];score=sample['score']
        if score not in inventories:inventories[score]=json.loads((args.inventory/(score+'.json')).read_text(encoding='utf-8'))
        inv=inventories[score];source=inv['source_path']
        if source not in source_hashes:
            actual=hashlib.sha256(Path(source).read_bytes()).hexdigest();assert actual==inv['sha256'];source_hashes[source]=actual
        if key in contexts:
            reference=contexts[key]['sample']
            assert reference['source']==source and reference['sha256']==inv['sha256']
            assert reference['page']==sample['page'] and reference['text_object_index']==sample['object_index']
        symbols=[]
        for name in role['symbols']:
            item=capture['glyphs'].get(name);assert item is not None,(key,name)
            cp=item['codepoint'];assert all(cp in font.getBestCmap() for font in fonts),(key,name)
            symbols.append(dict(symbol=name,codepoint=cp,music_and_text_present=True))
        rows.append(dict(group=key,role=role['role'],symbols=symbols,source=source,source_sha256=source_hashes[source],
            representative=dict(score=score,font=sample['font'],unicode=sample['unicode'],page=sample['page'],text_object_index=sample['object_index']),
            member_samples=len(group['members']),scope='representative-only',
            context_confirmation=spec['page_context_confirmations'].get(key[1:]),
            native_route=role.get('native_route','normal-symbol-route'),member_semantics=role.get('member_semantics','not-individually-certified')))
    fallback=[];base_map=baseline.getBestCmap();study=fonts[0];study_map=study.getBestCmap()
    for name in spec['fallbacks_not_confirmed_in_this_batch']:
        cp=int(names[name]['codepoint'][2:],16);assert cp in base_map and cp in study_map,name
        a,b=RecordingPen(),RecordingPen();baseline.getGlyphSet()[base_map[cp]].draw(a);study.getGlyphSet()[study_map[cp]].draw(b)
        assert a.value==b.value and baseline['hmtx'].metrics[base_map[cp]]==study['hmtx'].metrics[study_map[cp]],name
        fallback.append(dict(symbol=name,codepoint=cp,unchanged_leland_outline_and_metrics=True,status='not-confirmed-in-this-review-batch'))
    report=dict(scope=spec['scope'],groups=len(rows),member_samples=sum(r['member_samples'] for r in rows),
        context_confirmations=sum(r['context_confirmation'] is not None for r in rows),
        source_hashes=source_hashes,rows=rows,fallbacks=fallback,completion_claim=False)
    report['font_hashes']={family:hashlib.sha256((args.fonts/family/(family+'.otf')).read_bytes()).hexdigest() for family in ('Kumo Score Study','Kumo Score Study Text')}
    (args.output/'role-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for font in fonts+[baseline]:font.close()
    print('Reviewed representative groups',len(rows),'member samples represented',report['member_samples'],'page contexts',report['context_confirmations'])
    print('All assigned target glyphs present in both families;',len(fallback),'explicit Leland fallbacks unchanged; whole-corpus completion not claimed')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--decisions',type=Path,default=ROOT/'source/reviewed_role_decisions.json')
    p.add_argument('--groups',type=Path,default=ROOT/'dist/symbol-review-groups-069/groups.json')
    p.add_argument('--inventory',type=Path,default=ROOT/'dist/corpus-v2')
    p.add_argument('--contexts',type=Path,nargs='+',default=[ROOT/'dist/role-context-106/catalog.json',ROOT/'dist/role-context-107/catalog.json'])
    p.add_argument('--glyphnames',type=Path,default=Path('E:/programming/funcodes/muse3_dev/MuseScore/fonts/smufl/glyphnames.json'))
    for name in ('capture','fonts','output'):p.add_argument('--'+name,type=Path,required=True)
    run(p.parse_args())
