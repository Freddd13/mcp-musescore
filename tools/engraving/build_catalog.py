"""Build the review index and a private, local-only image browser from recorded reading."""
import html
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BASE = REPO/'docs/engraving/corpus'
PRIVATE = REPO/'tmp/engraving/corpus'


def main():
    inventory = json.loads((BASE/'inventory.json').read_text(encoding='utf-8'))
    review = json.loads((BASE/'reviews.json').read_text(encoding='utf-8'))
    complete = {r['id']: r for r in review['scores']}
    partial = {r['id']: r for r in review.get('partial_scores', [])}
    lines = ['# 官谱全目录与阅读入口', '',
             f'目录共{inventory["score_count"]}份、{inventory["total_pages"]}页。已完成本轮逐谱案例记录{len(complete)}份，另有{len(partial)}份分段阅读中。页级记录见JSON；清点、渲染不计为阅读。', '',
             '[当前目标与完成条件](../CONTINUOUS_STUDY.md) · [阅读记录](reviews.json) · [证据核查](verification.json)', '',
             '本机图片在项目`tmp/engraving/corpus/`，打开其中`index.html`可按曲名、主题和阅读状态查图。原谱只读。历史专题与本轮分开，不重复冒计。', '',
             '| ID | 文件 | 页数 | 本轮阅读 | 笔记 |', '| --- | --- | ---: | --- | --- |']
    cards = []
    for score in inventory['scores']:
        row = complete.get(score['id']) or partial.get(score['id'])
        state = 'read' if score['id'] in complete else 'partial' if row else 'pending'
        label = '已有逐谱案例' if state == 'read' else f'部分：{len(row["screened_pages"])}/{score["pages"]}页' if row else '待逐谱阅读'
        note = f'[{row["note"]}]({row["note"]})' if row else '—'
        filename = score['relative_path'].replace('|', '&#124;')
        lines.append(f'| {score["id"]} | {filename} | {score["pages"]} | {label} | {note} |')
        topics = '、'.join(row['topics']) if row else '尚未记录本轮实际阅读，生成图片不等于已分析。'
        boards = ' '.join(f'<a href="{score["id"]}/board-{n:02d}.jpg">第{(n-1)*6+1}–{min(n*6,score["pages"])}页拼图</a>' for n in range(1,(score['pages']+5)//6+1))
        note_link = f'<a href="{(BASE/row["note"]).as_uri()}">研究笔记</a>' if row else ''
        key = html.escape(score['id']+' '+score['relative_path']+' '+topics, quote=True)
        cards.append(f'<article data-state="{state}" data-key="{key}"><h2>{score["id"]} · {html.escape(score["relative_path"][:-4])}</h2><p>{score["pages"]}页 · {label} · {note_link}</p><p>{html.escape(topics)}</p><details><summary>页面和原文件</summary><p>{boards}</p><a href="{Path(score["source_path"]).as_uri()}">只读原PDF</a><p><img loading="lazy" src="{score["id"]}/board-01.jpg"></p></details></article>')
    (BASE/'INDEX.md').write_bytes(('\n'.join(lines)+'\n').encode('utf-8'))
    intro = f'{inventory["score_count"]}份 / {inventory["total_pages"]}页。已有{len(complete)}份逐谱笔记，{len(partial)}份分段阅读中。这里是学习入口，尚未完成全目录研究。'
    page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>官谱净书学习</title><style>body{max-width:1200px;margin:32px auto;padding:0 20px;font:17px/1.65 system-ui;background:#f4f2ed;color:#202020}header{position:sticky;top:0;background:#f4f2ed;padding:12px 0;border-bottom:1px solid #aaa}input,select{font:inherit;padding:8px}input{width:60%}article{padding:18px 24px;margin:18px 0;background:white;border-radius:8px}h2{font-size:21px}a{color:#235b74;margin-right:12px}img{max-width:100%;height:auto}summary{cursor:pointer}#count{margin-left:12px}</style><header><h1>官谱净书学习</h1><p>'''+intro+'''</p><input id="query" placeholder="找曲名、主题或编号"><select id="state"><option value="all">全部</option><option value="read">已有逐谱案例</option><option value="partial">分段阅读中</option><option value="pending">待逐谱阅读</option></select><span id="count"></span></header>'''+''.join(cards)+'''<script>const q=document.getElementById('query'),s=document.getElementById('state');function filter(){let n=0;for(const a of document.querySelectorAll('article')){const yes=a.dataset.key.toLowerCase().includes(q.value.toLowerCase())&&(s.value==='all'||a.dataset.state===s.value);a.hidden=!yes;n+=yes;}document.getElementById('count').textContent=n+'份';}q.addEventListener('input',filter);s.addEventListener('change',filter);filter();</script></html>'''
    PRIVATE.mkdir(parents=True, exist_ok=True)
    (PRIVATE/'index.html').write_bytes(page.encode('utf-8'))
    print(f'Indexed {len(cards)} PDFs: {len(complete)} documented, {len(partial)} partial.')


if __name__ == '__main__':
    main()
