"""Standard names plus the host's explicitly supported Leland brace alternates."""
import json
from pathlib import Path


def load_symbol_names(path):
    names=json.loads(Path(path).read_text(encoding='utf-8'))
    baseline=Path(__file__).resolve().parents[1]/'vendor/leland/leland_metadata.json'
    meta=json.loads(baseline.read_text(encoding='utf-8'))
    wanted={'braceSmall','braceLarge','braceLarger'}
    for row in meta['glyphsWithAlternates']['brace']['alternates']:
        if row['name'] in wanted:
            assert row['name'] not in names
            names[row['name']]=dict(codepoint=row['codepoint'],native_alternate_of='brace')
    assert wanted.issubset(names)
    return names
