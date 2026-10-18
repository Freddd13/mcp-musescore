"""Build local music/Text study fonts, retaining complete Leland baselines.

PDF-derived data and fonts stay in ignored dist/, outside public build.py.
Requires fontTools. No OS installation and no source-score modification.
"""
import argparse,copy,hashlib,json,math
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from build import ROOT,rename,bounds
from source.contours import vertical_edges,inside,area
from source.pdf_symbol_map import LIGATURES


def ink_intervals(loops,x):
    """Filled intervals at x, including separated arms and contour holes."""
    hits=[]
    for points in loops:
        for a,b in zip(points,points[1:]+points[:1]):
            if min(a[0],b[0])<=x<max(a[0],b[0]):
                hits.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
    hits=sorted(set(hits));result=[]
    for low,high in zip(hits,hits[1:]):
        if high-low>1e-7 and sum(inside(v,(x,(low+high)/2)) for v in loops)%2:
            result.append((low,high))
    assert result,('No filled interval',x)
    return result


def add_ligatures(font,rules):
    """Append simple ligature lookups while preserving baseline GSUB features."""
    baseline=copy.deepcopy(font['GSUB']) if 'GSUB' in font else None
    preserved={tag:copy.deepcopy(font[tag]) for tag in ('GPOS','GDEF') if tag in font}
    addOpenTypeFeaturesFromString(font,'feature liga {\n'+'\n'.join(rules)+'\n} liga;')
    for tag,table in preserved.items():font[tag]=table
    if baseline is None:return
    added=font['GSUB'].table;old=baseline.table
    offset=len(old.LookupList.Lookup)
    assert all(v.LookupType==4 for v in added.LookupList.Lookup)
    old.LookupList.Lookup.extend(added.LookupList.Lookup);old.LookupList.LookupCount=len(old.LookupList.Lookup)
    existing={}
    for i,r in enumerate(old.FeatureList.FeatureRecord):existing.setdefault(r.FeatureTag,[]).append(i)
    new_features=[];feature_groups=[]
    for record in added.FeatureList.FeatureRecord:
        lookups=[offset+i for i in record.Feature.LookupListIndex]
        if record.FeatureTag in existing:
            indices=existing[record.FeatureTag]
            for index in indices:
                feature=old.FeatureList.FeatureRecord[index].Feature
                feature.LookupListIndex=lookups+feature.LookupListIndex
                feature.LookupCount=len(feature.LookupListIndex)
        else:
            record.Feature.LookupListIndex=lookups
            index=len(old.FeatureList.FeatureRecord);old.FeatureList.FeatureRecord.append(record)
            indices=[index]
        new_features.append(indices[0]);feature_groups.append(indices)
    old.FeatureList.FeatureCount=len(old.FeatureList.FeatureRecord)
    for script in old.ScriptList.ScriptRecord:
        languages=([script.Script.DefaultLangSys] if script.Script.DefaultLangSys else [])
        languages += [v.LangSys for v in script.Script.LangSysRecord]
        for lang in languages:
            for indices in feature_groups:
                if not any(i in lang.FeatureIndex for i in indices):lang.FeatureIndex.append(indices[0])
            lang.FeatureIndex=sorted(lang.FeatureIndex);lang.FeatureCount=len(lang.FeatureIndex)
    if not any(r.ScriptTag=='DFLT' for r in old.ScriptList.ScriptRecord):
        script=next(r for r in added.ScriptList.ScriptRecord if r.ScriptTag=='DFLT')
        script.Script.DefaultLangSys.FeatureIndex=new_features
        script.Script.DefaultLangSys.FeatureCount=len(new_features)
        old.ScriptList.ScriptRecord.append(script);old.ScriptList.ScriptCount=len(old.ScriptList.ScriptRecord)
    font['GSUB']=baseline


