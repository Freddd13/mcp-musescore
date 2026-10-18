"""Read-only PDF corpus preparation. Generated material stays under project tmp/."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
PRIVATE = REPO / 'tmp' / 'engraving'
SOURCE = Path(r'C:\Users\Fred\OneDrive - yunzd\cloudreve\Sheets\【2021-】新官谱')
CATALOG = REPO / 'docs' / 'engraving' / 'corpus' / 'inventory.json'
POPLER = Path(r'C:\Users\Fred\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe')


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory():
    from pypdf import PdfReader
    old = json.loads(CATALOG.read_text(encoding='utf-8')) if CATALOG.exists() else {}
    known = {r['relative_path']: r for r in old.get('scores', [])}
    paths = sorted(SOURCE.rglob('*.pdf'), key=lambda p: str(p.relative_to(SOURCE)).casefold())
    next_id = max((int(r['id'][1:]) for r in known.values()), default=0) + 1
    jobs = []
    for path in paths:
        relative = str(path.relative_to(SOURCE))
        prior = known.get(relative)
        sid = prior['id'] if prior else f'A{next_id:03d}'
        next_id += not bool(prior)
        jobs.append((path, relative, sid))

    def inspect(job):
        path, relative, sid = job
        row = {'id': sid, 'relative_path': relative, 'source_path': str(path)}
        try:
            reader = PdfReader(path)
            row.update(sha256=digest(path), bytes=path.stat().st_size, pages=len(reader.pages),
                       metadata={str(k): str(v) for k, v in (reader.metadata or {}).items()},
                       page_sizes_pt=sorted({(round(float(p.mediabox.width), 2), round(float(p.mediabox.height), 2)) for p in reader.pages}),
                       inventory_status='readable')
        except Exception as exc:
            row.update(inventory_status='error', error=repr(exc))
        return row

    rows = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(inspect, job) for job in jobs]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(f'{row["id"]}: {row.get("pages", "ERROR")} pages', flush=True)
    rows.sort(key=lambda r: r['id'])
    write_json(CATALOG, {'date': datetime.now().astimezone().isoformat(), 'source_root': str(SOURCE),
                        'scope': 'Every PDF recursively present in the user-provided directory at inventory time. File names do not establish publication authenticity.',
                        'score_count': len(rows), 'total_pages': sum(r.get('pages', 0) for r in rows),
                        'review_policy': 'Inventory and rendering do not count as visual review or analysis.', 'scores': rows})
    print(json.dumps({'scores': len(rows), 'pages': sum(r.get('pages', 0) for r in rows), 'errors': sum(r['inventory_status'] != 'readable' for r in rows)}))


def selected(ids):
    rows = json.loads(CATALOG.read_text(encoding='utf-8'))['scores']
    if not ids:
        return rows
    wanted = set(ids.split(','))
    return [r for r in rows if r['id'] in wanted]


def render(ids, workers, width):
    from PIL import Image, ImageDraw, ImageFont
    if not POPLER.is_file():
        raise FileNotFoundError(POPLER)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 24)

    def run(row):
        if row['inventory_status'] != 'readable':
            return {'id': row['id'], 'error': 'Unreadable source'}
        directory = PRIVATE / 'corpus' / row['id']
        directory.mkdir(parents=True, exist_ok=True)
        manifest = directory / 'render.json'
        existing = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {}
        complete = existing.get('source_sha256') == row['sha256'] and existing.get('width') == width and len(list(directory.glob('page-*.jpg'))) == row['pages']
        if not complete:
            args = [str(POPLER), '-scale-to-x', str(width), '-scale-to-y', '-1', '-jpeg', '-jpegopt', 'quality=90', row['source_path'], str(directory/'page')]
            result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
            (directory/'render.log').write_bytes((result.stdout+result.stderr).encode('utf-8'))
            if result.returncode:
                return {'id': row['id'], 'error': result.stderr[-1500:]}
            write_json(manifest, {'source_sha256': row['sha256'], 'width': width, 'command': args, 'returncode': result.returncode, 'visual_review': False})
        pages = sorted(directory.glob('page-*.jpg'), key=lambda p: int(p.stem.split('-')[-1]))
        if len(pages) != row['pages']:
            raise ValueError(f'Page render count mismatch for {row["id"]}')
        for start in range(0, len(pages), 6):
            group = pages[start:start+6]
            canvas = Image.new('RGB', (1800, ((len(group)+1)//2)*1310), '#dcdcd8')
            draw = ImageDraw.Draw(canvas)
            for i, path in enumerate(group):
                im = Image.open(path).convert('RGB')
                im.thumbnail((880, 1250))
                x, y = (i%2)*900, (i//2)*1310
                draw.text((x+12, y+5), f'{row["id"]} | PDF {int(path.stem.split("-")[-1])}', fill='#111111', font=font)
                canvas.paste(im, (x+(900-im.width)//2, y+45))
            target = directory/f'board-{start//6+1:02d}.jpg'
            canvas.save(target, quality=92)
        return {'id': row['id'], 'pages': len(pages), 'boards': (len(pages)+5)//6, 'cached': complete}

    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(run, row) for row in selected(ids)]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
    write_json(PRIVATE/'corpus'/'render-status.json', results)


def extract(ids):
    from pypdf import PdfReader
    for row in selected(ids):
        if row['inventory_status'] != 'readable':
            continue
        target = PRIVATE/'corpus'/row['id']/'text.json'
        if target.exists():
            continue
        reader = PdfReader(row['source_path'])
        pages = [{'pdf_page': n, 'text': page.extract_text() or ''} for n, page in enumerate(reader.pages, 1)]
        write_json(target, {'source_sha256': row['sha256'], 'warning': 'Private search aid, not a replacement for visual score reading; music glyph extraction is unreliable.', 'pages': pages})
        print(row['id'], flush=True)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    PRIVATE.mkdir(parents=True, exist_ok=True)
    temp = PRIVATE/'runtime-temp'
    temp.mkdir(exist_ok=True)
    os.environ.update(TEMP=str(temp), TMP=str(temp), TMPDIR=str(temp), MPLCONFIGDIR=str(temp/'matplotlib'), XDG_CACHE_HOME=str(temp/'cache'))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['inventory', 'render', 'extract'])
    parser.add_argument('--ids', default='')
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--width', type=int, default=1800)
    args = parser.parse_args()
    if args.command == 'inventory':
        inventory()
    elif args.command == 'render':
        render(args.ids, args.workers, args.width)
    else:
        extract(args.ids)


if __name__ == '__main__':
    main()
