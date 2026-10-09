"""Read selected user references and render observation crops, never extract fonts."""
import hashlib
import json
from pathlib import Path
import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent / 'dist/reference-review'
SOURCE = Path(r'C:\Users\Fred\OneDrive - yunzd\cloudreve\Sheets\【2021-】新官谱')
ROOT.mkdir(parents=True, exist_ok=True)
rows = []
for label, pattern in [('sincerely', 'Sincerely*'), ('idol', 'Idol*'), ('iris', 'IRIS OUT*'), ('shirushi', 'Shirushi*'), ('sparkle', 'Sparkle*'), ('unravel', 'unravel*')]:
    file = next(SOURCE.glob(pattern + '.pdf'))
    before = hashlib.sha256(file.read_bytes()).hexdigest()
    reader = PdfReader(str(file))
    families = set()
    for page in reader.pages:
        resources = page.get('/Resources').get_object()
        for font in resources.get('/Font', {}).values():
            families.add(str(font.get_object().get('/BaseFont', 'unknown')))
    doc = pdfium.PdfDocument(str(file))
    for i in range(min(2, len(doc))):
        page = doc[i]
        image = page.render(scale=5).to_pil()
        image.save(ROOT / ('%s-p%d.png' % (label, i + 1)))
        # Broad common-scale crop; inspect and select details later.
        w, h = image.size
        image.crop((int(w*.045), int(h*.2), int(w*.95), int(h*.52))).save(ROOT / ('%s-detail.png' % label))
        page.close()
    doc.close()
    assert hashlib.sha256(file.read_bytes()).hexdigest() == before
    rows.append(dict(label=label, path=str(file), sha256=before, fonts=sorted(families), pages=len(reader.pages)))
    print(label, sorted(families), flush=True)
(ROOT / 'sources.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