def write_font(base_path,out,family,data,sm,control=False,text=False):
    out.mkdir(parents=True,exist_ok=False)
    font=TTFont(base_path,recalcTimestamp=False);original_order=list(font.getGlyphOrder());cmap=dict(font.getBestCmap())
    version=data.get('version','0.410')
    rename(font,family,version,' Local unpublished user-PDF shape study; not the Chaconne font program.')
    font['name'].setName('Leland baseline retains OFL. Reference-derived portions are local study material; no redistribution license is granted for them.',13,3,1,0x409)
    top=font['CFF '].cff.topDictIndex[0]
    meta=copy.deepcopy(json.loads((ROOT/'vendor/leland/leland_metadata.json').read_text(encoding='utf-8'))) if not text else dict(glyphBBoxes={},glyphsWithAnchors={})
    report=dict(family=family,baseline=str(base_path),baseline_sha256=hashlib.sha256(base_path.read_bytes()).hexdigest(),changed={},added=[],ligatures=[])
    if not control:
        for symbol,item in data['glyphs'].items():
            cp=item['codepoint'];glyph=cmap.get(cp);loops=item['outlines'];box=item['bounds'];advance=item['advance']
            standard=symbol in sm
            if not standard:assert glyph is None,('Custom Unicode collides with baseline',symbol,cp)
            if glyph is None:
                glyph='uni%04X'%cp
                assert glyph not in font.getGlyphOrder()
                order=list(font.getGlyphOrder())+[glyph];font.setGlyphOrder(order)
                # Indexed CFF charstrings: register the new name and index.
                top.charset=order
                top.CharStrings.charStrings[glyph]=len(top.CharStrings.charStringsIndex.items)
                top.CharStrings.charStringsIndex.append(None)
                for table in font['cmap'].tables:
                    if table.isUnicode():table.cmap[cp]=glyph
                cmap[cp]=glyph;report['added'].append(symbol)
            pen=T2CharStringPen(advance-getattr(top.Private,'nominalWidthX',0),font.getGlyphSet(),roundTolerance=0)
            if item.get('commands'):
                for op,points in item['commands']:
                    assert op in ('moveTo','lineTo','curveTo','closePath')
                    points=[tuple(round(v*65536)/65536 for v in p) for p in points]
                    getattr(pen,op)(*points)
            else:
                for points in loops:
                    points=[tuple(round(v*65536)/65536 for v in p) for p in points]
                    pen.moveTo(points[0])
                    for p in points[1:]:pen.lineTo(p)
                    pen.closePath()
            top.CharStrings[glyph]=pen.getCharString(private=top.Private,globalSubrs=top.GlobalSubrs,optimize=not bool(item.get('commands')))
            font['hmtx'].metrics[glyph]=(advance,int(math.floor(box[0])))
            if standard:
                meta['glyphBBoxes'][symbol]=dict(bBoxSW=[v/250 for v in box[:2]],bBoxNE=[v/250 for v in box[2:]])
                anchors=meta['glyphsWithAnchors'].setdefault(symbol,{})
            else:
                # These are explicit Unicode Text extras, not unknown SMuFL
                # names for the host to resolve as noSym.
                meta.setdefault('kumoUnicodeExtras',{})[symbol]=dict(codepoint=cp,bounds_sp=[v/250 for v in box],usage=item['usage'])
                anchors={}
            # Conservative cutouts bound the new ink; old Leland cutout gaps
            # cannot be assumed to survive a different outline.
            for key in list(anchors):
                if key.startswith('cutOut'):
                    anchors[key]=[(box[0] if key.endswith(('NW','SW')) else box[2])/250,
                                  (box[3] if key.endswith(('NW','NE')) else box[1])/250]
            if symbol in ('noteheadBlack','noteheadHalf'):
                for key,x,side,inset in [('stemDownNW',box[0]+2,box[0],12),('stemUpSE',box[2]-2,box[2],-12)]:
                    lo,hi=vertical_edges(loops[0],x);y=(lo+hi)/2+inset
                    assert inside(loops[0],(x,y)) and all(not inside(v,(x,y)) for v in loops[1:])
                    anchors[key]=[side/250,y/250]
                for key,point in list(anchors.items()):
                    if key.startswith('splitStem'):
                        x=min(max(point[0]*250,box[0]+2),box[2]-2);lo,hi=vertical_edges(loops[0],x)
                        anchors[key]=[x/250,(hi if 'Up' in key else lo)/250]
                if len(loops)>1:assert area(loops[0])*area(loops[1])<0
            if symbol=='noteheadXBlack':
                for key,x,side,which in [('stemDownNW',box[0]+2,box[0],-1),('stemUpSE',box[2]-2,box[2],0)]:
                    low,high=ink_intervals(loops,x)[which];y=(low+high)/2
                    assert sum(inside(v,(x,y)) for v in loops)%2
                    anchors[key]=[side/250,y/250]
                for key,point in list(anchors.items()):
                    if key.startswith('splitStem'):
                        x=min(max(point[0]*250,box[0]+2),box[2]-2)
                        low,high=ink_intervals(loops,x)[0 if 'Up' in key else -1]
                        anchors[key]=[x/250,(low+high)/500]
            if symbol.startswith('flag'):
                anchors['stemUpNW' if symbol.endswith('Up') else 'stemDownSW']=[0,0]
            if item['repeat']:anchors['repeatOffset']=[item['repeat']/250,0]
            report['changed'][symbol]=dict(codepoint=cp,glyph=glyph,advance=advance,bounds_sp=[v/250 for v in box],anchors=anchors,smufl=standard,
                cubic_segments=sum(op=='curveTo' for op,points in item.get('commands',[])))
        # MuseScore 3 composes dynamics from letter symbols. Default OpenType
        # liga selects the observed complete forms without changing score XML.
        rules=[]
        for target,components in LIGATURES:
            codes=[int(sm[n]['codepoint'][2:],16) for n in [target]+components]
            if all(c in cmap for c in codes):
                rules.append('sub %s by %s;'%(' '.join(cmap[c] for c in codes[1:]),cmap[codes[0]]))
                report['ligatures'].append(dict(target=target,components=components))
        if rules:add_ligatures(font,rules)
    meta.update(fontName=family,fontVersion=float(version))
    path=out/(family+'.otf');font.save(path);font.close()
    (out/(family+'.json')).write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    (out/'SOURCE.txt').write_text('LOCAL STUDY, NOT A PUBLIC FONT RELEASE.\nLeland baseline plus raster-derived user-PDF shapes.\nNo source font program recovered. Capture provenance remains in capture.json.\n',encoding='utf-8')
    (out/'Leland-OFL.txt').write_bytes((ROOT/'vendor/leland/LICENSE.txt').read_bytes())
    with TTFont(base_path) as base,TTFont(path) as result:
        assert set(base.getBestCmap()).issubset(result.getBestCmap())
        assert result.getGlyphOrder()[:len(original_order)]==original_order
        for tag in ('GPOS','GDEF'):
            if tag in base:assert tag in result and base[tag].compile(base)==result[tag].compile(result),tag
        allowed={v['glyph'] for v in report['changed'].values()}
        for glyph in original_order:
            a,b=RecordingPen(),RecordingPen();base.getGlyphSet()[glyph].draw(a);result.getGlyphSet()[glyph].draw(b)
            assert (a.value!=b.value)==(glyph in allowed),glyph
            if glyph not in allowed:assert base['hmtx'].metrics[glyph]==result['hmtx'].metrics[glyph]
        for symbol,row in report['changed'].items():
            actual=bounds(result.getGlyphSet(),row['glyph'])
            assert all(abs(a/250-b)<1e-5 for a,b in zip(actual,row['bounds_sp'])),symbol
            cs=result['CFF '].cff.topDictIndex[0].CharStrings[row['glyph']];record=RecordingPen();cs.draw(record)
            assert sum(op=='curveTo' for op,points in record.value)==row['cubic_segments'],symbol
            assert cs.width==row['advance']==result['hmtx'].metrics[row['glyph']][0]
        report.update(glyph_count=len(result.getGlyphOrder()),cmap_count=len(result.getBestCmap()),coverage_preserved=True,
                      unchanged_outlines_and_metrics_preserved=True,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return report


def run(args):
    assert not args.output.exists(),'Use a new build directory'
    data=json.loads(args.capture.read_text(encoding='utf-8'));sm=json.loads(args.glyphnames.read_text(encoding='utf-8'))
    report=dict(capture_sha256=hashlib.sha256(args.capture.read_bytes()).hexdigest(),fonts={})
    for control in [True,False]:
        for text in [False,True]:
            family=('Kumo Score Control' if control else 'Kumo Score Study')+(' Text' if text else '')
            base=ROOT/'vendor/leland'/('LelandText.otf' if text else 'Leland.otf')
            report['fonts'][family]=write_font(base,args.output/family,family,data,sm,control,text)
    (args.output/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Four local families built; complete baselines and unchanged glyphs/metrics verified.')
    for name,r in report['fonts'].items():print(name,'changed',len(r['changed']),'added',len(r['added']),'ligatures',len(r['ligatures']))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--glyphnames',type=Path,default=Path('E:/programming/funcodes/muse3_dev/MuseScore/fonts/smufl/glyphnames.json'))
    run(p.parse_args())
